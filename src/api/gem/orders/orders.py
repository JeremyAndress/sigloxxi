from sqlalchemy.orm import Session
from fastapi import (
    APIRouter, Depends, HTTPException,
    WebSocketDisconnect,WebSocket
)
from typing import List
from db.session import get_db
from schemas.orders import (
    OrdersBase, OrdersUpdate,
    OrdersDetailBase, OrdersDetailUpdate,
    OrdersCompletedBase, 
    OrdersCompletedUpdate,OrdersDetailCompletedUpdate,
    OrdersDetailCompletedBase, 
    OrdersDetailCompletedUpdate,
    OrderList,ListOrdersDetail,
    ListOrdersCompleted,ListOrdersDetailCompleted
)
from schemas.response import Response_SM
from schemas.user import UserCreate,UserList
from schemas.token import TokenUser
from core.security import create_access_token
from api.deps import get_admin_user, get_client_user
from .controller import (
    get_all_orders_cn, create_orders, update_orders_cn, delete_orders_cn,
    get_all_orders_detail_cn as get_orders_detail,
    create_orders_detail, update_orders_detail_cn,
    delete_orders_detail_cn,
    get_all_orders_completed_cn as get_orders_completed,
    create_orders_completed, update_orders_completed_cn,
    delete_orders_completed_cn,
    get_all_orders_detail_completed_cn as get_ords_detail_cmp,
    create_orders_detail_completed,
    update_orders_detail_completed_cn as upd_ords_detail_completed,
    delete_orders_detail_completed_cn as dlt_ords_detail_completed
)
router = APIRouter()
#var ws = new WebSocket("ws://localhost:8097/api/v1/ws");
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()
@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")

@router.get("/orders/get_all_orders/",response_model=OrderList,tags=["admin"])
def get_all_orders(
    page: int,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_admin_user)
):
    orders = get_all_orders_cn(page,db)
    return orders

@router.post("/orders/orders_create/", response_model = Response_SM,tags=["admin","cliente"])
def orders_create(
    order: OrdersBase, 
    db:Session = Depends(get_db),
    current_user: UserCreate = Depends(get_client_user)
):
    response = create_orders(order, db)
    return response

@router.delete("/orders/delete_orders/", response_model = Response_SM,tags=["admin","cliente"])
def delete_orders(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_client_user)
):
    response = delete_orders_cn(id, db)
    return response

@router.put("/orders/update_orders/", response_model = Response_SM,tags=["admin","cliente"])
def update_orders(
    order: OrdersUpdate,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_client_user)
):
    response = update_orders_cn(order, db)
    return response

###################
## ORDERS DETAIL ##
###################

@router.get("/orders_detail/get_all_orders_detail/", response_model = ListOrdersDetail,tags=["admin","cliente"])
def get_all_reservation(
        page: int,
        db: Session = Depends(get_db),
        current_user: UserCreate = Depends(get_client_user)
    ):
    response = get_orders_detail(page, db)
    return response

@router.post("/orders_detail/orders_detail_create/", response_model = Response_SM, tags = ["admin"])
def orders_detail_create(
        order: OrdersDetailBase, 
        db: Session = Depends(get_db),
        current_user: UserCreate = Depends(get_admin_user)
    ):
    response = create_orders_detail(order,db)
    return response

@router.put("/orders_detail/update_orders_detail/", response_model = Response_SM,tags=["admin"])
def update_detail(
    upd_detail: OrdersDetailUpdate,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_admin_user)
):
    response = update_orders_detail_cn(upd_detail, db)
    return response

@router.delete("/orders_detail/delete_orders_detail/", response_model = Response_SM, tags=["admin"])
def delete_detail(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_admin_user)
):
    response = delete_orders_detail_cn(id, db)
    return response

######################
## ORDERS COMPLETED ##
######################

@router.get("/orders_completed/get_all_orders_completed/", response_model = ListOrdersCompleted,tags=["admin","cliente"])
def get_all_orders_completed(
        page: int,
        db: Session = Depends(get_db),
        current_user: UserCreate = Depends(get_client_user)
    ):
    response = get_orders_completed(page, db)
    return response

@router.post("/orders_completed/orders_completed_create/", response_model = Response_SM, tags = ["admin"])
def orders_completed_create(
        order: OrdersCompletedBase, 
        db: Session = Depends(get_db),
        current_user: UserCreate = Depends(get_admin_user)
    ):
    response = create_orders_completed(order,db)
    return response

@router.put("/orders_completed/update_orders_completed/", response_model = Response_SM,tags=["admin"])
def update_completed(
    upd_completed: OrdersCompletedUpdate,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_admin_user)
):
    response = update_orders_completed_cn(upd_completed, db)
    return response

@router.delete("/orders_completed/delete_orders_completed/", response_model = Response_SM, tags=["admin"])
def delete_completed(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_admin_user)
):
    response = delete_orders_completed_cn(id, db)
    return response

#############################
## ORDERS DETAIL COMPLETED ##
#############################

@router.get("/orders_detail_completed/get_all_orders_detail_completed/", response_model = ListOrdersDetailCompleted,tags=["admin","cliente"])
def get_all_orders_detail_completed(
        page: int,
        db: Session = Depends(get_db),
        current_user: UserCreate = Depends(get_client_user)
    ):
    response = get_ords_detail_cmp(page, db)
    return response

@router.post("/orders_detail_completed/orders_detail_completed_create/", response_model = Response_SM, tags = ["admin"])
def deteil_completed_create(
        order: OrdersDetailCompletedBase, 
        db: Session = Depends(get_db),
        current_user: UserCreate = Depends(get_admin_user)
    ):
    response = create_orders_detail_completed(order,db)
    return response

@router.put("/orders_detail_completed/update_orders_detail_completed/", response_model = Response_SM,tags=["admin"])
def update_detail_completed(
    upd_detail_completed: OrdersDetailCompletedUpdate,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_admin_user)
):
    response = upd_ords_detail_completed(upd_detail_completed, db)
    return response

@router.delete("/orders_detail_completed/delete_orders_detail_completed/", response_model = Response_SM, tags=["admin"])
def delete_completed(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_admin_user)
):
    response = dlt_ords_detail_completed(id, db)
    return response
