from .response import Pagination
from typing import Optional, List
from pydantic import BaseModel

class ReservationBase(BaseModel):
    date_applied: str
    user_id: int

class Reservation(ReservationBase):
    id: int
    class Config:
        orm_mode = True

class ReservationList(Pagination):
    data: List[Reservation]
    class Config:
        orm_mode = True
