from models import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

class Orders(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key = True)
    table_id = Column(Integer, ForeignKey("tables.id", ondelete = 'cascade'))
    status = Column(String)
    creation = Column(DateTime)
    tables = relationship("Tables")

class OrdersDetail(Base):
    __tablename__ = 'orders_detail'
    id = Column(Integer,primary_key = True)
    orders_id = Column(Integer, ForeignKey("orders.id", ondelete = 'cascade'))
    food_plate_id = Column(Integer, ForeignKey("food_plate.id", ondelete = 'cascade'))
    status = Column(String)
    quantity = Column(Integer)
    served = Column(DateTime)
    orders = relationship("Orders")
    food_plate = relationship("FoodPlate")

class OrdersCompleted(Base):
    __tablename__ = 'orders_completed'
    id = Column(Integer,primary_key = True)
    status = Column(String)
    creation = Column(DateTime)

class OrdersDetailCompleted(Base):
    __tablename__ = 'orders_detail_completed'
    id = Column(Integer,primary_key = True)
    orders_completed_id = Column(Integer, ForeignKey("orders_completed.id", ondelete = 'cascade'))
    food_plate_id = Column(Integer, ForeignKey("food_plate.id", ondelete = 'cascade'))
    quantity = Column(Integer)
    served = Column(DateTime)
    orders = relationship("OrdersCompleted")
    food_plate = relationship("FoodPlate")

