from typing import List, TypedDict
from src.domain.tables import Tables
from src.infra.repositories.base_repository import BaseRepository


class TablesByTableUserInResult(TypedDict):
    id: int
    table_user: str


class TablesRepository(BaseRepository):
    def __init__(self):
        super().__init__(Tables)

    def list_tables_by_table_users_in(self, table_list: List[Tables]) -> List[TablesByTableUserInResult]:
        table_names = [f"'{table.table_user}'" for table in table_list]
        query = f"""select id, table_user from "tables" where table_user  in ({','.join(table_names)})"""
        return self.execute_query(query)

    def list_tables_by_store_id(self, store_id: int):
        return self.filter_by(store_id=store_id).all()

    def find_by_table_name(self, table_name: str) -> Tables:
        return self.filter_by(table_name=table_name).first()
