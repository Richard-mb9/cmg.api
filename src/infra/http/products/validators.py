create_product_validator = {
    'store_id': {
        'type': 'number',
        'required': True
    },
    'image_url': {
        'type': 'string',
    },
    'name': {
        'type': 'string',
        'required': True
    },
    'description': {
        'type': 'string'
    },
    'price': {
        'type': 'float',
        'required': True,
    },
    'available_store': {
        'type': 'boolean',
        'required': True
    },
    'available_delivery': {
        'type': 'boolean',
        'required': True
    },
    'categories_ids': {
        'type': 'list',
        'schema': {
            'type': 'number'
        },
        'required': True
    }
}

update_product_validator = {
    'image_url': {
        'type': 'string'
    },
    'name': {
        'type': 'string'
    },
    'description': {
        'type': 'string'
    },
    'price': {
        'type': 'float'
    },
    'available_store': {
        'type': 'boolean'
    },
    'available_delivery': {
        'type': 'boolean'
    },
    'categories_ids': {
        'type': 'list',
        'schema': {
            'type': 'number'
        }
    }
}
