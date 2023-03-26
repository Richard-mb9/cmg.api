from src.infra.repositories.base_repository import BaseRepository
from src.domain.stores import Stores
from src.config import get_session


class StoresRepository(BaseRepository):
    def __init__(self):
        super().__init__(Stores)

    def read_by_user_id(self, user_id):
        session = get_session()
        return session.query(self.entity).filter_by(user_id=user_id).first()
