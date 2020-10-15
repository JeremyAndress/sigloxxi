from sqlalchemy.orm import Session
from utils.logging import logger
from utils.pagination import paginate
from schemas.response import Response_SM
from models import FoodPlate

def get_all_fp_cn(page:int,db:Session):
    fp  = paginate(db.query(FoodPlate),page,10)
    return fp