from typing import TypedDict, List

from src.utils.handlers import object_as_dict
from src.domain.invoices import Invoices
from src.domain.invoices_items import InvoicesItems
from src.infra.repositories.invoices_repository import InvoicesRepository
from src.infra.repositories.invoices_items_repository import InvoicesItemsRepository
from src.infra.repositories.tables_repository import TablesRepository
from src.services.products_service import ProductsService
from src.utils.errors import UnprocessableEntityError
from src.utils.errors import BadRequestError, NotFoundError


class AddItemsInInvoiceRequest(TypedDict):
    product_id: int
    quantity: int


class InvoiceService:
    def __init__(self):
        self.repository = InvoicesRepository()
        self.invoice_items_repository = InvoicesItemsRepository()
        self.table_repository = TablesRepository()

    def create(self, data):
        table = self.table_repository.find_by_table_name(
            data.get('table_name'))
        if table is None:
            NotFoundError('this table does not exist')
        if self.__table_with_invoice_opened(
                table_id=table.id, store_id=data.get('store_id')):
            raise BadRequestError('this table has an open order')
        table = self.table_repository.find_by_table_name(data['table_name'])
        invoice = Invoices(
            store_id=data.get('store_id'),
            table_id=table.id,
            price=0.0
        )
        result = self.repository.create(invoice)
        return {'id': result.id}

    def get_table_orders(self, table_id: int, store_id: int):
        return self.repository.get_table_orders(table_id=table_id, store_id=store_id)

    def __table_with_invoice_opened(self, table_id: int, store_id: int):
        invoices = object_as_dict(
            self.get_table_orders(table_id=table_id, store_id=store_id))
        return len(invoices) > 0

    def update(self, id, data_to_update):
        self.repository.update(id, data_to_update)

    def read_by_id(self, id) -> dict:
        result = self.repository.read_by_id(id)
        return object_as_dict(result)

    def list(self) -> list:
        return object_as_dict(self.repository.list())

    def list_by_store(self, store_id, params={}):
        return self.repository.get_store_orders(store_id, params)

    def delete(self, id):
        self.repository.delete(id)

    def __read_invoice_by_id(self, invoice_id) -> Invoices:
        return self.repository.read_by_id(invoice_id)

    def __get_products_prices(self, items: List[AddItemsInInvoiceRequest]):
        """
        recebe uma lista de produtos, e busca no banco de dados todos os dados destes produtos,
        depois cria uma um dicionario que como chaves tem os ids de cada produto, e como valor
        os preços unitarios destes produtos
        """
        products_ids = set()
        for item in items:
            products_ids.add(item['product_id'])
        products = ProductsService().batch_get_by_id(list(products_ids))
        products_prices = {}
        for product in products:
            products_prices[product.id] = product.price
        return products_prices

    def add_items(self, invoice_id, items: List[AddItemsInInvoiceRequest]):
        invoice = self.__read_invoice_by_id(invoice_id)
        if not invoice.opened:
            UnprocessableEntityError(
                "the invoice sent has already been closed")

        items_for_create = []
        products_prices = self.__get_products_prices(items)
        total_price = invoice.price
        for item in items:
            product_price = products_prices.get(item.get('product_id'))
            items_for_create.append(
                InvoicesItems(
                    invoice_id=int(invoice_id),
                    product_id=item.get('product_id'),
                    quantity=item.get('quantity'),
                    unity_price=product_price,
                    price=(product_price * item.get('quantity'))
                )
            )
            total_price += (product_price * item.get('quantity'))
        self.invoice_items_repository.batch_insert(items_for_create)
        self.repository.update(invoice_id, {'price': total_price})
        return {'price': total_price}

    def remove_items_from_invoice(self, order_id):
        invoice_item: InvoicesItems = self.invoice_items_repository.read_by_id(
            order_id)
        invoice: Invoices = self.repository.read_by_id(invoice_item.invoice_id)
        new_price = invoice.price - invoice_item.price
        self.repository.update(invoice.id, {'price': new_price})
        self.invoice_items_repository.delete(invoice_item.id)
        return {'new_invoice_price': new_price}
