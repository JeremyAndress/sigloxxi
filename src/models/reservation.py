from models import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

class Reservation(Base):
    __tablename__ = 'reservation'
    id = Column(Integer,primary_key = True)
    user_id = Column(Integer, ForeignKey( "user.id", ondelete = 'cascade'))
    date_applied = Column(DateTime)
    user = relationship("User")

