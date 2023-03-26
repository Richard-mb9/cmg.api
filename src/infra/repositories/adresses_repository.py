from src.infra.repositories.base_repository import BaseRepository
from src.config import get_session
from src.domain.adresses import Adresses


class AdressesRepository(BaseRepository):
    def __init__(self):
        super().__init__(Adresses)

    def list_by_user_id(self, user_id):
        session = get_session()
        return session.query(self.entity).filter_by(user_id=user_id).all()
