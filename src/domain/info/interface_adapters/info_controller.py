
from flask import jsonify, request
from domain.info.app_bussines_rules.use_cases.load_links import links

import uuid
import json
# Entities
from domain.info.entreprise_bussines.entities.info_dom import Info_dom
# Models
from frameworks.storage.client.driver.driver_2 import psql_driver


class InfoController:
    def getById(id):
        try:
            info = psql_driver.get_one(id)
            if info != None:
                return jsonify(info)
            else:
                return jsonify({}), 404
        except Exception as ex:
            return jsonify({'message': str(ex)}), 500

    def getLinkById(id):
        try:
            info = psql_driver.get_one_link(id)
            if info != None:
                return jsonify(info)
            else:
                return jsonify({}), 404
        except Exception as ex:
            return jsonify({'message': str(ex)}), 500

    def getAll():
        try:
            info = psql_driver.get_all()
            return jsonify(info)
        except Exception as ex:
            return jsonify({'message': str(ex)}), 500

    def postOne():
        try:
            departamento = request.json['departamento']
            municipio = request.json['municipio']
            zona = request.json['zona']
            mesa = request.json['mesa']
            link = request.json['link']

            info = Info_dom(str(uuid.uuid4()), departamento,
                            municipio, zona, mesa, link)

            # infoList = json.loads(info)

            affected_rows = psql_driver.add_one(info.to_List())

            if affected_rows == 1:
                return jsonify(info.id)
            else:
                return jsonify({'message': 'Error on insert'}), 500

        except Exception as ex:
            return jsonify({'message': str(ex)}), 500

    def postLinks():
        try:

            dbLinks = links.load_all_links()
            # print(dbLinks)
            affected_rows = psql_driver.add_all(dbLinks)
            return f"{affected_rows} links were added to DB"

        except Exception as ex:
            return jsonify({'message': str(ex)}), 500
