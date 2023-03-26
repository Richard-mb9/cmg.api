from flask import Blueprint
from flask import request, Response
from json import loads
from http import HTTPStatus
from flask import jsonify
from src.utils.security.security import login_required


from src.services.adresses_service import AdressesService
from src.utils.validator import validator
from .validators import create_and_update_addresses_validator


app = Blueprint('adresses', __name__)


@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'


@app.route('', methods=['POST'])
@login_required
def create_adress():
    data = loads(request.data)
    validator(create_and_update_addresses_validator, data)
    return jsonify(AdressesService().create(data)), HTTPStatus.CREATED


@app.route('', methods=['GET'])
@login_required
def list_adresses():
    return jsonify(AdressesService().list_by_user_id())


@app.route('/<adress_id>', methods=['GET'])
@login_required
def read_adress(adress_id):
    return jsonify(AdressesService().read_by_id(adress_id))


@app.route('/<adress_id>', methods=['PUT'])
@login_required
def update_adress(adress_id):
    data = loads(request.data)
    validator(create_and_update_addresses_validator, data)
    AdressesService().update(adress_id, data)
    return Response(status=HTTPStatus.NO_CONTENT)


@app.route('/<adress_id>', methods=['DELETE'])
@login_required
def delete_adress(adress_id):
    AdressesService().delete(adress_id)
    return Response(status=HTTPStatus.NO_CONTENT)
