from sqlalchemy.orm import Session
from utils.logging import logger
from models import Tables

def count_tables(db:Session):
    count = db.query(Tables).count()
    return count
