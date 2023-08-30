import uuid


class Info_dom():

    def __init__(self, id: None, departamento=None, municipio=None, puesto=None, zona=None, mesa=None, link=None, votosGustavo=None, votosIvan=None, votosBlanco=None, votosNulos=None, votosNoMarcados=None, votosTotal=None, votosSufragantes=None, votosUrna=None, votosIncinerados=None, validarTotal=None, validarVotantes=None) -> None:
        self.id = id if id else str(uuid.uuid4())
        self.departamento = departamento
        self.municipio = municipio
        self.puesto = puesto
        self.zona = zona
        self.mesa = mesa
        self.link = link
        self.votosGustavo = votosGustavo
        self.votosIvan = votosIvan
        self.votosBlanco = votosBlanco
        self.votosNulos = votosNulos
        self.votosNoMarcados = votosNoMarcados
        self.votosTotal = votosTotal
        self.votosSufragantes = votosSufragantes
        self.votosUrna = votosUrna
        self.votosIncinerados = votosIncinerados
        self.validarTotal = validarTotal
        self.validarVotantes = validarVotantes
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
    
    # def convert_json_to_Info_dom(json_data):
    #     new_info_dom = Info_dom(
    #         departamento=json_data['departamento'],
    #         municipio=json_data.get('municipio'),
    #         puesto=json_data.get('puesto'),
    #         zona=json_data.get('zona'),
    #         mesa=json_data.get('mesa'),
    #         link=json_data.get('link')
    # )
    # return new_info_dom

    
class MakeInfo:

    def __init__(self) -> None:
        pass

    def execute(self, item_dict):
        newDom = Info_dom(item_dict)
        return self.validateData(newDom, item_dict)
    
    def validateData(self, item, data):

        item.id = data.id if data.id else str(uuid.uuid4())
        return item