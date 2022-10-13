class Info_dom():

    def __init__(self, id, departamento=None, municipio=None, zona=None, mesa=None, link=None, votosGustavo=None, votosIvan=None, votosBlanco=None, votosNulos=None, votosNoMarcados=None, votosTotal=None, votosSufragantes=None, votosUrna=None, votosIncinerados=None, validarTotal=None, validarVotantes=None) -> None:
        self.id = id
        self.departamento = departamento
        self.municipio = municipio
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
        return [self.id,self.departamento,self.municipio,self.zona,self.mesa, self.link,self.votosGustavo,self.votosIvan,
            self.votosBlanco,self.votosNulos,self.votosNoMarcados,self.votosTotal,self.votosSufragantes,self.votosUrna,self.votosIncinerados,
            self.validarTotal,self.validarVotantes]