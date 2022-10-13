class Info_dal():

    def __init__(self, id, departamento=None, municipio=None, zona=None, mesa=None, link=None, votos_gustavo=None, votos_ivan=None, votos_blanco=None, 
    votos_nulos=None, votos_no_marcados=None, votos_total=None, votos_sufragantes=None, votos_urna=None, votos_incinerados=None, validar_total=None, validar_votantes=None) -> None:
        self.id = id
        self.departamento = departamento
        self.municipio = municipio
        self.zona = zona
        self.mesa = mesa
        self.link = link
        self.votos_gustavo = votos_gustavo
        self.votos_ivan = votos_ivan
        self.votos_blanco = votos_blanco
        self.votos_nulos = votos_nulos
        self.votos_no_marcados = votos_no_marcados
        self.votos_total = votos_total
        self.votos_sufragantes = votos_sufragantes
        self.votos_urna = votos_urna
        self.votos_incinerados = votos_incinerados
        self.validar_total = validar_total
        self.validar_votantes = validar_votantes
        # pass

    def headers():
        return ['id', 
            'departamento',
            'municipio',
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
            'validar_totantes']