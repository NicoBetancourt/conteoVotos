# from urllib import response
from flask import Blueprint
from domain.info.interface_adapters.web.controllers.info_controller import InfoController

link_route = Blueprint('link_routes', __name__)

@link_route.route('/')
def get_all():
    return InfoController.getAll()

@link_route.route('/<id>')
def get_one(id):
    return InfoController.getOne(id)

@link_route.route('/add', methods=['POST'])
def post_one():
    return InfoController.create()

@link_route.route('/<id>/update', methods=['PUT'])
def update(id):
    return InfoController.update(id)

@link_route.route('/', methods=['DELETE'])
def delete():
    return InfoController.delete()

@link_route.route('/load-links', methods=['POST'])
def load_info_links():
    return InfoController.loadInfo()
