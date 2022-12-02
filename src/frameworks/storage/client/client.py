import psycopg2
from psycopg2 import DatabaseError
from decouple import config


def get_connection():
    try:
        return psycopg2.connect(
            host=config('PGSQL_HOST'),
            user=config('PGSQL_USER'),
            password=config('PGSQL_PASSWORD'),
            port=config('PGSQL_PORT'),
            database=config('PGSQL_DATABASE'),
        )
    except DatabaseError as ex:
        raise ex


def create_new_table():
    table_name = config('TABLE_NAME')
    print('Crea la base de datos {} si no existe'.format(table_name))
    create_table = f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id VARCHAR(50),
                    departamento VARCHAR(50),
                    municipio VARCHAR(50),
                    puesto VARCHAR(50),
                    zona VARCHAR(50),
                    mesa VARCHAR(50),
                    link VARCHAR(150),
                    votos_gustavo SMALLINT,
                    votos_ivan SMALLINT,
                    votos_blanco SMALLINT,
                    votos_nulos SMALLINT,
                    votos_no_marcados SMALLINT,
                    votos_total INT,
                    votos_sufragantes INT,
                    votos_urna INT,
                    votos_incinerados SMALLINT,
                    validar_total BOOLEAN,
                    validar_totantes BOOLEAN
                )
                """

    connection = get_connection()
    cur = connection.cursor()
    cur.execute(create_table)
    connection.commit()
