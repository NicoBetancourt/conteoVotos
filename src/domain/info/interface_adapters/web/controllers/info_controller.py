from flask import jsonify, request
from .base_controller import BaseController
from domain.info.app_bussines_rules.use_cases import create_link, delete_links, get_link, get_all_links, update_link, load_links

class InfoController(BaseController):

    @staticmethod
    def create():
        try:
            json = request.json
            data = create_link(json)

            response = {
                "count": data,
            }
            return response
        except Exception as ex:
                    return jsonify({'Error message': str(ex)}), 500

    @staticmethod
    def getAll():
        try:
            params = request.args
            info_objects = get_all_links(params)
            data = [info_obj.to_JSON() for info_obj in info_objects]

            response = {
                "data": data,
                "count": len(data)
            }

            return response
        except Exception as ex:
            return jsonify({'Error message': str(ex)}), 500
    
    @staticmethod
    def getOne(id):
        try:
            response = get_link(id)
            return response.to_JSON()
        except Exception as ex:
            return jsonify({'Error message': str(ex)}), 500
    
    @staticmethod
    def delete():
        try:
            params = request.args
            info_deleted = delete_links(params)

            response = {
                "count": info_deleted
            }

            return response
        except Exception as ex:
            return jsonify({'Error message': str(ex)}), 500
    
    @staticmethod
    def update(id):
        try:
            json = request.json
            data = update_link(json, id)

            response = {
                "id": id,
                "info": data.to_JSON(),
            }
            return response
        except Exception as ex:
                    return jsonify({'Error message': str(ex)}), 500
        
    @staticmethod
    def loadInfo():
        try:
            params = request.args
            info_objects = load_links()
            data = [info_obj.to_JSON() for info_obj in info_objects]

            response = {
                "data": data,
                "count": len(data)
            }

            return response
        except Exception as ex:
            return jsonify({'Error message': str(ex)}), 500
    