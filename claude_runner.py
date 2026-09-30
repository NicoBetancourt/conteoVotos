import concurrent.futures
import os
import time
from typing import List

from langchain.schema import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or ""

google_api_key = SecretStr(GEMINI_API_KEY)

from pydantic import BaseModel, Field


class InfoDOM(BaseModel):
    departamento: str = Field(description="Nombre del departamento")
    municipio: str = Field(description="Nombre del municipio")
    puesto: str = Field(description="Número del puesto (formateado como '01')")
    zona: str = Field(description="Número de la zona (formateado como '01')")
    mesa: str = Field(description="Número de la mesa (formateado como '001')")
    votosGustavo: int = Field(description="Número de votos para Gustavo Petro")
    votosIvan: int = Field(description="Número de votos para Ivan Duque")
    votosBlanco: int = Field(description="Número de votos en Blanco")
    votosNulos: int = Field(description="Número de votos en Nulos")
    votosNoMarcados: int = Field(description="Número de votos en No Marcados")
    votosTotal: int = Field(description="Número total de motos de la mesa")
    votosSufragantes: int = Field(description="Número total de votos sufragantes")
    votosUrna: int = Field(description="Número total de votos en la urna")
    votosIncinerados: int = Field(description="Número total de votos incinerados")


class InfoDOMs(BaseModel):
    items: List[InfoDOM] = Field(description="Lista de objetos InfoDOM")


class Check(BaseModel):
    id: str
    departamento: str
    municipio: str
    zona: str
    completado: bool = False


class Tarjeton(BaseModel):
    id: str
    departamento: str
    municipio: str
    puesto: str
    zona: str
    mesa: str
    link: str
    votos_gustavo: int = 0
    votos_ivan: int = 0
    votos_blanco: int = 0
    votos_nulos: int = 0
    votos_no_marcados: int = 0
    votos_total: int = 0
    votos_sufragantes: int = 0
    votos_urna: int = 0
    votos_incinerados: int = 0
    validar_total: bool = False
    validar_votantes: bool = False

    def convert_from_dom(self, dom: InfoDOM):
        self.votos_gustavo = dom.votosGustavo
        self.votos_ivan = dom.votosIvan
        self.votos_blanco = dom.votosBlanco
        self.votos_nulos = dom.votosNulos
        self.votos_no_marcados = dom.votosNoMarcados
        self.votos_total = dom.votosTotal
        self.votos_sufragantes = dom.votosSufragantes
        self.votos_urna = dom.votosUrna
        self.votos_incinerados = dom.votosIncinerados
        self.validar_total = (
            self.votos_total
            == (
                self.votos_gustavo
                + self.votos_ivan
                + self.votos_blanco
                + self.votos_nulos
                + self.votos_no_marcados
            )
            and self.votos_total == self.votos_urna
        )
        self.validar_votantes = self.votos_sufragantes == (
            self.votos_urna + self.votos_incinerados
        )


def process_single_image_batch(
    batch_images: list[str], api_key, model="gemini-2.0-flash"
):
    text = {"type": "text", "text": "Extract the information of these documents"}
    image_urls = [
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
        }
        for base64_image in batch_images
    ]

    content = [text] + image_urls
    messages = [
        SystemMessage("""
        You will extract text from the next image, where there are some votes for different political parties.
        The text is in Spanish.

        The output follows the next example:
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
                """),
        HumanMessage(content),  # type: ignore
    ]

    llm = ChatGoogleGenerativeAI(model=model, api_key=api_key, temperature=0)
    llm_structured = llm.with_structured_output(InfoDOMs)
    response = llm_structured.invoke(messages)
    return response.items


def process_images_chain(
    base64_images: list[str],
    api_key,
    model="gemini-2.0-flash",
    max_workers=4,
    batch_size=10,
) -> List:
    inicio = time.time()
    print(f"Processing {len(base64_images)} images")

    all_results = []
    # Create batches of optimal size (smaller than 40 for better parallelism)
    batches = [
        base64_images[i : i + batch_size]
        for i in range(0, len(base64_images), batch_size)
    ]

    # Process batches in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_batch = {
            executor.submit(process_single_image_batch, batch, api_key, model): batch
            for batch in batches
        }

        for future in concurrent.futures.as_completed(future_to_batch):
            try:
                results = future.result()
                all_results.extend(results)
            except Exception as exc:
                print(f"Batch processing generated an exception: {exc}")

    print(f"Images processed: {time.time() - inicio:.5f} seconds")
    return all_results


from contextlib import contextmanager

import psycopg2
from decouple import config
from psycopg2.extras import DictCursor, execute_batch
from psycopg2.pool import ThreadedConnectionPool

# Database configuration
HOST = config("PGSQL_HOST")
USER = config("PGSQL_USER")
PASSWORD = config("PGSQL_PASSWORD")
PORT = config("PGSQL_PORT")
DB_NAME = config("PGSQL_DATABASE")
table_name = config("TABLE_NAME")
table_check = "resumen"

# Create a connection pool
pool = ThreadedConnectionPool(
    5,  # Minimum number of connections
    20,  # Maximum number of connections
    dbname=DB_NAME,
    user=USER,
    password=PASSWORD,
    host=HOST,
    port=PORT,
)


@contextmanager
def get_connection():
    """Context manager for getting a connection from the pool"""
    conn = pool.getconn()
    try:
        yield conn
    finally:
        pool.putconn(conn)


def create_row(infoDom, table_name=table_name):
    try:
        dictItem = infoDom.dict()
        columns = list(dictItem.keys())
        values = list(dictItem.values())

        with get_connection() as connection:
            with connection.cursor() as cursor:
                query = f'INSERT INTO "{table_name}" ({",".join(columns)}) VALUES ({",".join(["%s"] * len(columns))})'
                cursor.execute(query, values)
                affected_rows = cursor.rowcount
                connection.commit()
        return affected_rows
    except psycopg2.Error as e:
        raise Exception(e)


