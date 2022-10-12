from flask import Blueprint, jsonify, request
import uuid

from domain.info.app_bussines_rules.use_cases.load_links import links

# Entities
from domain.info.entreprise_bussines.entities.info_dom import Info_dom
# Models
from frameworks.storage.models.infoModel import InfoModel

main = Blueprint('info_blueprint', __name__)


@main.route('/')
def get_Info():
    try:
        info = InfoModel.get_AllInfo()
        return jsonify(info)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/<id>')
def get_info(id):
    try:
        info = InfoModel.get_Info(id)
        print(info)
        if info != None:
            return jsonify(info)
        else:
            return jsonify({}), 404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/add', methods=['POST'])
def post_info():
    try:
        departamento = request.json['departamento']
        municipio = request.json['municipio']
        zona = request.json['zona']
        mesa = request.json['mesa']
        link = request.json['link']

        info = Info_dom(str(uuid.uuid4()), departamento,
                        municipio, zona, mesa, link)

        affected_rows = InfoModel.post_Info(info)

        if affected_rows == 1:
            return jsonify(info.id)
        else:
            return jsonify({'message': 'Error on insert'}), 500

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


# @main.route('/loadLinks', methods=['POST'])
# def post_info():
#     try:
#         links.load_links()
#         print('prueba')

#     except Exception as ex:
#         return jsonify({'message': str(ex)}), 500
