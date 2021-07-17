from sqlalchemy import Column, Integer, String
from sqlalchemy_serializer import SerializerMixin

from data.db.db_session import SQLAlchemyBase


class Car(SQLAlchemyBase):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    make = Column(String)
    model = Column(String)
    engine_info = Column(String)
    year = Column(Integer)
    price = Column(Integer)