class Info_dal():

    def __init__(self, info_dict=None):

        if info_dict is None:
            info_dict = {}

        self.id = info_dict.get('id')
        self.departamento = info_dict.get('departamento')
        self.municipio = info_dict.get('municipio')
        self.puesto = info_dict.get('puesto')
        self.zona = info_dict.get('zona')
        self.mesa = info_dict.get('mesa')
        self.link = info_dict.get('link')
        self.votos_gustavo = info_dict.get('votos_gustavo')
        self.votos_ivan = info_dict.get('votos_ivan')
        self.votos_blanco = info_dict.get('votos_blanco')
        self.votos_nulos = info_dict.get('votos_nulos')
        self.votos_no_marcados = info_dict.get('votos_no_marcados')
        self.votos_total = info_dict.get('votos_total')
        self.votos_sufragantes = info_dict.get('votos_sufragantes')
        self.votos_urna = info_dict.get('votos_urna')
        self.votos_incinerados = info_dict.get('votos_incinerados')
        self.validar_total = info_dict.get('validar_total')
        self.validar_votantes = info_dict.get('validar_votantes')

    def headers(self):
        return ['id', 
            'departamento',
            'municipio',
            'puesto', 
            'zona', 
            'mesa', 
            'link', 
            'votos_gustavo', 
            'votos_ivan', 
            'votos_blanco', 
            'votos_nulos',
            'votos_no_marcados', 
            'votos_total',
            'votos_sufragantes',
            'votos_urna',
            'votos_incinerados',
            'validar_total',
            'validar_votantes']
    
    def to_JSON(self):
        return {
            'id': self.id,
            'departamento': self.departamento,
            'municipio': self.municipio,
            'puesto': self.puesto,
            'zona': self.zona,
            'mesa': self.mesa,
            'link': self.link,
            'votos_gustavo': self.votos_gustavo,
            'votos_ivan': self.votos_ivan,
            'votos_blanco': self.votos_blanco,
            'votos_nulos': self.votos_nulos,
            'votos_no_marcados': self.votos_no_marcados,
            'votos_total': self.votos_total,
            'votos_sufragantes': self.votos_sufragantes,
            'votos_urna': self.votos_urna,
            'votos_incinerados': self.votos_incinerados,
            'validar_total': self.validar_total,
            'validar_votantes': self.validar_votantes
        }

    def to_List(self):
        return [self.id,self.departamento,self.municipio,self.puesto,self.zona,self.mesa, self.link,self.votos_gustavo,self.votos_ivan,
            self.votos_blanco,self.votos_nulos,self.votos_no_marcados,self.votos_total,self.votos_sufragantes,self.votos_urna,self.votos_incinerados,
            self.validar_total,self.validar_votantes]