from domain.info.interface_adapters.repositories.info_repository import InfoRepository
from frameworks.storage.client.driver.driver_2 import psql_driver
from ..models.info_model import Info_dal

COLLECTION_NAME = 'infovotos';

class InfoPSQLRepository(InfoRepository):

    def __init__(self):
        super().__init__(self)
        self.info_dal = Info_dal

    def create_info(self, values):
        columns = [self.info_dal.headers()]
        return psql_driver.add_one(COLLECTION_NAME, columns, values)

    def get_by_id(self, id):
        return psql_driver.get_one(COLLECTION_NAME, id)
    
    def get_all_info(self, filter):
        return psql_driver.get_all(COLLECTION_NAME, filter)
    
    def delete_info(self, filter):
        return psql_driver.delete(COLLECTION_NAME, filter)

    def update_info_by_columna1(self, columna1, nueva_columna2):
        columns = ['columna2']
        values = [nueva_columna2]
        condition = 'columna1 = %s'
        return psql_driver.update(COLLECTION_NAME, columns, values, condition=condition, params=(columna1,))