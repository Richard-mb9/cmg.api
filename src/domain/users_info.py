from src.config import Base

from sqlalchemy import Column, Integer, String


class UsersInfo(Base):
    __tablename__ = 'users_info'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer,nullable=False)
    name = Column(String)
    cpf = Column(String)


    def __repr__(self): # pragma: no cover
        return f'User {self.name}'