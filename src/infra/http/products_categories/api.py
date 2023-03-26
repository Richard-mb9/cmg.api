from flask import Blueprint
from flask import request, Response
from json import loads
from http import HTTPStatus
from flask import jsonify

from src.utils.security.security import login_required, roles_allowed
from src.utils.validator import validator

from src.services.products_categories_service import ProductsCategoriesService

from .validators import create_product_category_validator
from .validators import update_product_category_validator

app = Blueprint('products_categories', __name__)


@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'


@app.route('', methods=['POST'])
# @roles_allowed("CREATE_PRODUCT_CATEGORY")
def create_product_category():
    data = loads(request.data)
    validator(create_product_category_validator, data)
    result = ProductsCategoriesService().create(data)
    return jsonify(result), HTTPStatus.CREATED


@app.route('/<category_id>', methods=['PUT'])
# @roles_allowed("UPDATE_PRODUCT_CATEGORY")
def update_product_category(category_id: int):
    data = loads(request.data)
    validator(update_product_category_validator, data)
    ProductsCategoriesService().update(category_id, data)
    return Response(status=HTTPStatus.NO_CONTENT)


@app.route('/<category_id>', methods=['GET'])
def read_product_category(category_id: int):
    category = ProductsCategoriesService().read_by_id(category_id)
    return jsonify(category)


@app.route('/stores/<store_id>', methods=['GET'])
def list_products_categories_by_store_id(store_id: int):
    categories = ProductsCategoriesService().list_by_store_id(store_id)
    return jsonify(categories)


@app.route('/<category_id>', methods=['DELETE'])
# @roles_allowed("DELETE_PRODUCT_CATEGORY")
def delete_product_category(category_id: int):
    ProductsCategoriesService().delete(category_id)
    return Response(status=HTTPStatus.NO_CONTENT)
