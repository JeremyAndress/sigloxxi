from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.user import UserCreate
from db.session import get_db
from schemas.food_plate import FoodPlateList,FoodPlateCreate
from api.deps import get_admin_user,get_client_user,get_chef_user
from schemas.response import Response_SM
from .controller import get_all_fp_cn,create_fp_cn

router = APIRouter()

@router.get('/food_plates/get_all_food_plates/',response_model=FoodPlateList,tags=["admin","cliente"])
def get_all_food_plates(
    page:int,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_client_user)
):
    fp = get_all_fp_cn(page,db)
    return fp

@router.post("/food_plates/create_food_plates/", response_model = Response_SM,tags=["admin","cocina"])
def create_food_plates(
    food_plate: FoodPlateCreate, 
    db:Session = Depends(get_db),
    current_user: UserCreate = Depends(get_chef_user)
):
    response = create_fp_cn(food_plate,db)
    return response