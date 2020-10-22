from typing import Optional, List
from pydantic import BaseModel,validator
from .response import Pagination
from datetime import datetime

class FoodPlateBase(BaseModel):
    name: str
    price: int
    
class SuppliesPlate(BaseModel):
    id: int
    quantity:int
    

class FoodPlateCreate(FoodPlateBase):
    supplies: List[SuppliesPlate]
    @validator('supplies')
    def supplies_null(cls, v):
        assert len(v) >= 1 ,'must contain 1 supplies' 
        return v

class FoodPlate(FoodPlateBase):
    id: int
    creation: datetime
    class Config:
        orm_mode = True

class FoodPlateList(Pagination):
    data: List[FoodPlate]
    class Config:
        orm_mode = True