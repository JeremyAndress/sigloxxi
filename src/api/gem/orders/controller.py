from sqlalchemy.orm import Session
from sqlalchemy.sql import extract
from datetime import datetime
from utils.logging import logger
from utils.pagination import paginate
from schemas.user import UserList
from schemas.response import Response_SM
from schemas.orders import (
    OrdersBase, OrdersUpdate,
    OrdersDetailBase, OrdersDetailUpdate,
    OrdersCompletedBase, OrdersCompletedUpdate,
    OrdersDetailCompletedBase, OrdersDetailCompletedUpdate
)
from models import (
    Orders, OrdersDetail,OrdersCompleted,
    OrdersDetailCompleted
)

from api.gem.tables.controller import count_tables

def get_all_orders_cn(page:int, db:Session):
    orders = paginate(db.query(Orders),page,10)
    return orders 

def create_orders(order: OrdersBase, db:Session):
    arsene = Response_SM(status = False, result = '...')
    try:
        orders_data = Orders(
            table_id = order.table_id,
            status = order.status,
            creation = order.creation
        )
        db.add(orders_data)
        db.commit()
        db.refresh(orders_data)
        arsene.status = True if orders_data.id else False
        arsene.result = 'success' if orders_data else 'order cant create'
    except Exception as e:
        arsene.result = f'error {e}'
        logger.error(f'error {e}')
    return arsene

def update_orders_cn(order: OrdersUpdate, db: Session):
    arsene = Response_SM(status = False, result = '...')
    try:
        order_data = db.query(Orders).filter(Orders.id == order.id).update({
            Orders.table_id: order.table_id,
            Orders.status: order.status,
            Orders.creation: order.creation
        })
        db.commit()
        db.flush()
        arsene.status = True if order_data else False
        arsene.result = 'success' if order_data else 'order does not exist'
    except Exception as e:
        arsene.result = f'error {e}'
        logger.error(f'error {e}')
    return arsene

def delete_orders_cn(id: int, db: Session):
    arsene = Response_SM(status = False, result= '...')
    try:
        orders_delete = db.query(Orders).filter(Orders.id == id).delete()
        db.commit()
        db.flush()
        arsene.status = True if orders_delete else False
        arsene.result = 'success' if orders_delete else 'order does not exist'
    except Exception as e:
        arsene.result = f'error {e}'
        logger.error(f'error {e}')
    return arsene

###################
## ORDERS DETAIL ##
###################

def get_all_orders_detail_cn(page: int, db: Session):
    detail = paginate(db.query(OrdersDetail),page,10)
    return detail 

def create_orders_detail(detail: OrdersDetailBase, db:Session):
    arsene = Response_SM(status = False, result = '...')
    try:
        detail_data = OrdersDetail(
            orders_id = detail.orders_id,
            food_plate_id = detail.food_plate_id,
            status = detail.status,
            quantity = detail.quantity,
            served = detail.served
        )
        db.add(detail_data)
        db.commit()
        db.refresh(detail_data)
        arsene.status = True if detail_data.id else False
        arsene.result = 'success' if detail_data else 'order detail cant create'
    except Exception as e:
        arsene.result = f'error {e}'
        logger.error(f'error {e}')
    return arsene

def update_orders_detail_cn(detail: OrdersDetailUpdate, db: Session):
    arsene = Response_SM(status = False, result = '...')
    try:
        detail_update = db.query(OrdersDetail).filter(OrdersDetail.id == detail.id).update({
            OrdersDetail.orders_id: detail.orders_id,
            OrdersDetail.food_plate_id: detail.food_plate_id,
            OrdersDetail.status: detail.status,
            OrdersDetail.quantity: detail.quantity,
            OrdersDetail.served: detail.served
        })
        db.commit()
        db.flush()
        arsene.status = True if detail_update else False
        arsene.result = 'success' if detail_update else 'order detail does not exist'
    except Exception as e:
        arsene.result = f'error {e}'
        logger.error(f'error {e}')
    return arsene

def delete_orders_detail_cn(id: int, db: Session):
    arsene = Response_SM(status = False, result= '...')
    try:
        detail_data = db.query(OrdersDetail).filter(OrdersDetail.id == id).delete()
        db.commit()
        db.flush()
        arsene.status = True if detail_data else False
        arsene.result = 'success' if detail_data else 'order detail does not exist'
    except Exception as e:
        arsene.result = f'error {e}'
        logger.error(f'error {e}')
    return arsene

