from typing import List

from src.domain.tables import Tables
from src.infra.repositories.tables_repository import TablesRepository
from src.infra.repositories.stores_repository import StoresRepository
from src.infra.integrations.cmg_auth import CMGAuth
from src.utils.errors import BadRequestError

from src.utils.handlers import generate_password, object_as_dict
from .schemas.tables.batch_create_tables import BatchCreateTableRequest


class TablesService:
    def __init__(self):
        self.repository = TablesRepository()
        self.store_repository = StoresRepository()

    def batch_create(self, data: BatchCreateTableRequest):
        store_id = data['store_id']
        initial_range = data['initial_range']
        end_range = data['end_range']

        self.__verify_if_store_exists(store_id)

        tables = []
        for i in range(initial_range, (end_range + 1)):
            tables.append(self.create(
                store_id=store_id,
                table_name=f'{i}'
            ))
        tables = self.__remove_duplicate_tables(tables)
        CMGAuth().batch_create_table_users(tables)
        self.repository.batch_insert(tables)

    def create(self, store_id, table_name: str):
        return Tables(
            store_id=store_id,
            table_name=table_name,
            table_user=f'{table_name}_{store_id}@table.com',
            table_password=generate_password(10)
        )

    def list_by_store_id(self, store_id):
        self.__verify_if_store_exists(store_id)
        tables = self.repository.list_tables_by_store_id(store_id)
        return object_as_dict(tables)

    def __verify_if_store_exists(self, store_id):
        store = self.store_repository.read_by_id(store_id)
        if store is None:
            BadRequestError(f'there is no store with the id {store_id}')

    def __remove_duplicate_tables(self, tables: List[Tables]):
        tables_in_db = self.repository.list_tables_by_table_users_in(tables)
        if len(tables_in_db) == 0:
            return tables

        new_tables = []
        for table in tables:
            duplicate = False
            for table_in_db in tables_in_db:
                if table_in_db['table_user'] == table.table_user:
                    duplicate = True
                    continue
            if not duplicate:
                new_tables.append(table)

        return new_tables
