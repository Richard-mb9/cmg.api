create_invoice_by_store_validator = {
    'table_name': {
        'type': 'string',
        'required': True
    }
}

add_item_in_invoice_validator = {
    'items': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'product_id': {
                    'type': 'integer',
                    'required': True
                },
                'quantity': {
                    'type': 'integer',
                    'required': True
                }
            }

        },
    }
}
