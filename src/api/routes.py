from fastapi import APIRouter
from .gem.user import user
from .gem.rol import rol
from .gem.reservation import reservation
from .gem.tables import tables

router = APIRouter()
router.include_router(user.router)
router.include_router(rol.router,tags=["admin"])
router.include_router(reservation.router)
router.include_router(tables.router)