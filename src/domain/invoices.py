from src.config import Base

from sqlalchemy import Column, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class Invoices(Base):
    __tablename__ = 'invoices'

    id = Column(Integer, primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), nullable=False)
    table_id = Column(Integer, ForeignKey('tables.id'), nullable=False)
    opened = Column(Boolean, default=True)
    price = Column(Float, nullable=False)
    invoices_items = relationship('InvoicesItems')

    def __repr__(self):  # pragma: no cover
        return f'Invoice {self.id}'
