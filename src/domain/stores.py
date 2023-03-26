from src.config import Base

from sqlalchemy import Column, Integer, String


class Stores(Base):
    __tablename__ = 'stores'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    name = Column(String)
    corporate_name = Column(String)
    cnpj = Column(String)
    image_url = Column(String)
    description = Column(String)

    def __repr__(self):  # pragma: no cover
        return f'Store {self.corporate_name}'
