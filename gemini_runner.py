import asyncio
import base64
import concurrent.futures
import io
import os
import time
from collections import defaultdict
from typing import Any  # Asegúrate de importar List, Dict, Any, Optional
from typing import Dict, List, Optional

import psycopg2
import requests
from decouple import config
from langchain.schema import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from pdf2image import convert_from_bytes
from psycopg2.extras import DictCursor, execute_values
from psycopg2.pool import SimpleConnectionPool
from pydantic import BaseModel
from tqdm import tqdm

# --- Configuración (igual que antes) ---
HOST = config("PGSQL_HOST")
USER = config("PGSQL_USER")
PASSWORD = config("PGSQL_PASSWORD")
PORT = config("PGSQL_PORT", default="5432")  # Añadir default por si acaso
DB_NAME = config("PGSQL_DATABASE")
TABLE_NAME = config("TABLE_NAME", default="infovotos")  # Añadir default
TABLE_CHECK = config("TABLE_CHECK", default="resumen")  # Añadir default
# --- Placeholder para tus modelos Pydantic ---

GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY") or ""


# Necesitarás definir estas clases según tu estructura de datos real
class InfoDOM(BaseModel):
    departamento: str
    municipio: str
    puesto: str
    zona: str
    mesa: str  # O int, ajusta según lo que extraiga el LLM
    votosGustavo: int
    votosIvan: int
    votosBlanco: int
    votosNulos: int
    votosNoMarcados: int
    votosTotal: int
    votosSufragantes: int
    votosUrna: int
    votosIncinerados: int


class InfoDOMs(BaseModel):
    items: List[InfoDOM]


class Tarjeton(BaseModel):
    # Define los campos de tu Tarjeton, incluyendo los que vienen de la BD
    # y los que se actualizan desde InfoDOM
    id: int  # Asumiendo que hay un id o clave primaria
    departamento: str
    municipio: str
    puesto: str
    zona: str
    mesa: str  # O int
    link: str
    votos_blanco: Optional[int] = None
    votos_gustavo: Optional[int] = None
    votos_incinerados: Optional[int] = None
    votos_ivan: Optional[int] = None
    votos_no_marcados: Optional[int] = None
    votos_nulos: Optional[int] = None
    votos_sufragantes: Optional[int] = None
    votos_total: Optional[int] = None
    votos_urna: Optional[int] = None

    def convert_from_dom(self, info_dom: InfoDOM):
        # Mapea los campos de InfoDOM a Tarjeton
        # ¡Cuidado con las mayúsculas/minúsculas y nombres!
        self.votos_blanco = info_dom.votosBlanco
        self.votos_gustavo = info_dom.votosGustavo
        self.votos_incinerados = info_dom.votosIncinerados
        self.votos_ivan = info_dom.votosIvan
        self.votos_no_marcados = info_dom.votosNoMarcados
        self.votos_nulos = info_dom.votosNulos
        self.votos_sufragantes = info_dom.votosSufragantes
        self.votos_total = info_dom.votosTotal
        self.votos_urna = info_dom.votosUrna
        # Asegúrate que departamento, municipio, puesto, zona, mesa coincidan
        # o añade lógica de validación si es necesario


class Check(BaseModel):
    id: int  # O el tipo que sea tu ID
    departamento: str
    municipio: str
    zona: str
    completado: bool


# --- Pool de Conexiones a la Base de Datos ---
# Ajusta minconn y maxconn según tus necesidades
db_pool = SimpleConnectionPool(
    minconn=1,
    maxconn=10,  # Aumenta si esperas mucha concurrencia
    dbname=DB_NAME,
    user=USER,
    password=PASSWORD,
    host=HOST,
    port=PORT,
)


# --- Funciones de Base de Datos (modificadas para usar el pool) ---
def get_connection_from_pool():
    return db_pool.getconn()


def return_connection_to_pool(conn):
    db_pool.putconn(conn)


