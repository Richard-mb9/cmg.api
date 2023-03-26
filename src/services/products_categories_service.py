from src.infra.repositories.products_repository import ProductsRepository
from src.utils.handlers import object_as_dict
from src.infra.repositories.products_categories_repository import ProductsCategoriesRepository
from src.domain.products_categories import ProductsCategories

from src.services.schemas.products_categories.create_product_category_request import CreateProductCategoryRequest
from src.services.schemas.products_categories.update_product_category_request import UpdateProductCategoryRequest
from src.utils.errors import BadRequestError


class ProductsCategoriesService:
    def __init__(self):
        self.repository = ProductsCategoriesRepository()

    def create(self, data: CreateProductCategoryRequest):
        category = ProductsCategories(
            name=data['name'],
            store_id=data['store_id']
        )
        result = self.repository.create(category)
        return {'id': result.id}

    def read_by_id(self, id) -> dict:
        result = self.repository.read_by_id(id)
        return object_as_dict(result)

    def update(self, id, data_to_update: UpdateProductCategoryRequest):
        self.repository.update(id, data_to_update)

    def list(self) -> list:
        return object_as_dict(self.repository.list())

    def list_by_store_id(self, store_id: int):
        return object_as_dict(self.repository.list_by_store_id(store_id))

    def delete(self, id):
        products_linked = ProductsRepository().list_by_product_category(id)
        if len(products_linked) > 0:
            BadRequestError("there are products linked to this category!")
        self.repository.delete(id)
