from models import Base
from sqlalchemy import Column, Integer,String

class Supplies(Base):
    __tablename__ = 'supplies'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    quantity = Column(Integer)
    modicum = Column(Integer)
    on_hold = Column(Integer)
