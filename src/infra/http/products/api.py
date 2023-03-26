from flask import Blueprint
from json import loads
from http import HTTPStatus
from src.utils.security.security import roles_allowed
from flask import request, Response, jsonify

from src.services.products_service import ProductsService
from src.utils.validator import validator
from src.utils.errors import BadRequestError

from .validators import create_product_validator
from .validators import update_product_validator

app = Blueprint('products', __name__)


@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'


@app.route('', methods=['POST'])
# @roles_allowed('CREATE_PRODUCT')
def create_product():
    data = loads(request.data)
    validator(create_product_validator, data)
    return ProductsService().create(data)


@app.route('/<product_id>/image', methods=['PUT'])
# @roles_allowed('UPDATE_PRODUCT')
def update_product_image(product_id: int):
    if 'image' not in request.files:
        BadRequestError('No file part')
    image = request.files['image']
    if image.filename == '':
        BadRequestError('No selected file')
    return jsonify({'image_url': ProductsService().update_image_product(product_id, image)}), HTTPStatus.OK


@app.route('/<product_id>', methods=['PUT'])
# @roles_allowed('UPDATE_PRODUCT')
def update_product(product_id: int):
    data = loads(request.data)
    validator(update_product_validator, data)
    ProductsService().update(product_id, data)
    return Response(status=HTTPStatus.NO_CONTENT)


@app.route('/<product_id>', methods=['GET'])
def read_product(product_id: int):
    return ProductsService().read_by_id(product_id)


@app.route('/<product_id>', methods=['DELETE'])
# @roles_allowed('DELETE_PRODUCT')
def delete_product(product_id: int):
    ProductsService().delete(product_id)
    return Response(status=HTTPStatus.OK)


@app.route('/stores/<store_id>', methods=['GET'])
def list_product_by_store(store_id: int):
    products = ProductsService().list_by_store_id(store_id)
    return jsonify(products)
