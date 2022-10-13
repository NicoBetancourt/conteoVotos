from frameworks.storage.client.client import get_connection
from domain.info.entreprise_bussines.entities.info_dom import Info_dom
from frameworks.storage.models.info_model import Info_dal
from decouple import config

table_name = config('TABLE_NAME')


class psql_driver():
    @classmethod
    def get_one(self, id):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    f"SELECT id, departamento,municipio,zona,mesa,link from {table_name} WHERE id = %s", id)
                row = cursor.fetchone()
                infoData = None

                if row != None:
                    infoData = Info_dom(
                        row[0], row[1], row[2], row[3], row[4], row[5])
                    infoData = infoData.to_JSON()

            connection.close()

            return infoData
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_all(self):
        try:
            connection = get_connection()
            infoData = []

            with connection.cursor() as cursor:
                cursor.execute(
                    f"SELECT id, departamento,municipio,zona,mesa,link from {table_name} ORDER BY departamento ASC")
                resultset = cursor.fetchall()

                for row in resultset:
                    info = Info_dom(row[0], row[1], row[2],
                                    row[3], row[4], row[5])
                    infoData.append(info.to_JSON())

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
                ))+") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

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
                ))+") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

                # args_str = ','.join(cursor.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", x) for x in info)
                # cursor.execute(f"INSERT INTO {table_name} VALUES " + args_str)

                cursor.executemany(str_query, info)
                affected_rows = cursor.rowcount
                connection.commit()
                connection.close()

            return affected_rows
        except Exception as ex:
            raise Exception(ex)
