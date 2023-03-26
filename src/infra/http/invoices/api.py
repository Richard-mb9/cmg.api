
from flask import Blueprint
from flask import request
from json import loads
from http import HTTPStatus
from flask import jsonify
from src.utils.security.security import login_required
from src.utils.validator import validator


from src.services.invoices_service import InvoiceService

from .validators import create_invoice_by_store_validator
from .validators import add_item_in_invoice_validator


app = Blueprint('invoices', __name__)


@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'


@app.route('/stores/<store_id>', methods=['POST'])
@login_required
def create_invoice_by_store(store_id: int):
    data = loads(request.data)
    validator(create_invoice_by_store_validator, data)
    payload = {**data, 'store_id': store_id}
    return jsonify(InvoiceService().create(payload)), HTTPStatus.CREATED


@app.route('/stores/<store_id>', methods=['GET'])
def list_invoices_by_store(store_id: int):
    params = request.args.to_dict()
    return jsonify(InvoiceService().list_by_store(store_id, params))


@app.route('/<invoice_id>/items', methods=['POST'])
# @login_required
def add_item_in_invoice(invoice_id: int):
    data = loads(request.data)
    validator(add_item_in_invoice_validator, data)
    return jsonify(InvoiceService().add_items(invoice_id, data['items']))


@app.route('/items/<order_id>', methods=['DELETE'])
@login_required
def remove_item_from_invoice(order_id: int):
    return jsonify(InvoiceService().remove_items_from_invoice(order_id))
