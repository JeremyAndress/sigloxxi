from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.user import UserCreate
from db.session import get_db
from api.deps import get_admin_user
from schemas.response import Response_SM
from .controller import get_all_fp_cn

router = APIRouter()

@router.get('/get_all_food_plates/',tags=["admin","cocina"])
def get_all_food_plates(
    page:int,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_admin_user)
):
    fp = get_all_fp_cn(page,db)
    return fp