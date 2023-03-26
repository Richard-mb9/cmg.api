from src.config import Base

from sqlalchemy import Column, Integer, String, ForeignKey


class Telephones(Base):
    __tablename__ = 'telephones'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    ddd = Column(String, nullable=False)
    number = Column(String, nullable=False)


    def __repr__(self): # pragma: no cover
        return f'User ({self.ddd}) {self.number}'