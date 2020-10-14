from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class OrdersBase(BaseModel):
    table_id: int
    status: str
    creation: datetime

class OrdersUpdate(OrdersBase):
    id: int
    class Config:
        orm_mode = True

class OrdersDetailBase(BaseModel):
    orders_id: int
    food_plate_id: int
    status: str
    quantity: int
    served: datetime

class OrdersDetailUpdate(OrdersDetailBase):
    id: int
    class Config:
        orm_mode = True

class OrdersCompletedBase(BaseModel):
    status: str
    creation: datetime

class OrdersCompletedUpdate(OrdersCompletedBase):
    id: int
    class Config:
        orm_mode = True

class OrdersDetailCompletedBase(BaseModel):
    orders_completed_id: int
    food_plate_id: int
    quantity: int
    served: datetime

class OrdersDetailCompletedUpdate(OrdersDetailCompletedBase):
    id: int
    class Config:
        orm_mode = True
