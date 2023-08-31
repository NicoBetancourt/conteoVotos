import psycopg2
from psycopg2 import DatabaseError
from decouple import config

_HOST = config('PGSQL_HOST')
_USER = config('PGSQL_USER')
_PASSWORD = config('PGSQL_PASSWORD')
_PORT = config('PGSQL_PORT')
_DB_NAME = config('PGSQL_DATABASE')

table_name = config('TABLE_NAME')

class PostgresClient:
    def __init__(self, _DB_NAME, _USER, _PASSWORD, _HOST, _PORT):
        self.dbname = _DB_NAME
        self.user = _USER
        self.password = _PASSWORD
        self.host = _HOST
        self.port = _PORT
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
        except DatabaseError as ex:
            raise ex

def get_connection():
    try:
        return psycopg2.connect(
            host=_HOST,
            user=_USER,
            password=_PASSWORD,
            port=_PORT,
            database=_DB_NAME,
        )
    except DatabaseError as ex:
        raise ex

def create_new_table():
    
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
                    validar_votantes BOOLEAN
                )
                """

    connection = get_connection()
    cur = connection.cursor()
    cur.execute(create_table)
    connection.commit()