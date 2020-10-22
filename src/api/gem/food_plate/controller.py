from datetime import datetime
from sqlalchemy.orm import Session
from utils.logging import logger
from utils.pagination import paginate
from schemas.food_plate import FoodPlateCreate
from schemas.response import Response_SM
from models import FoodPlate,SuppliesPlate,Supplies

def get_all_fp_cn(page:int,db:Session):
    fp  = paginate(db.query(FoodPlate),page,10)
    return fp

def create_fp_cn(food_plate: FoodPlateCreate, db:Session):
    arsene =  Response_SM(status=False,result= '...')
    try:
        fp_data = FoodPlate(
            name = food_plate.name,
            price = food_plate.price,
            creation = datetime.now()
        )
        db.add(fp_data)
        db.commit()
        db.refresh(fp_data)
        arsene.status = True if fp_data.id else False
        arsene.result = 'success'
        for sp in food_plate.supplies:
            if db.query(Supplies).filter(Supplies.id == sp.id).first():
                sp_date = SuppliesPlate(
                    quantity = sp.quantity,
                    food_plate_id = fp_data.id,
                    supplies_id = sp.id,
                )
                db.add(sp_date)
                db.commit()
                db.refresh(sp_date)
    except Exception as e:
        arsene.result = f'error {e}'
        logger.error(f'error {e}')
    return arsene