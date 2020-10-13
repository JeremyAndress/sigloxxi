from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from .rol import Rol
from .user import User
from .tables import Tables
from .reservation import Reservation, ReservationStatus
from .supplies import Supplies
