from typing import List
import requests
from json import dumps

from src.config import CMG_AUTH_URL
from src.utils.security.security import get_token
from src.domain.tables import Tables


class CMGAuth:
    def __init__(self) -> None:
        pass

    def batch_create_table_users(self, tables: List[Tables]):
        headers = {
            'Authorization': f'Bearer {get_token()}'
        }

        for table in tables:
            requests.post(url=f'{CMG_AUTH_URL}/users', headers=headers, data=dumps({
                "email": table.table_user,
                "password": table.table_password,
                "profiles": ["TABLE"]
            }))
