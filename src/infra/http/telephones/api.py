from flask import Blueprint
from flask import request, Response
from json import loads
from http import HTTPStatus
from flask import jsonify
from src.utils.security.security import login_required
from src.utils.handlers import get_items_to_querys_from_request
from src.utils.errors import BadRequestError


from src.services.telephones_service import TelephonesService
from src.utils.validator import validator
from .validators import create_and_update_telephone_validator

app = Blueprint('telephones', __name__)


@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'


@app.route('', methods=['POST'])
@login_required
def create_telephone():
    data = loads(request.data)
    validator(create_and_update_telephone_validator, data)
    return jsonify(TelephonesService().create(data)), HTTPStatus.CREATED


@app.route('', methods=['GET'])
@login_required
def list_telephones():
    return jsonify(TelephonesService().list_by_user_id())


@app.route('/<telephone_id>', methods=['GET'])
@login_required
def read_telephone(telephone_id):
    return jsonify(TelephonesService().read_by_id(telephone_id))


@app.route('/<telephone_id>', methods=['PUT'])
@login_required
def update_telephone(telephone_id):
    data = loads(request.data)
    validator(create_and_update_telephone_validator, data)
    TelephonesService().update(telephone_id, data)
    return Response(status=HTTPStatus.NO_CONTENT)


@app.route('/<telephone_id>', methods=['DELETE'])
@login_required
def delete_telephone(telephone_id):
    TelephonesService().delete(telephone_id)
    return Response(status=HTTPStatus.NO_CONTENT)


@app.route('/batch', methods=['DELETE'])
@login_required
def batch_delete_telephone():
    params = get_items_to_querys_from_request()
    ids = params.get('ids')
    if ids is None:
        raise BadRequestError("need to send the ids")
    TelephonesService().batch_delete(params['ids'])
    return Response(status=HTTPStatus.NO_CONTENT)
