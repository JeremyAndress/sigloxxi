from typing import Optional, List
from pydantic import BaseModel
from .response import Pagination

class TablesBase(BaseModel):
    id: int
    number: int 
    status: bool 
    user_id: int
    class Config:
        orm_mode = True

