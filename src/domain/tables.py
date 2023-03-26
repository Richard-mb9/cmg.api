from src.config import Base

from sqlalchemy import Column, Integer, String, ForeignKey


class Tables(Base):
    __tablename__ = 'tables'

    id = Column(Integer, primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), nullable=False)
    table_name = Column(String, nullable=False)
    table_user = Column(String, nullable=False)
    table_password = Column(String, nullable=False)

    def __repr__(self):  # pragma: no cover
        return f'Table {self.table_name} for store {self.store_id}'