def execute_query(query: str, params: tuple = None, fetch: str = None):
    """Función genérica para ejecutar consultas usando el pool."""
    conn = None
    try:
        conn = get_connection_from_pool()
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(query, params)
            conn.commit()
            if fetch == "one":
                return cursor.fetchone()
            elif fetch == "all":
                return cursor.fetchall()
            elif fetch == "count":
                return cursor.rowcount
            else:
                return None  # Para INSERT, UPDATE, DELETE sin retorno explícito
    except psycopg2.Error as e:
        # Considera hacer rollback en caso de error si es parte de una transacción mayor
        # if conn: conn.rollback()
        print(f"Error de Base de Datos: {e}")
        raise  # Relanza la excepción para que el flujo principal la maneje
    finally:
        if conn:
            return_connection_to_pool(conn)


def create_row(infoDom: InfoDOM, table_name: str = TABLE_NAME):
    # Esta función parece no usarse en el flujo principal, pero la adaptamos
    dictItem = infoDom.dict()
    columns = list(dictItem.keys())
    values = list(dictItem.values())
    placeholders = ", ".join(["%s"] * len(columns))
    query = f'INSERT INTO "{table_name}" ({",".join(columns)}) VALUES ({placeholders})'
    return execute_query(query, tuple(values), fetch="count")


def update_single_row(
    values: Dict[str, Any], table_name: str, columns: List[str], condition: str
):
    """Actualiza una única fila (usada para la tabla check)."""
    set_values = ", ".join([f'"{column}" = %s' for column in columns])
    query = f'UPDATE "{table_name}" SET {set_values} WHERE {condition}'
    # Asegúrate que los valores estén en el orden correcto de las columnas + condición si aplica
    # Esta implementación asume que la condición ya incluye sus valores o no necesita parámetros
    # Si la condición necesita params: f"id = %s", hay que pasar el valor de id al final de los values
    # Ejemplo: execute_query(query, tuple(list(values.values()) + [id_value]))
    return execute_query(query, tuple(values.values()), fetch="count")


def update_tarjeton_rows_batch(info_list: List[Tarjeton], table_name: str = TABLE_NAME):
    """Actualiza múltiples filas de tarjetones usando execute_values."""
    if not info_list:
        return 0

    columns_to_update = [
        "votos_blanco",
        "votos_gustavo",
        "votos_incinerados",
        "votos_ivan",
        "votos_no_marcados",
        "votos_nulos",
        "votos_sufragantes",
        "votos_total",
        "votos_urna",
    ]
    # Columnas para identificar la fila (claves primarias o únicas)
    key_columns = ["departamento", "municipio", "puesto", "zona", "mesa"]

    # Prepara los datos para execute_values: lista de tuplas
    # Cada tupla debe contener: (valor_col1, valor_col2, ..., valor_key1, valor_key2, ...)
    data_tuples = []
    for info in info_list:
        # Solo actualiza si tiene datos (evita sobreescribir con None si no se procesó)
        # O ajusta esta lógica si siempre quieres actualizar
        if info.votos_total is not None:  # Asume que votos_total es un buen indicador
            data_tuples.append(
                tuple(
                    [getattr(info, col) for col in columns_to_update]
                    + [getattr(info, col) for col in key_columns]
                )
            )

    if not data_tuples:
        print("No hay datos válidos para actualizar en el lote.")
        return 0

    set_clause = ", ".join([f'"{col}" = data.{col}' for col in columns_to_update])
    where_clause = " AND ".join([f't."{col}" = data.{col}' for col in key_columns])

    # Construye la consulta usando una tabla temporal (CTE o similar) con execute_values
    # La sintaxis exacta puede variar ligeramente, esto es común
    query = f"""
        UPDATE "{table_name}" AS t
        SET {set_clause}
        FROM (VALUES %s) AS data ({", ".join(columns_to_update + key_columns)})
        WHERE {where_clause};
    """

    conn = None
    try:
        conn = get_connection_from_pool()
        with conn.cursor() as cursor:
            # page_size controla cuántas filas se envían en cada lote a la BD
            execute_values(cursor, query, data_tuples, page_size=100)
            affected_rows = cursor.rowcount
            conn.commit()
            print(f"Actualización por lotes afectó {affected_rows} filas.")
            return affected_rows
    except psycopg2.Error as e:
        print(f"Error en actualización por lotes: {e}")
        if conn:
            conn.rollback()  # Importante hacer rollback en error de lote
        raise
    finally:
        if conn:
            return_connection_to_pool(conn)


