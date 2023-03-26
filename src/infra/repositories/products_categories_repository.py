from typing import List

from src.infra.repositories.base_repository import BaseRepository
from src.domain.products_categories import ProductsCategories
from src.config import get_session


class ProductsCategoriesRepository(BaseRepository):
    def __init__(self):
        super().__init__(ProductsCategories)

    def list_by_store_id(self, store_id) -> List[ProductsCategories]:
        session = get_session()
        return session.query(self.entity).filter_by(store_id=store_id).all()