def update_row(values, table_name=table_name, columns=[], condition=None):
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                set_values = ", ".join([f"{column} = %s" for column in columns])
                condition_query = f" WHERE {condition}" if condition else ""
                query = f"UPDATE {table_name} SET {set_values}{condition_query}"
                cursor.execute(query, list(values.values()))
                connection.commit()
    except psycopg2.Error as e:
        raise Exception(e)


def update_rows(info_list, table_name):
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
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

                # Prepare column names for SET
                set_values = ", ".join(
                    [f"{column} = %s" for column in columns_to_update]
                )

                # Condition to identify the row
                condition = (
                    "departamento = %s AND municipio = %s AND puesto = %s "
                    "AND zona = %s AND mesa = %s"
                )

                # Build SQL query
                query = f"UPDATE {table_name} SET {set_values} WHERE {condition}"

                # Prepare batch parameters
                batch_params = []
                for info in info_list:
                    # Values for columns to update and for WHERE condition
                    values = [
                        info.votos_blanco,
                        info.votos_gustavo,
                        info.votos_incinerados,
                        info.votos_ivan,
                        info.votos_no_marcados,
                        info.votos_nulos,
                        info.votos_sufragantes,
                        info.votos_total,
                        info.votos_urna,
                        info.departamento,
                        info.municipio,
                        info.puesto,
                        info.zona,
                        info.mesa,
                    ]
                    batch_params.append(values)

                # Execute batch update
                execute_batch(cursor, query, batch_params, page_size=100)
                connection.commit()

    except Exception as e:
        print(f"Error while updating rows: {e}")


def get_all_by_columns(params, table_name=table_name):
    try:
        columns = list(params.keys())
        values = list(params.values())
        where_clause = " AND ".join([f'"{col}" = %s' for col in columns])

        with get_connection() as connection:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                query = f'SELECT * FROM "{table_name}" WHERE {where_clause}'
                cursor.execute(query, values)
                infoData = cursor.fetchall()
        return infoData
    except Exception as ex:
        raise Exception(ex)


def get_all_rows(table_name=table_name, condition=None):
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                condition_query = f" WHERE {condition}" if condition else ""
                query = f'SELECT * FROM "{table_name}"{condition_query}'
                cursor.execute(query)
                result = cursor.fetchall()
        return result
    except psycopg2.Error as e:
        raise Exception(e)


import base64
import io
import re
from collections import defaultdict

import requests
from pdf2image import convert_from_bytes
from tqdm import tqdm


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


def process_puesto(puesto, grupo_tarjetones, table_name):
    print(f"Processing puesto: {puesto}")

    # Extract links and convert to base64
    enlaces = [tarjeton.link for tarjeton in grupo_tarjetones]

    # Process images in smaller parallel batches for better efficiency
    images_base64_raw = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        images_base64_raw = list(executor.map(pdf_to_image_base64, enlaces))

    images_base64 = [img for img in images_base64_raw if img is not None]

    try:
        # Process images with optimized batch size and concurrency
        info_doms = process_images_chain(
            images_base64,
            api_key=google_api_key,
            batch_size=5,  # Smaller batches for better parallelism
            max_workers=4,  # Adjust based on CPU cores and API rate limits
        )

        # Match extracted data to tarjetones
        for tarjeton in grupo_tarjetones:
            if isinstance(tarjeton.mesa, int):
                tarjeton_mesa_numero = int(
                    re.search(r"\d+", str(tarjeton.mesa)).group()
                )
                info_dom = next(
                    (
                        info_dom
                        for info_dom in info_doms
                        if info_dom.mesa == tarjeton_mesa_numero
                    ),
                    None,
                )
            else:
                info_dom = next(
                    (
                        info_dom
                        for info_dom in info_doms
                        if str(info_dom.mesa).lower() == str(tarjeton.mesa).lower()
                    ),
                    None,
                )

            if info_dom:
                tarjeton.convert_from_dom(info_dom)

        # Update all rows at once
        update_rows(grupo_tarjetones, table_name=table_name)
        return True
    except Exception as e:
        print(f"Error processing puesto {puesto}: {e}")
        return False


def main_processing():
    resumen = get_all_rows(table_name=table_check, condition="completado = true")

    for item in tqdm(resumen, desc="Processing summary"):
        item_check = Check(
            id=item[0],
            departamento=item[1],
            municipio=item[2],
            zona=item[3],
            completado=item[4],
        )

        data = get_all_by_columns(
            table_name=table_name,
            params=item_check.model_dump(exclude={"id", "completado"}),
        )

        tarjetones = [Tarjeton(**item) for item in data]

        # Group tarjetones by puesto
        tarjetones_por_puesto = defaultdict(list)
        for tarjeton in tarjetones:
            tarjetones_por_puesto[tarjeton.puesto].append(tarjeton)

        # Process each puesto in parallel
        all_successful = True
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            future_to_puesto = {
                executor.submit(process_puesto, puesto, grupo, table_name): puesto
                for puesto, grupo in tarjetones_por_puesto.items()
            }

            for future in concurrent.futures.as_completed(future_to_puesto):
                puesto = future_to_puesto[future]
                try:
                    success = future.result()
                    if not success:
                        all_successful = False
                except Exception as exc:
                    print(f"Puesto {puesto} generated an exception: {exc}")
                    all_successful = False

        if all_successful:
            update_row(
                {"completado": False},
                table_name=table_check,
                columns=["completado"],
                condition=f"id = '{item_check.id}'",
            )


if __name__ == "__main__":
    main_processing()
if __name__ == "__main__":
    main_processing()
