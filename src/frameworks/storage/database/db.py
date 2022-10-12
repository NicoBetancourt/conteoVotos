import psycopg2
from psycopg2 import DatabaseError
from decouple import config


def get_connection():
    try:
        return psycopg2.connect(
            host=config('PGSQL_HOST'),
            user=config('PGSQL_USER'),
            password=config('PGSQL_PASSWORD'),
            port=5432,
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
                    departamento VARCHAR(30),
                    municipio VARCHAR(30),
                    zona VARCHAR(5),
                    mesa VARCHAR(5),
                    link VARCHAR(5),
                    votosGustavo SMALLINT,
                    votosIvan SMALLINT,
                    votosBlanco SMALLINT,
                    votosNulos SMALLINT,
                    votosNoMarcados SMALLINT,
                    votosTotal INT,
                    votosSufragantes INT,
                    votosUrna INT,
                    votosIncinerados SMALLINT,
                    validarTotal BOOLEAN,
                    validarVotantes BOOLEAN
                )
                """
    connection = get_connection()
    cur = connection.cursor()
    cur.execute(create_table)
    connection.commit()
