STATES = [
    'ACRE',
    'ALAGOAS',
    'AMAPA',
    'AMAZONAS',
    'BAHIA',
    'CEARA',
    'DISTRITO FEDERAL',
    'ESPIRITO SANTO',
    'GOIAS',
    'MARANHAO',
    'MATO GROSSO',
    'MATO GROSSO DO SUL',
    'MINAS GERAIS',
    'PARA',
    'PARAIBA',
    'PARANA',
    'PERNANBUCO',
    'PIAUI',
    'RIO DE JANEIRO',
    'RIO GRANDE DO NORTE',
    'RIO GRANDE DO SUL',
    'RONDONIA',
    'RORAIMA',
    'SANTA CATARINA',
    'SAO PAULO',
    'SERGIPE',
    'TOCANTINS'
]

create_and_update_addresses_validator = {
    'cep': {
        'type': 'string',
        'required': True
    },
    'number': {
        'type': 'string',
        'required': True
    },
    'street': {
        'type': 'string',
        'required': True
    },
    'complement': {
        'type': 'string',
        'required': True
    },
    'district': {
        'type': 'string'
    },
    'city': {
        'type': 'string',
        'required': True
    },
    'state': {
        'type': 'string',
        'required': True,
        'allowed': STATES
    },
    'country': {
        'type': 'string',
        'allowed': ['BRASIL']
    },
}
