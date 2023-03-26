from flask import Blueprint
from json import loads
from http import HTTPStatus
from flask import request, Response, jsonify
from src.utils.security.security import roles_allowed

from src.services.tables_service import TablesService
from src.utils.validator import validator


from .validators import batch_create_tables_validator

app = Blueprint('tables', __name__)


@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'


@app.route('/create/batch', methods=['POST'])
def batch_create_table():
    data = loads(request.data)
    validator(batch_create_tables_validator, data)
    TablesService().batch_create(data)
    return Response(status=HTTPStatus.CREATED)


@app.route('/stores/<store_id>', methods=['GET'])
@roles_allowed('READ_TABLES')
def list_tables_by_store_id(store_id):
    return jsonify(TablesService().list_by_store_id(store_id))
