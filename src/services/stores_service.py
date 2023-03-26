import os
from werkzeug.utils import secure_filename

from src.infra.repositories.stores_repository import StoresRepository
from src.domain.stores import Stores
from src.domain.adresses import Adresses
from src.domain.telephone import Telephones
from src.utils.security.security import get_user_id_in_token
from src.utils.handlers import object_as_dict
from src.utils.errors import BadRequestError, NotFoundError
from src.services.image_upload_service import ImageUploadService

from src.services.schemas.stores.create_and_update_store_request import CreateAndUpdateStoreRequest
from src.services.adresses_service import AdressesService
from src.services.telephones_service import TelephonesService
from src.services.products_service import ProductsService
from src.services.products_categories_service import ProductsCategoriesService


class StoresService:
    def __init__(self):
        self.repository = StoresRepository()
        self.user_id_logged = None

    def __get_user_id_logged(self):
        if self.user_id_logged is None:
            self.user_id_logged = get_user_id_in_token()
        return self.user_id_logged

    def create_and_update_store(self, data: CreateAndUpdateStoreRequest):
        user_id = self.__get_user_id_logged()
        store: Stores = self.repository.read_by_user_id(user_id)
        if store is None:
            return self.create(data)
        return self.update(store.id, data)

    def update(self, store_id: int, data: CreateAndUpdateStoreRequest):
        store_updated = self.repository.update(store_id, data)
        return object_as_dict(store_updated)

    def create(self, data: CreateAndUpdateStoreRequest):
        store = Stores(
            user_id=self.__get_user_id_logged(),
            name=data.get('name'),
            cnpj=data.get('cnpj'),
            corporate_name=data.get('corporate_name')
        )
        result = self.repository.create(store)
        return {'id': result.id, 'user_id': result.user_id}

    def create_and_update(self, data):
        user_id = self.__get_user_id_logged()
        store = self.repository.read_by_id(user_id)
        if store is not None:
            self.__update(data)
        return self.__create(data)

    def get_store_logged(self):
        store = self.repository.read_by_id(self.__get_user_id_logged())
        if store is None:
            return {}
        return object_as_dict(store)

    def read_by_user_id(self, id) -> dict:
        store = self.repository.read_by_user_id(id)
        if store is None:
            raise NotFoundError('Store not found')
        return object_as_dict(store)

    def update_image_store(self, store_id, image):
        if not image:
            BadRequestError('there was an error saving the image')
        path = ImageUploadService().save(image, store_id, 'store_images')
        store: Stores = self.repository.read_by_id(store_id)
        self.repository.update(store.id, {'image_url': path})
        return object_as_dict(store)

    def load_all_data_store_data_by_user_id(self, user_id):
        store = self.read_by_user_id(user_id)
        telephones = TelephonesService().list_by_user_id(user_id)
        addresses = AdressesService().list_by_user_id()
        products = ProductsService().list_by_store_id(store['id'])
        products_categories = ProductsCategoriesService(
        ).list_by_store_id(store['id'])

        return {
            'store': store,
            'telephones': telephones,
            'addresses': addresses,
            'products': products,
            'products_categories': products_categories,
        }

    def load_all_data_store_data_by_store_id(self, store_id):
        store: Stores = self.repository.read_by_id(store_id)
        telephones = TelephonesService().list_by_user_id(store.user_id)
        addresses = AdressesService().list_by_user_id(store.user_id)
        products = ProductsService().list_by_store_id(store.id)
        products_categories = ProductsCategoriesService(
        ).list_by_store_id(store.id)

        return {
            'store': object_as_dict(store),
            'telephones': telephones,
            'addresses': addresses,
            'products': products,
            'products_categories': products_categories,
        }
