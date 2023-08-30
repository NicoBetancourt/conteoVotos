from domain.info.entreprise_bussines.repository_reader import RepositoryReader
from domain.info.entreprise_bussines.entities.info_dom import Info_dom
from frameworks.storage.models.info_model import Info_dal

class InfoRepository(RepositoryReader):

    def __init__(self, implementation):
        """
        Currently this project is using PostgreSQL
        :param implementation: Used database repository.
        """
        self.impl = implementation

    def get_all(self, filters):
        infoDal = self.impl.get_all_info(self.filterDomToDal(filters))
        infoDom = list(map(self.fromDalToDom, infoDal))
        return infoDom

    def get_one(self, id: int):
        infoDal = self.impl.get_by_id(id)
        infoDom = self.fromDalToDom(infoDal)
        return infoDom

    def create(self, item):
        infoDal = self.fromDomToDal(item)
        return self.impl.create(infoDal)

    def update(self, id: int):
        return self.impl.update(self, id)

    def delete(self, filters):
        filter = self.filterDomToDal(filters)

        if (filter == ''):
            raise ValueError('Any filter was included')
        
        rowsDeleted = self.impl.delete_info(filter)
        return rowsDeleted
    
    def fromDalToDom(self, itemDal):
        dom = Info_dom(*itemDal)
        return dom
    
    def fromDomToDal(self, itemDom):
        dal = Info_dal(*itemDom)
        return dal
    
    def filterDomToDal(self, itemArray):
        mapFilter = []
        for item in itemArray:
            mapFilter.append(f"{item} LIKE '{itemArray[item]}%'")

        condition = ' AND '.join(mapFilter)
        return condition