######################
## ORDERS COMPLETED ##
######################

def get_all_orders_completed_cn(page: int, db: Session):
    completed = paginate(db.query(OrdersCompleted),page,10)
    return completed 

def create_orders_completed(completed: OrdersCompletedBase, db:Session):
    arsene = Response_SM(status = False, result = '...')
    try:
        completed_data = OrdersCompleted(
            status = completed.status,
            creation = completed.creation
        )
        db.add(completed_data)
        db.commit()
        db.refresh(completed_data)
        arsene.status = True if completed_data.id else False
        arsene.result = 'success' if completed_data else 'order completed cant create'
    except Exception as e:
        arsene.result = f'error {e}'
        logger.error(f'error {e}')
    return arsene

def update_orders_completed_cn(completed: OrdersCompletedUpdate, db: Session):
    arsene = Response_SM(status = False, result = '...')
    try:
        completed_data = db.query(OrdersCompleted).filter(OrdersCompleted.id == completed.id).update({
            OrdersCompleted.status: completed.status,
            OrdersCompleted.creation: completed.creation
        })
        db.commit()
        db.flush()
        arsene.status = True if completed_data else False
        arsene.result = 'success' if completed_data else 'order completed does not exist'
    except Exception as e:
        arsene.result = f'error {e}'
        logger.error(f'error {e}')
    return arsene

def delete_orders_completed_cn(id: int, db: Session):
    arsene = Response_SM(status = False, result= '...')
    try:
        completed_delete = db.query(OrdersCompleted).filter(OrdersCompleted.id == id).delete()
        db.commit()
        db.flush()
        arsene.status = True if completed_delete else False
        arsene.result = 'success' if completed_delete else 'order completed does not exist'
    except Exception as e:
        arsene.result = f'error {e}'
        logger.error(f'error {e}')
    return arsene

#############################
## ORDERS DETAIL COMPLETED ##
#############################

def get_all_orders_detail_completed_cn(page: int, db: Session):
    detail_completed = paginate(db.query(OrdersDetailCompleted),page,10)
    return detail_completed 

def create_orders_detail_completed(detail_completed: OrdersDetailCompletedBase, db:Session):
    arsene = Response_SM(status = False, result = '...')
    try:
        detail_completed_data = OrdersDetailCompleted(
            orders_id = detail_completed.orders_id,
            food_plate_id = detail_completed.food_plate_id,
            quantity = detail_completed.quantity,
            served = detail_completed.served
        )
        db.add(detail_completed_data)
        db.commit()
        db.refresh(detail_completed_data)
        arsene.status = True if detail_completed_data.id else False
        arsene.result = 'success' if detail_completed_data else 'order detail completed cant create'
    except Exception as e:
        arsene.result = f'error {e}'
        logger.error(f'error {e}')
    return arsene

def update_orders_detail_completed_cn(detail_completed: OrdersDetailCompletedUpdate, db: Session):
    arsene = Response_SM(status = False, result = '...')
    try:
        detail_completed_data = db.query(OrdersDetailCompleted).filter(OrdersDetailCompleted.id == detail_completed.id).update({
            OrdersDetailCompleted.orders_id: detail_completed.orders_id,
            OrdersDetailCompleted.food_plate_id: detail_completed.food_plate_id,
            OrdersDetailCompleted.quantity: detail_completed.quantity,
            OrdersDetailCompleted.served: detail_completed.served
        })
        db.commit()
        db.flush()
        arsene.status = True if detail_completed_data else False
        arsene.result = 'success' if detail_completed_data else 'order detail completed does not exist'
    except Exception as e:
        arsene.result = f'error {e}'
        logger.error(f'error {e}')
    return arsene

def delete_orders_detail_completed_cn(id: int, db: Session):
    arsene = Response_SM(status = False, result= '...')
    try:
        detail_completed_delete = db.query(OrdersDetailCompleted).filter(OrdersDetailCompleted.id == id).delete()
        db.commit()
        db.flush()
        arsene.status = True if detail_completed_delete else False
        arsene.result = 'success' if detail_completed_delete else 'order detail completed does not exist'
    except Exception as e:
        arsene.result = f'error {e}'
        logger.error(f'error {e}')
    return arsene
