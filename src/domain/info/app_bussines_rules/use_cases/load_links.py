import requests
from bs4 import BeautifulSoup

class links():
    def load_all_links():

        url = 'https://elecciones1.registraduria.gov.co/e14_pre2_2018/e14'

        findDepartamentos = 'cargar_departamentos_barra'
        findMunicipios = 'cambiar_departamento'
        findZonas = 'cambiar_municipio'
        findMesas = 'cambiar_zona'
        findLinks = 'cargar_mesas'


        def getInfo(url, accion, dep, mun, zona, pues):
            body = dict(accion=accion,
                        dep_activo=dep,
                        mun_activo=mun,
                        zona_activo=zona,
                        pues_activo=pues)

            htmlText = requests.post(url, data=body).text
            return htmlText


        infoDepartamento = getInfo(url, findDepartamentos, '01', '', '', '')

        soupDepartamentos = BeautifulSoup(infoDepartamento, "html.parser")

        arrayDepartamentos = []
        arrayMunicipios = []
        arrayZonas = []
        arrayMesas = []
        arrayLinks = []

        # Itera cada uno de los departamentos
        for departamento in soupDepartamentos.findAll('a'):

            arrayDepartamentos.append(departamento.text)
            dpto = (departamento['id'][-2:]).replace('_', '0')
            infoMunicipios = getInfo(url, findMunicipios, dpto, '', '', '')
            soupDepartamentos = BeautifulSoup(infoMunicipios, "html.parser")

            print(departamento.text)

            # Itera cada uno de los municipios
            for municipio in soupDepartamentos.findAll('option'):
                arrayMunicipios.append(municipio.text)

                mnpio = ('00'+municipio['value'])[-3:]
                infoZonas = getInfo(url, findZonas, dpto, mnpio, '', '')
                soupZonas = BeautifulSoup(infoZonas, "html.parser")
                print(municipio.text)

                # Itera cada uno de las zonas
                for zona in soupZonas.findAll('option'):
                    arrayZonas.append(zona.text)
                    zon = ('0'+zona['value'])[-2:]
                    infoMesas = getInfo(url, findMesas, dpto, mnpio, zon, '')
                    soupMesas = BeautifulSoup(infoMesas, "html.parser")
                    print(zona.text)

                    # Itera cada uno de las mesas
                    for mesa in soupMesas.findAll('option'):
                        arrayZonas.append(mesa.text)
                        mes = ('0'+mesa['value'])[-2:]
                        infoLinks = getInfo(url, findLinks, dpto, mnpio, zon, mes)
                        soupLinks = BeautifulSoup(infoLinks, "html.parser")
                        print(mesa.text)

                        # Itera cada uno de los links
                        for link in soupLinks.findAll('a'):
                            arrayLinks.append(link['href'])
                            print(link['href'])
