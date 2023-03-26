from src.utils.security.security import get_user_id_in_token
from src.utils.handlers import object_as_dict

from src.infra.repositories.telephones_repository import TelephonesRepository
from src.domain.telephone import Telephones


class TelephonesService:
    def __init__(self):
        self.repository = TelephonesRepository()
        self.user_id_logged = None

    def __get_user_id_logged(self):
        if self.user_id_logged is None:
            self.user_id_logged = get_user_id_in_token()
        return self.user_id_logged

    def create(self, data):
        telphone = Telephones(
            user_id=self.__get_user_id_logged(),
            ddd=data.get('ddd'),
            number=data.get('number')
        )
        result = self.repository.create(telphone)
        return {'id': result.id}

    def list_by_user_id(self, user_id=None):
        user_id = self.__get_user_id_logged() if user_id is None else user_id
        result = self.repository.list_by_user_id(user_id)
        return object_as_dict(result)

    def read_by_id(self, id):
        result = self.repository.read_by_id(id)
        return object_as_dict(result)

    def update(self, telephone_id, data_to_update):
        self.repository.update(telephone_id, data_to_update)

    def delete(self, id):
        self.repository.delete(id)

    def batch_delete(self, ids: str):
        ids = ids.split(',')
        self.repository.batch_delete(ids)
