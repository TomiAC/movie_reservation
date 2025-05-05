from models import Seat
from sqlalchemy.orm import Session

def get_seats_auditorium(db: Session, auditorium_id: str, skip: int = 0, limit: int = 100):
    return db.query(Seat).filter(Seat.auditorium_id == auditorium_id).offset(skip).limit(limit).all()

async def create_seat(db: Session, code: str, auditorium_id: str):
    db_seat = Seat(code=code, auditorium_id=auditorium_id)
    db.add(db_seat)
    db.commit()
    db.refresh(db_seat)
    return db_seat

def get_seat_by_code(db: Session, code: str):
    return db.query(Seat).filter(Seat.code == code).first()