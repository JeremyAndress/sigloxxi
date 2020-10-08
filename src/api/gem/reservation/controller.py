from sqlalchemy.orm import Session
from sqlalchemy.sql import extract
from datetime import datetime
from utils.logging import logger
from utils.pagination import paginate
from schemas.reservation import ReservationBase, Reservation as Reservation_Update
from schemas.response import Response_SM
from models import Reservation, ReservationStatus
from api.gem.tables.controller import count_tables

def get_all_rsvt_status_cn(db:Session):
    return db.query(ReservationStatus).all()

def get_all_reservation_cn(page:int, db:Session):
    reservation = paginate(db.query(Reservation),page,10)
    return reservation

def get_reservation_day(date,db:Session):
    count = 0
    try:
        count = db.query(Reservation).filter(
            extract('day',Reservation.date_applied ) == date.day,
            extract('month',Reservation.date_applied ) == date.month,
            extract('year',Reservation.date_applied ) == date.year
        ).count()
    except Exception as e:
        logger.error(f'{e}')
    return count

def permission_reservation(day,db:Session):
    tables = count_tables(db) 
    res = get_reservation_day(day ,db)
    logger.info(f'tables count {tables} res count {res}')
    return tables - res

def create_reservation(rsvt: ReservationBase, db:Session):
    arsene = Response_SM(status = False, result = '...')
    try:
    
        prms = permission_reservation(rsvt.date_applied,db)
        if prms >= 1:
            reservation_data = Reservation(
                user_id = rsvt.user_id,
                date_applied = rsvt.date_applied,
                status_id = 1
            )
            db.add(reservation_data)
            db.commit()
            db.refresh(reservation_data)
            arsene.status = True if reservation_data.id else False
            arsene.result = 'success' if reservation_data else 'reservation cant create'
        else:
            arsene.result = 'Day without reservations available'
    except Exception as e:
        arsene.result = f'error {e}'
        logger.error(f'error {e}')
    return arsene

def update_reservation_cn(reservation: Reservation_Update, db: Session):
    arsene = Response_SM(status=False,result= '...')
    try:
        reservation_data = db.query(Reservation).filter(Reservation.id == reservation.id).update({
            Reservation.date_applied: reservation.date_applied,
            Reservation.status_id: reservation.status_id
        })
        db.commit()
        db.flush()
        arsene.status = True if reservation_data else False
        arsene.result = 'success' if reservation_data else 'reservation does not exist'
    except Exception as e:
        arsene.result = f'error {e}'
        logger.error(f'error {e}')
    return arsene

def delete_reservation_cn(id: int, db: Session):
    arsene = Response_SM(status = False, result= '...')
    try:
        reservation_delete = db.query(Reservation).filter(Reservation.id == id).delete()
        db.commit()
        db.flush()
        arsene.status = True if reservation_delete else False
        arsene.result = 'success' if reservation_delete else 'reservation does not exist'
    except Exception as e:
        arsene.result = f'error {e}'
        logger.error(f'error {e}')
    return arsene

