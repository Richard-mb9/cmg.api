from src.config import Base

from sqlalchemy import Column, Integer,  ForeignKey, Boolean, Float


class InvoicesItems(Base):
    __tablename__ = 'invoices_items'

    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey('invoices.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unity_price = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    delivered = Column(Boolean, nullable=False, default=False)

    def __repr__(self):  # pragma: no cover
        return f'Invoices Items {self.id}'
