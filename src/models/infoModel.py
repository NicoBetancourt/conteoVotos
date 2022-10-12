from database.db import get_connection
from .entities.info_dom import Info_dom
from decouple import config

table_name = config('TABLE_NAME')


class InfoModel():
    @classmethod
    def get_Info(self, id):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    f"SELECT id, departamento,municipio,zona,mesa,link from {table_name} WHERE id = %s", (id,))
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
    def get_AllInfo(self):
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
    def post_Info(self, info):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    f"INSERT INTO {table_name} (id, departamento,municipio,zona,mesa,link) VALUES (%s,%s,%s,%s,%s,%s)", (info.id, info.departamento, info.municipio, info.zona, info.mesa, info.link))
            affected_rows = cursor.rowcount
            connection.commit()
            connection.close()

            return affected_rows
        except Exception as ex:
            raise Exception(ex)
