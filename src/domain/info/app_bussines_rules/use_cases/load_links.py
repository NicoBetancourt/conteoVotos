import requests
from bs4 import BeautifulSoup
import uuid

# Entities
from domain.info.entreprise_bussines.entities.info_dom import Info_dom


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

        arrayInfo = []

        # Itera cada uno de los departamentos
        for departamento in soupDepartamentos.findAll('a'):
            dpto = (departamento['id'][-2:]).replace('_', '0')
            infoMunicipios = getInfo(url, findMunicipios, dpto, '', '', '')
            soupDepartamentos = BeautifulSoup(infoMunicipios, "html.parser")

            # Itera cada uno de los municipios
            for municipio in soupDepartamentos.findAll('option'):
                mnpio = ('00'+municipio['value'])[-3:]
                infoZonas = getInfo(url, findZonas, dpto, mnpio, '', '')
                soupZonas = BeautifulSoup(infoZonas, "html.parser")

                # Itera cada uno de las zonas
                for zona in soupZonas.findAll('option'):
                    zon = ('0'+zona['value'])[-2:]
                    infoMesas = getInfo(url, findMesas, dpto, mnpio, zon, '')
                    soupMesas = BeautifulSoup(infoMesas, "html.parser")

                    # Itera cada uno de las mesas
                    for mesa in soupMesas.findAll('option'):
                        mes = ('0'+mesa['value'])[-2:]
                        infoLinks = getInfo(
                            url, findLinks, dpto, mnpio, zon, mes)
                        soupLinks = BeautifulSoup(infoLinks, "html.parser")

                        # Itera cada uno de los links
                        for link in soupLinks.findAll('a'):

                            info = Info_dom(str(uuid.uuid4(
                            )), departamento.text, municipio.text, mesa.text, zona.text, link.text, link['href'])

                            arrayInfo.append(info.to_List())

                            if len(arrayInfo) > 20000:
                                break

                        else:
                            continue
                        break
                    else:
                        continue
                    break
                else:
                    continue
                break
            else:
                continue
            break

        return arrayInfo
