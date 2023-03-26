from typing import List
from src.domain.products_categories import ProductsCategories
from src.domain.products import Products
from src.infra.repositories.base_repository import BaseRepository
from src.config import get_session


class ProductsRepository(BaseRepository):
    def __init__(self):
        super().__init__(Products)

    def list_by_store_id(self, store_id) -> List[Products]:
        session = get_session()
        return session.query(self.entity).filter_by(store_id=store_id).all()

    def update_categories(self, product: Products, product_categories: List[ProductsCategories]):
        session = get_session()
        product.categories = product_categories
        session.commit()

    def list_by_product_category(self, category_id):
        session = get_session()
        result = session.execute(
            "select id, store_id, image_url, name, price, available_delivery , available_store, description\n"
            + "from products p\n"
            + "inner join products_categories_products pcp on pcp.product_id = p.id\n"
            + f"where pcp.category_id = {category_id}"
        )
        return self.format_search_query(result)
