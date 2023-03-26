from src.infra.repositories.base_repository import BaseRepository
from src.domain.invoices import Invoices


class InvoicesRepository(BaseRepository):
    def __init__(self):
        super().__init__(Invoices)

    def get_table_orders(self, table_id: int, store_id: int):
        return self.session.query(self.entity).filter_by(
            table_id=table_id).filter_by(store_id=store_id).all()

    def get_store_orders(self, store_id: int, params: dict = {}):
        invoice_id = params.get('invoiceId', 'null')
        table_name = params.get('tableName', 'null')
        query = f"""
            select
                i.id,
                i.opened,
                i.price,
                i.store_id,
                t.table_name,
                i.price as total_price,
                ii.id as order_id,
                ii.product_id,
                p.name as product_name,
	            p.image_url as product_image_url,
                ii.quantity,
                ii.unity_price,
                ii.price,
                ii.delivered
            from invoices i
            inner join invoices_items ii on ii.invoice_id = i.id
            inner join tables t on t.id = i.table_id
            inner join products p on p.id = ii.product_id
            where 
                i.store_id = {store_id}
                and ({invoice_id} is null or i.id = {invoice_id})
                and ({table_name} is null or t.table_name = '{table_name}')
        """
        results = self.execute_query(query)
        separate_result_by_invoice_id = {}
        for result in results:
            if not str(result['id']) in separate_result_by_invoice_id:
                separate_result_by_invoice_id[str(result['id'])] = [result]
            else:
                separate_result_by_invoice_id[str(result['id'])].append(result)

        invoices = []

        for invoice_id in separate_result_by_invoice_id:
            invoice = separate_result_by_invoice_id[invoice_id]
            invoices.append({
                'id': invoice[0]['id'],
                'opened': invoice[0]['opened'],
                'price': invoice[0]['price'],
                'store_id': invoice[0]['store_id'],
                'table_name': invoice[0]['table_name'],
                'total': invoice[0]['total_price'],
                'items': [
                    {
                        'order_id': item['order_id'],
                        'product_id': item['product_id'],
                        'quantity': item['quantity'],
                        'unity_price': item['unity_price'],
                        'price': item['price'],
                        'delivered': item['delivered'],
                        'product_name': item['product_name'],
                        'product_image_url': item['product_image_url']
                    } for item in invoice
                ]
            })

        return invoices


""" {
'id': result[0]['id'],
'opened': result[0]['opened'],
'price': result[0]['price'],
'store_id': result[0]['store_id'],
'table_name': result[0]['table_name'],
'total': result[0]['total_price'],
'items': [
    {
        'product_id': item['product_id'],
        'quantity': item['quantity'],
        'unity_price': item['unity_price'],
        'price': item['price'],
        'delivered': item['delivered']
    } for item in result
]
} """
