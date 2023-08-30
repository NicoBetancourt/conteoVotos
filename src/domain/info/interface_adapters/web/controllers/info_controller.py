from flask import jsonify, request
from .base_controller import BaseController
from domain.info.app_bussines_rules.use_cases import create_link, delete_links, get_link, get_all_links

class InfoController(BaseController):

    @staticmethod
    def create():
        json = request.json
        response = create_link(json)
        return response

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
    def update():
        raise NotImplementedError()
    