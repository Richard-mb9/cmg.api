from typing import List
from src.services.image_upload_service import ImageUploadService
from src.utils.handlers import object_as_dict
from src.infra.repositories.products_repository import ProductsRepository
from src.infra.repositories.products_categories_repository import ProductsCategoriesRepository
from src.domain.products import Products
from src.domain.products_categories import ProductsCategories

from src.services.schemas.product.create_product_request import CreateProductRequest
from src.services.schemas.product.update_product_request import UpdateProductRequest


class ProductsService:
    def __init__(self):
        self.repository = ProductsRepository()

    def create(self, data: CreateProductRequest):
        products_categories = self.get_product_catagories(
            data['categories_ids']
        )
        product = Products(
            store_id=data['store_id'],
            image_url=data.get('image_url'),
            name=data['name'],
            price=data['price'],
            description=data.get('description'),
            available_store=data['available_store'],
            available_delivery=data['available_delivery'],
            categories=products_categories
        )
        result = self.repository.create(product)
        return {'id': result.id}

    def read_by_id(self, id: int):
        result = self.repository.read_by_id(id)
        return object_as_dict(result)

    def list_by_store_id(self, store_id: int):
        products = self.repository.list_by_store_id(store_id)
        products_formatted = []
        for product in products:
            product_formatted = object_as_dict(product)
            product_formatted['categories'] = [object_as_dict(
                product_category) for product_category in product.categories]
            products_formatted.append(product_formatted)
        return products_formatted

    def update(self, product_id, data_to_update: UpdateProductRequest):
        products_categories_ids = data_to_update.get('categories_ids')
        if products_categories_ids is not None:
            product = self.repository.read_by_id(product_id)
            products_categories = ProductsCategoriesRepository(
            ).read_by_id_in(products_categories_ids)
            self.repository.update_categories(product, products_categories)
            del data_to_update['categories_ids']
        self.repository.update(product_id, data_to_update)

    def delete(self, id: int):
        self.repository.delete(id)

    def batch_get_by_id(self, ids: List[int]) -> List[Products]:
        return self.repository.read_by_id_in(ids)

    def get_product_catagories(self, categories_ids: List[int]) -> List[ProductsCategories]:
        categories: List[ProductsCategories] = []
        for product_category_id in categories_ids:
            product_category = ProductsCategoriesRepository().read_by_id(product_category_id)
            if product_category is not None:
                categories.append(product_category)
        return categories

    def update_image_product(self, product_id, image):
        path = ImageUploadService().save(image, product_id, 'product_images')
        self.repository.update(product_id, {'image_url': path})
        return path
