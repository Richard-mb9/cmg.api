from src.config import Base

from sqlalchemy import Column, Integer, String, ForeignKey


class ProductsCategories(Base):
    __tablename__ = 'products_categories'

    store_id = Column(Integer, ForeignKey('stores.id'), nullable=False)
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __repr__(self): # pragma: no cover
        return f'Category {self.name}'