def get_all_by_columns(
    params: Dict[str, Any], table_name: str = TABLE_NAME
) -> List[Dict]:
    columns = list(params.keys())
    values = list(params.values())
    where_clause = " AND ".join([f'"{col}" = %s' for col in columns])
    query = f'SELECT * FROM "{table_name}" WHERE {where_clause}'
    return execute_query(query, tuple(values), fetch="all")


def get_all_rows(table_name: str = TABLE_NAME, condition: str = None) -> List[Dict]:
    condition_query = f" WHERE {condition}" if condition else ""
    query = f'SELECT * FROM "{table_name}"{condition_query}'
    # Pasar los parámetros de forma segura si la condición los usa
    # Por ahora, asumimos que la condición es simple como "completado = true"
    return execute_query(query, fetch="all")


# --- Lógica Principal Refactorizada ---


# Placeholder: Función para convertir PDF a Base64 (DEBE ser implementada)
def pdf_to_image_base64(url, page_number=0, image_format="PNG"):
    try:
        # Descargar PDF desde la URL
        response = requests.get(url)
        pdf_file = io.BytesIO(response.content)

        # Convertir página específica a imagen
        images = convert_from_bytes(
            pdf_file.getvalue(), poppler_path="/opt/homebrew/bin/"
        )

        # Seleccionar página específica (por defecto la primera)
        page_image = images[page_number]

        # Convertir imagen a base64
        buffered = io.BytesIO()
        page_image.save(buffered, format=image_format)
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return img_base64

    except Exception as e:
        print(f"Error procesando PDF: {e}")
        return None


async def process_images_batch_async(
    base64_images: list[str],
    api_key: str = GOOGLE_API_KEY,
    model: str = "gemini-1.5-flash",  # Usar un modelo reciente si es posible
    batch_id: str = "batch",  # Para logging/seguimiento
) -> List[InfoDOM]:
    """Procesa un único lote de imágenes de forma asíncrona."""
    if not base64_images:
        return []

    inicio = time.time()
    print(f"[{batch_id}] Processing {len(base64_images)} images...")

    text_prompt = {
        "type": "text",
        "text": "Extract the information of theses documents",
    }
    image_urls = [
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
        }
        for base64_image in base64_images
        if base64_image  # Ignora Nones
    ]

    if not image_urls:
        print(f"[{batch_id}] No valid images to process.")
        return []

    content = [text_prompt] + image_urls
    messages = [
        SystemMessage(
            content="""
                You will extract text from the next image, where there are some votes for different political parties.
                The text is in Spanish.

                The output follows the next example format exactly, including quotes for strings and correct numbers:
                    - departamento='ANTIOQUIA'
                    - municipio='MEDELLIN'
                    - puesto='01'
                    - zona='01'
                    - mesa='019'
                    - votosGustavo=21
                    - votosIvan=42
                    - votosBlanco=3
                    - votosNulos=2
                    - votosNoMarcados=0
                    - votosTotal=68
                    - votosSufragantes=68
                    - votosUrna=68
                    - votosIncinerados=0

                Provide one block like the example for each document image detected.
                Return the results as a list under the key 'items'.
            """
        ),
        HumanMessage(content=content),
    ]

    try:
        # Reutilizar el cliente LLM si es posible fuera de la función para evitar recrearlo
        # Pero si necesitas diferentes configs por llamada, créalo aquí.
        llm = ChatGoogleGenerativeAI(model=model, api_key=api_key, temperature=0)
        llm_structured = llm.with_structured_output(InfoDOMs)

        # Usar ainoke para la llamada asíncrona
        response = await llm_structured.ainvoke(messages)

        print(
            f"[{batch_id}] Batch processed in: {time.time() - inicio:.3f}s. Items extracted: {len(response.items)}"
        )
        return response.items
    except Exception as e:
        print(f"[{batch_id}] Error processing batch with LLM: {e}")
        # Considera reintentos o manejo específico de errores de API aquí
        return []  # Devuelve lista vacía en caso de error


