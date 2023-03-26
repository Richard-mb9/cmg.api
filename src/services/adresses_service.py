from src.utils.security.security import get_user_id_in_token
from src.utils.handlers import object_as_dict

from src.infra.repositories.adresses_repository import AdressesRepository
from src.domain.adresses import Adresses


class AdressesService:
    def __init__(self):
        self.repository = AdressesRepository()
        self.user_id_logged = None

    def __get_user_id_logged(self):
        if self.user_id_logged is None:
            self.user_id_logged = get_user_id_in_token()
        return self.user_id_logged

    def create(self, data):
        adress = Adresses(
            user_id=self.__get_user_id_logged(),
            cep=data.get('cep'),
            number=data.get('number'),
            street=data.get('street'),
            complement=data.get('complement', None),
            city=data.get('city'),
            state=data.get('state'),
            district=data.get('district'),
            country=data.get('country', 'BRASIL')
        )
        result = self.repository.create(adress)
        return {'id': result.id}

    def list_by_user_id(self, user_id=None):
        user_id = self.__get_user_id_logged() if user_id is None else user_id
        result = self.repository.list_by_user_id(user_id)
        return object_as_dict(result)

    def read_by_id(self, id):
        result = self.repository.read_by_id(id)
        return object_as_dict(result)

    def update(self, address_id, data_to_update):
        self.repository.update(address_id, data_to_update)

    def delete(self, id):
        self.repository.delete(id)
