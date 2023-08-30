import psycopg2
from frameworks.storage.client.client import get_connection
from domain.info.entreprise_bussines.entities.info_dom import Info_dom
from frameworks.storage.models.info_model import Info_dal
from decouple import config

table_name = config('TABLE_NAME')
# _logger = init_logger(__name__)

class psql_driver():
    @classmethod
    def create(self, table_name, columns, values):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                query = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({','.join(['%s']*len(columns))})"
                cursor.execute(query, values)
                affected_rows = cursor.rowcount
                connection.commit()
                cursor.close()
                print("Registro creado exitosamente.") # Logger
            return affected_rows
        except psycopg2.Error as e:
            raise Exception(e)

    @classmethod
    def get_all(self, table_name, condition=None):
        try:
            connection = get_connection()
            print('Estoy corriendo dentro de get all')
            with connection.cursor() as cursor:

                condition_query = f" WHERE {condition}" if condition else ""
                query = f"SELECT * FROM {table_name}{condition_query}"
                cursor.execute(query)
                result = cursor.fetchall()
                cursor.close()
            return result
        except psycopg2.Error as e:
            raise Exception(e)
    
    @classmethod
    def update(self, table_name, columns, values, condition=None):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:

                set_values = ", ".join([f"{column} = %s" for column in columns])
                condition_query = f" WHERE {condition}" if condition else ""
                query = f"UPDATE {table_name} SET {set_values}{condition_query}"
                cursor.execute(query, values)
                connection.commit()
                cursor.close()
        except psycopg2.Error as e:
            raise Exception(e)
        
    @classmethod
    def delete(self, table_name, condition=None):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:

                condition_query = f" WHERE {condition}" if condition else ""
                query = f"DELETE FROM {table_name}{condition_query}"
                cursor.execute(query)
                rows_affected = cursor.rowcount 
                connection.commit()
                cursor.close()
                return rows_affected
        except psycopg2.Error as e:
            raise Exception(e)

    @classmethod
    def get_one(self, table_name, id):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * from {table_name} WHERE id = %s", (id,))
                infoData = cursor.fetchone()

            connection.close()

            return infoData
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def add_one(self, info):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:

                str_query = f"INSERT INTO {table_name} ("+','.join(x for x in Info_dal.headers(
                ))+") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

                cursor.execute(str_query, (info))

                affected_rows = cursor.rowcount
                connection.commit()
                connection.close()

            return affected_rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def add_all(self, info):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                str_query = f"INSERT INTO {table_name} ("+','.join(x for x in Info_dal.headers(
                ))+") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

                # args_str = ','.join(cursor.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", x) for x in info)
                # cursor.execute(f"INSERT INTO {table_name} VALUES " + args_str)

                cursor.executemany(str_query, info)
                affected_rows = cursor.rowcount
                connection.commit()
                connection.close()

            return affected_rows
        except Exception as ex:
            raise Exception(ex)
