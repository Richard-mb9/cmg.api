from json import JSONDecodeError, loads
from flask import request
from sqlalchemy import inspect
import string
import random


def object_as_dict(obj):
    if isinstance(obj, list):
        items = []
        for item in obj:
            items.append(object_as_dict(item))
        return items
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


def get_items_to_querys_from_request():
    object = {}
    for key in request.args:
        object[key] = request.args[key]
    return object


def get_data_or_form():
    try:
        data = loads(request.data)
        return data
    except JSONDecodeError:
        if request.form:
            return dict(request.form)
        else:
            return {}


def generate_password(size):
    random_str = string.ascii_letters + string.digits + \
        string.ascii_uppercase + '!@#$%&*=?/:><'
    return ''.join(random.choice(random_str) for i in range(size))
