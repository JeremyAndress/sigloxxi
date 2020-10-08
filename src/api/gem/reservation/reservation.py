from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from db.session import get_db
from schemas.reservation import (
    ReservationStatus,
    ReservationBase,Reservation, ReservationList
)
from schemas.response import Response_SM
from schemas.user import UserCreate
from schemas.token import TokenUser
from core.security import create_access_token
from api.deps import get_admin_user, get_client_user
from .controller import (
    create_reservation as create_rsvt,
    get_all_reservation_cn, get_all_rsvt_status_cn,
    delete_reservation_cn, update_reservation_cn
)
router = APIRouter()

@router.post("/reservation/reservation_create/", response_model = Response_SM,tags=["admin","cliente"])
def reservation_create(
    rsvt: ReservationBase, 
    db:Session = Depends(get_db),
    current_user: UserCreate = Depends(get_client_user)
):
    '''La creacion de reserva se permite segun la cantidad de mesas disponibles'''
    response = create_rsvt(rsvt,db)
    return response

@router.get("/reservation/get_all_reservation/", response_model = ReservationList,tags=["admin"])
def get_all_reservation(
    page: int,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_admin_user)
):
    reservation = get_all_reservation_cn(page,db)
    return reservation

@router.get("/reservation/get_all_reservation_status/", response_model = List[ReservationStatus],tags=["admin","cliente"])
def get_all_reservation(
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_client_user)
):
    status = get_all_rsvt_status_cn(db)
    return status

@router.delete("/reservation/delete_reservation/", response_model = Response_SM)
def delete_reservation(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_admin_user)
):
    response = delete_reservation_cn(id, db)
    return response

@router.put("/reservation/update_reservation/", response_model = Response_SM,tags=["admin","cliente"])
def update_reservation(
    upd_rsvt: Reservation,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_client_user)
):
    response = update_reservation_cn(upd_rsvt, db)
    return response
