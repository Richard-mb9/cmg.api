from src.config import Base

from sqlalchemy import Column, Integer, String, ForeignKey


class Adresses(Base):
    __tablename__ = 'adresses'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    cep = Column(String, nullable=False)
    street = Column(String, nullable=False)
    number = Column(Integer, nullable=False)
    complement = Column(String)
    district = Column(String)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, default='BRASIL')

    def __repr__(self):  # pragma: no cover
        return f'User id {self.user_id}'
