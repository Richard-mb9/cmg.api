from flask import Blueprint
from flask import request
from json import loads
from http import HTTPStatus
from flask import jsonify
from src.utils.security.security import login_required, roles_allowed
from src.utils.errors import BadRequestError

from src.services.stores_service import StoresService
from src.utils.validator import validator
from .validators import create_and_update_store_validator


app = Blueprint('stores', __name__)


@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'


@app.route('', methods=['POST'])
@login_required
def create_and_update_store():
    data = loads(request.data)
    validator(create_and_update_store_validator, data)
    return jsonify(StoresService().create_and_update_store(data)), HTTPStatus.CREATED


""" @app.route('/<store_id>', methods=['PUT'])
# @roles_allowed("UPDATE_STORE")
def update_store(store_id: int):
    data = loads(request.data)
    validator(create_and_update_store_validator, data)
    return jsonify(service.update(store_id, data)), HTTPStatus.OK """


@app.route('/<store_id>/image', methods=['PUT'])
# @roles_allowed("UPDATE_STORE")
def update_image_store(store_id: int):
    if 'image' not in request.files:
        BadRequestError('No file part')
    image = request.files['image']
    if image.filename == '':
        BadRequestError('No selected file')
    return jsonify(StoresService().update_image_store(store_id, image)), HTTPStatus.OK


@app.route('/user/<user_id>', methods=['GET'])
def read_by_user_id(user_id):
    store = StoresService().read_by_user_id(user_id)
    return jsonify(store)


@app.route('/user/<user_id>/all-data', methods=['GET'])
def read_all_data_by_user_id(user_id):
    store = StoresService().load_all_data_store_data_by_user_id(user_id)
    return jsonify(store)


@app.route('/<store_id>/all-data', methods=['GET'])
def read_all_data_by_store_id(store_id):
    store = StoresService().load_all_data_store_data_by_store_id(store_id)
    return jsonify(store)
