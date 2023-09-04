from domain.info.entreprise_bussines.repository_reader import RepositoryReader
from domain.info.entreprise_bussines.entities.info_dom import Info_dom
from frameworks.storage.postgres.models.info_model import Info_dal

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
        return self.impl.create_info(infoDal)

    def update(self, item, id):
        infoDal = self.fromDomToDal(item)
        filter = f"id = '{id}'"
        return self.impl.update_info(infoDal, filter)

    def delete(self, filters):
        filter = self.filterDomToDal(filters)

        if (filter == ''):
            raise ValueError('Any filter was included')
        
        rowsDeleted = self.impl.delete_info(filter)
        return rowsDeleted
    
    def fromDalToDom(self, itemDal):
        dom = Info_dom()
        dom.id = itemDal.id
        dom.departamento = itemDal.departamento
        dom.municipio = itemDal.municipio
        dom.puesto = itemDal.puesto
        dom.zona = itemDal.zona
        dom.mesa = itemDal.mesa
        dom.link = itemDal.link
        dom.votosGustavo = itemDal.votos_gustavo
        dom.votosIvan = itemDal.votos_ivan
        dom.votosBlanco = itemDal.votos_blanco
        dom.votosNulos = itemDal.votos_nulos
        dom.votosNoMarcados = itemDal.votos_no_marcados
        dom.votosTotal = itemDal.votos_total
        dom.votosSufragantes = itemDal.votos_sufragantes
        dom.votosUrna = itemDal.votos_urna
        dom.votosIncinerados = itemDal.votos_incinerados
        dom.validarTotal = itemDal.validar_total
        dom.validarVotantes = itemDal.validar_votantes
        return dom
    
    def fromDomToDal(self, itemDom):
        dal = Info_dal()
        dal.id = itemDom.id
        dal.departamento = itemDom.departamento
        dal.municipio = itemDom.municipio
        dal.puesto = itemDom.puesto
        dal.zona = itemDom.zona
        dal.mesa = itemDom.mesa
        dal.link = itemDom.link
        dal.votos_gustavo = itemDom.votosGustavo
        dal.votos_ivan = itemDom.votosIvan
        dal.votos_blanco = itemDom.votosBlanco
        dal.votos_nulos = itemDom.votosNulos
        dal.votos_no_marcados = itemDom.votosNoMarcados
        dal.votos_total = itemDom.votosTotal
        dal.votos_sufragantes = itemDom.votosSufragantes
        dal.votos_urna = itemDom.votosUrna
        dal.votos_incinerados = itemDom.votosIncinerados
        dal.validar_total = itemDom.validarTotal
        dal.validar_votantes = itemDom.validarVotantes
        return dal
    
    def filterDomToDal(self, itemArray):
        mapFilter = []
        for item in itemArray:
            mapFilter.append(f"{item} LIKE '{itemArray[item]}%'")

        condition = ' AND '.join(mapFilter)
        return condition