def convert_pdfs_concurrently(links: List[str]) -> List[Optional[str]]:
    """Usa ThreadPoolExecutor para convertir PDFs en paralelo."""
    results = []
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=8
    ) as executor:  # Ajusta max_workers
        # Submit tasks
        future_to_link = {
            executor.submit(pdf_to_image_base64, link): link for link in links
        }
        # Collect results as they complete
        for future in tqdm(
            concurrent.futures.as_completed(future_to_link),
            total=len(links),
            desc="Convirtiendo PDFs",
        ):
            link = future_to_link[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as exc:
                print(f"PDF {link} generó una excepción: {exc}")
                results.append(None)  # Añadir None si falla la conversión
    # Es posible que los resultados no estén en el mismo orden que los links
    # Si el orden importa, necesitas mapearlos de vuelta
    # Por ahora, simplemente devolvemos la lista de resultados (base64 o None)
    # Necesitarás asociar estos resultados con los tarjetones originales después.
    # Vamos a devolver un diccionario para facilitar el mapeo:
    link_to_base64 = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        future_to_link = {
            executor.submit(pdf_to_image_base64, link): link for link in links
        }
        for future in tqdm(
            concurrent.futures.as_completed(future_to_link),
            total=len(links),
            desc="Convirtiendo PDFs",
        ):
            link = future_to_link[future]
            try:
                link_to_base64[link] = future.result()
            except Exception as exc:
                print(f"PDF {link} generó una excepción: {exc}")
                link_to_base64[link] = None
    return link_to_base64


async def process_puesto_group(
    puesto: str,
    grupo_tarjetones: List[Tarjeton],
    link_to_base64_map: Dict[str, Optional[str]],
    api_key: str,
    model: str,
    batch_size: int = 40,  # Hacer configurable el tamaño del lote
):
    """Procesa un grupo de tarjetones para un puesto específico."""
    print(f"Procesando puesto: {puesto} con {len(grupo_tarjetones)} tarjetones")

    images_base64 = [link_to_base64_map.get(t.link) for t in grupo_tarjetones]
    valid_images = [img for img in images_base64 if img is not None]

    if not valid_images:
        print(f"Puesto {puesto}: No hay imágenes válidas para procesar.")
        return []  # Devuelve lista vacía si no hay imágenes

    all_info_doms: List[InfoDOM] = []
    tasks = []
    # Crear tareas asyncio para procesar lotes de imágenes
    for i in range(0, len(valid_images), batch_size):
        batch_images = valid_images[i : i + batch_size]
        batch_id = f"Puesto_{puesto}_Batch_{i // batch_size + 1}"
        tasks.append(process_images_batch_async(batch_images, api_key, model, batch_id))

    # Ejecutar tareas concurrentemente
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Recolectar resultados y manejar excepciones
    for result in results:
        if isinstance(result, Exception):
            print(
                f"Puesto {puesto}: Una tarea de procesamiento de lote falló: {result}"
            )
            # Podrías decidir si continuar o marcar el puesto como fallido
        elif result:  # Si no es excepción y no es None/vacío
            all_info_doms.extend(result)

    if not all_info_doms:
        print(f"Puesto {puesto}: No se extrajo información de las imágenes.")
        return []  # No hay nada que mapear

    # --- Mapeo Mejorado ---
    # Crear un diccionario para búsqueda rápida de info_dom por mesa
    # Normalizar las mesas extraídas (quitar ceros iniciales, convertir a string consistente)
    info_dom_map = {}
    for info_dom in all_info_doms:
        try:
            # Normalizar la mesa extraída (ej: '019' -> '19')
            mesa_key = (
                str(int(info_dom.mesa))
                if info_dom.mesa.isdigit()
                else info_dom.mesa.lower()
            )
            info_dom_map[mesa_key] = info_dom
        except Exception as e:
            print(
                f"Advertencia: No se pudo procesar/normalizar mesa '{info_dom.mesa}' del LLM: {e}"
            )

    updated_tarjetones = []
    for tarjeton in grupo_tarjetones:
        try:
            # Normalizar la mesa del tarjetón para la comparación
            tarjeton_mesa_key = (
                str(int(tarjeton.mesa))
                if isinstance(tarjeton.mesa, int) or tarjeton.mesa.isdigit()
                else tarjeton.mesa.lower()
            )

            info_dom = info_dom_map.get(tarjeton_mesa_key)

            if info_dom:
                # Validar consistencia básica si es necesario
                # ej: if info_dom.departamento == tarjeton.departamento: ...
                tarjeton.convert_from_dom(info_dom)
                updated_tarjetones.append(tarjeton)
            else:
                print(
                    f"Advertencia: No se encontró InfoDOM para Tarjeton Mesa '{tarjeton_mesa_key}' en Puesto {puesto}"
                )
        except Exception as e:
            print(
                f"Error mapeando Tarjeton Mesa '{tarjeton.mesa}' en Puesto {puesto}: {e}"
            )

    print(f"Puesto {puesto}: {len(updated_tarjetones)} tarjetones mapeados con éxito.")
    return updated_tarjetones


async def main_async():
    start_total_time = time.time()
    resumen = get_all_rows(table_name=TABLE_CHECK, condition="completado = true")
    print(f"Encontrados {len(resumen)} items en resumen para procesar.")

    for item_data in tqdm(resumen, desc="Procesando resumen items"):
        item_check = Check(
            id=item_data["id"],  # Acceder por nombre de columna
            departamento=item_data["departamento"],
            municipio=item_data["municipio"],
            zona=item_data["zona"],
            completado=item_data["completado"],
        )
        print(
            f"\nProcesando item: ID={item_check.id}, Depto={item_check.departamento}, Mun={item_check.municipio}, Zona={item_check.zona}"
        )

        try:
            data = get_all_by_columns(
                table_name=TABLE_NAME,
                params=item_check.model_dump(
                    include={"departamento", "municipio", "zona"}
                ),  # Usar include
            )
            if not data:
                print(
                    f"  No se encontraron tarjetones para el item {item_check.id}. Saltando."
                )
                # Marcar como no completado (o manejar como prefieras)
                update_single_row(
                    {"completado": False},  # Valor a actualizar
                    table_name=TABLE_CHECK,
                    columns=["completado"],  # Columna a actualizar
                    condition=f"id = {item_check.id}",  # Condición (¡cuidado con SQL injection si ID no es número!)
                    # Mejor: condition="id = %s", y pasar [item_check.id] como segundo param a execute_query
                )
                continue

            tarjetones = [
                Tarjeton(**dict(item)) for item in data
            ]  # Convertir DictRow a dict

            # --- 1. Convertir todos los PDFs para este item concurrentemente ---
            all_links = list(
                set([t.link for t in tarjetones])
            )  # Evitar duplicados si es posible
            link_to_base64_map = convert_pdfs_concurrently(all_links)

            # --- 2. Agrupar por puesto ---
            tarjetones_por_puesto = defaultdict(list)
            for tarjeton in tarjetones:
                tarjetones_por_puesto[tarjeton.puesto].append(tarjeton)

            # --- 3. Procesar cada grupo de puesto concurrentemente ---
            puesto_tasks = []
            for puesto, grupo_tarjetones in tarjetones_por_puesto.items():
                puesto_tasks.append(
                    process_puesto_group(
                        puesto,
                        grupo_tarjetones,
                        link_to_base64_map,
                        GOOGLE_API_KEY,
                        "gemini-1.5-flash",  # O el modelo que uses
                    )
                )

            # Ejecutar el procesamiento de todos los puestos para este item en paralelo
            results_por_puesto = await asyncio.gather(
                *puesto_tasks, return_exceptions=True
            )

            # --- 4. Recolectar todos los tarjetones actualizados y actualizar BD en lote ---
            all_updated_tarjetones: List[Tarjeton] = []
            item_valido = True
            for result in results_por_puesto:
                if isinstance(result, Exception):
                    print(
                        f"  Error procesando un puesto para item {item_check.id}: {result}"
                    )
                    item_valido = False
                    # Decide si quieres parar todo el item o solo saltar este puesto
                    # break # Descomenta para parar si un puesto falla
                elif result:  # Lista de tarjetones actualizados para ese puesto
                    all_updated_tarjetones.extend(result)

            if not all_updated_tarjetones:
                print(f"  No se actualizaron tarjetones para el item {item_check.id}.")
                # Decide qué hacer aquí, ¿marcar como completado=False?
                # Quizás solo si item_valido es True pero no hubo nada que actualizar.

            # Actualizar la base de datos en un solo lote grande
            if all_updated_tarjetones:
                print(
                    f"  Actualizando {len(all_updated_tarjetones)} tarjetones en la base de datos..."
                )
                try:
                    update_tarjeton_rows_batch(
                        all_updated_tarjetones, table_name=TABLE_NAME
                    )
                except Exception as db_error:
                    print(
                        f"  FALLO la actualización de la base de datos para item {item_check.id}: {db_error}"
                    )
                    item_valido = False  # Marcar como inválido si la BD falla

            # --- 5. Actualizar el estado del item en la tabla 'resumen' ---
            # Actualiza a False solo si TODO el procesamiento fue válido
            if item_valido:
                print(
                    f"  Item {item_check.id} procesado con éxito. Actualizando estado."
                )
                # OJO: La lógica original pone completado=False. Asegúrate que sea correcto.
                # Si significa "procesado y ya no pendiente", entonces False está bien.
                update_single_row(
                    {"completado": False},
                    table_name=TABLE_CHECK,
                    columns=["completado"],
                    condition=f"id = {item_check.id}",  # Mejorar seguridad si ID no es número
                )
            else:
                print(
                    f"  Item {item_check.id} tuvo errores durante el procesamiento. NO se actualiza estado a False."
                )
                # Podrías querer marcarlo con otro estado, como 'error'

        except Exception as e:
            print(f"\nError GRAVE procesando item {item_check.id}: {e}")
            # Considera marcar este item como erróneo en la tabla de check
            # update_single_row({"completado": None, "error_flag": True}, ...)

    end_total_time = time.time()
    print(f"\nProceso completado en {end_total_time - start_total_time:.2f} segundos.")


# --- Punto de Entrada ---
if __name__ == "__main__":
    # Validar que GOOGLE_API_KEY está presente
    if not GOOGLE_API_KEY:
        raise ValueError("La variable de entorno GOOGLE_API_KEY no está configurada.")

    # Ejecutar el bucle principal asíncrono
    asyncio.run(main_async())

    # Cerrar el pool de conexiones al final
    db_pool.closeall()
    print("Pool de conexiones cerrado.")
    # Cerrar el pool de conexiones al final
    db_pool.closeall()
    print("Pool de conexiones cerrado.")
    print("Pool de conexiones cerrado.")
    # Cerrar el pool de conexiones al final
    db_pool.closeall()
    print("Pool de conexiones cerrado.")
    print("Pool de conexiones cerrado.")
    # Cerrar el pool de conexiones al final
    db_pool.closeall()
    print("Pool de conexiones cerrado.")
    print("Pool de conexiones cerrado.")
