from src.infra.repositories.base_repository import BaseRepository
from src.domain.users_info import UsersInfo

class UsersInfoRepository(BaseRepository):
    def __init__(self):
        super().__init__(UsersInfo)