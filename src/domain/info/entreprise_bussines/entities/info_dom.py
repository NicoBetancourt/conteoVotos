import uuid


class Info_dom():

    def __init__(self, info_dict=None) -> None:
        if info_dict is None:
            info_dict = {}  # In case no dictionary is provided

        self.id = info_dict.get('id', str(uuid.uuid4()))
        self.departamento = info_dict.get('departamento')
        self.municipio = info_dict.get('municipio')
        self.puesto = info_dict.get('puesto')
        self.zona = info_dict.get('zona')
        self.mesa = info_dict.get('mesa')
        self.link = info_dict.get('link')
        self.votosGustavo = info_dict.get('votosGustavo')
        self.votosIvan = info_dict.get('votosIvan')
        self.votosBlanco = info_dict.get('votosBlanco')
        self.votosNulos = info_dict.get('votosNulos')
        self.votosNoMarcados = info_dict.get('votosNoMarcados')
        self.votosTotal = info_dict.get('votosTotal')
        self.votosSufragantes = info_dict.get('votosSufragantes')
        self.votosUrna = info_dict.get('votosUrna')
        self.votosIncinerados = info_dict.get('votosIncinerados')
        self.validarTotal = info_dict.get('validarTotal')
        self.validarVotantes = info_dict.get('validarVotantes')
        # pass

    def to_JSON(self):
        return {
            'id': self.id,
            'departamento': self.departamento,
            'municipio': self.municipio,
            'puesto': self.puesto,
            'zona': self.zona,
            'mesa': self.mesa,
            'link': self.link,
            'votosGustavo': self.votosGustavo,
            'votosIvan': self.votosIvan,
            'votosBlanco': self.votosBlanco,
            'votosNulos': self.votosNulos,
            'votosNoMarcados': self.votosNoMarcados,
            'votosTotal': self.votosTotal,
            'votosSufragantes': self.votosSufragantes,
            'votosUrna': self.votosUrna,
            'votosIncinerados': self.votosIncinerados,
            'validarTotal': self.validarTotal,
            'validarVotantes': self.validarVotantes
        }

    def to_List(self):
        return [self.id,self.departamento,self.municipio,self.puesto,self.zona,self.mesa, self.link,self.votosGustavo,self.votosIvan,
            self.votosBlanco,self.votosNulos,self.votosNoMarcados,self.votosTotal,self.votosSufragantes,self.votosUrna,self.votosIncinerados,
            self.validarTotal,self.validarVotantes]
    
    def update_info(self, item):
        # self.id = item.id if item.id else self.id
        self.departamento = item.departamento if item.departamento else self.departamento
        self.municipio = item.municipio if item.municipio else self.municipio
        self.puesto = item.puesto if item.puesto else self.puesto
        self.zona = item.zona if item.zona else self.zona
        self.mesa = item.mesa if item.mesa else self.mesa
        self.link = item.link if item.link else self.link
        self.votosGustavo = item.votosGustavo if item.votosGustavo else self.votosGustavo
        self.votosIvan = item.votosIvan if item.votosIvan else self.votosIvan
        self.votosBlanco = item.votosBlanco if item.votosBlanco else self.votosBlanco
        self.votosNulos = item.votosNulos if item.votosNulos else self.votosNulos
        self.votosNoMarcados = item.votosNoMarcados if item.votosNoMarcados else self.votosNoMarcados
        self.votosTotal = item.votosTotal if item.votosTotal else self.votosTotal
        self.votosSufragantes = item.votosSufragantes if item.votosSufragantes else self.votosSufragantes
        self.votosUrna = item.votosUrna if item.votosUrna else self.votosUrna
        self.votosIncinerados = item.votosIncinerados if item.votosIncinerados else self.votosIncinerados
        self.validarTotal = item.validarTotal if item.validarTotal else self.validarTotal
        self.validarVotantes = item.validarVotantes if item.validarVotantes else self.validarVotantes

        return self

    
class MakeInfo:

    def __init__(self) -> None:
        pass       

    def execute(self, item_dict):
        newDom = Info_dom(item_dict)
        return self.validateData(newDom, item_dict)
    
    def validateData(self, item, data):

        item.id = data.id if data.id else str(uuid.uuid4())
        return item