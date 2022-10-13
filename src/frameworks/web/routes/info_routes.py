from urllib import response
from flask import Blueprint
from domain.info.interface_adapters.info_controller import InfoController

main = Blueprint('info_blueprint', __name__)


@main.route('/')
def get_all():
    value = InfoController.getAll()
    return value

@main.route('/<id>')
def get_one(id):
    return InfoController.getById(id)


@main.route('/add', methods=['POST'])
def post_one():
    return InfoController.postOne()

@main.route('/loadlinks', methods=['POST'])
def post_links():
    return InfoController.postLinks()
