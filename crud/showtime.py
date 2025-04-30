from sqlalchemy.orm import Session
from models import Showtime
from schemas import ShowtimeCreate
from datetime import datetime

async def create_showtime(db: Session, showtime: ShowtimeCreate, end_time: str):
    print(showtime.model_dump())
    db_showtime = Showtime(**showtime.model_dump(), end_time=end_time)
    db.add(db_showtime)
    db.commit()
    db.refresh(db_showtime)
    return db_showtime

async def get_movie_active_showtimes(db: Session, movie_name: str, skip: int = 0, limit: int = 100):
    actual_date = datetime.now()
    return db.query(Showtime).filter(Showtime.start_time > actual_date, Showtime.movie_name == movie_name).offset(skip).limit(limit).all()

async def get_showtime(db: Session, showtime_id: str):
    return db.query(Showtime).filter(Showtime.id == showtime_id).first()

async def delete_showtime(db: Session, showtime_id: str):
    db_showtime = db.query(Showtime).filter(Showtime.id == showtime_id).first()
    db.delete(db_showtime)
    db.commit()
    return db_showtime

async def register_reservation_showtime(db: Session, showtime_id: str, tickets: int): 
    db_showtime = db.query(Showtime).filter(Showtime.id == showtime_id).first()
    result = db_showtime.avaible_tickets - tickets
    if result < 0:
        return None
    db_showtime.avaible_tickets = result
    db.commit()
    db.refresh(db_showtime)
    return db_showtime

def get_showtimes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Showtime).offset(skip).limit(limit).all()

def get_showtimes_date(db: Session, date: str, skip: int = 0, limit: int = 100):
    return db.query(Showtime).filter(Showtime.start_time == date).offset(skip).limit(limit).all()