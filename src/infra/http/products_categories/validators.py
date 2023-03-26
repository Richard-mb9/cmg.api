create_product_category_validator = {
    'store_id': {
        'type': 'integer',
        'required': True
    },
    'name': {
        'type': 'string',
        'required': True
    }
}


update_product_category_validator = {
    'name': {
        'type': 'string',
        'required': True
    }
}