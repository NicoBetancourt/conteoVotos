from domain.info.interface_adapters.repositories.info_repository import InfoRepository
from frameworks.storage.postgres.client.driver.driver import psql_driver
from ..models.info_model import Info_dal

COLLECTION_NAME = 'infovotos';

class InfoPSQLRepository(InfoRepository):

    def __init__(self):
        super().__init__(self)
        self.info_dal = Info_dal()

    def create_info(self, values):
        columns = self.info_dal.headers()
        return psql_driver.create(COLLECTION_NAME, columns, values.to_List())

    def get_by_id(self, id):
        col_values = psql_driver.get_one(COLLECTION_NAME, id)
        return self.list_to_json(col_values)
    
    def get_all_info(self, filter):
        multi_values = psql_driver.get_all(COLLECTION_NAME, filter)
        return list(map( self.list_to_json, multi_values))
    
    def delete_info(self, filter):
        return psql_driver.delete(COLLECTION_NAME, filter)

    def update_info(self, values, filter):
        columns = self.info_dal.headers()
        return psql_driver.update(COLLECTION_NAME, columns, values.to_List(), filter)
    
    def list_to_json(self,values):
        dal = Info_dal()
        dal.id = values[0]
        dal.departamento = values[1]
        dal.municipio = values[2]
        dal.puesto = values[3]
        dal.zona = values[4]
        dal.mesa = values[5]
        dal.link = values[6]
        dal.votos_gustavo = values[7]
        dal.votos_ivan = values[8]
        dal.votos_blanco = values[9]
        dal.votos_nulos = values[10]
        dal.votos_no_marcados = values[11]
        dal.votos_total = values[12]
        dal.votos_sufragantes = values[13]
        dal.votos_urna = values[14]
        dal.votos_incinerados = values[15]
        dal.validar_total = values[16]
        dal.validar_votantes = values[17]
        return dal