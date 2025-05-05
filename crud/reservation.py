from sqlalchemy.orm import Session
from models import Reservation
from schemas import ReservationCreate
from fastapi import HTTPException
from datetime import datetime

def create_reservation(db: Session, amount: int, showtime_id: str, user_id: str):
    db_reservation = Reservation(amount=amount, showtime_id=showtime_id, user_id=user_id)
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

def get_reservations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Reservation).offset(skip).limit(limit).all()

def get_reservation(db: Session, reservation_id: str):
    return db.query(Reservation).filter(Reservation.id == reservation_id).first()

def delete_reservation(db: Session, reservation_id: str, user_id: str):
    db_reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if db_reservation.user_id != user_id:
        raise HTTPException(status_code=400, detail="Invalid user")
    db.delete(db_reservation)
    db.commit()
    return db_reservation

def get_user_reservations(db: Session, user_id: str, skip: int = 0, limit: int = 100):
    return db.query(Reservation).filter(Reservation.user_id == user_id).offset(skip).limit(limit).all()

def get_user_active_reservations_on_showtime(db: Session, user_id: str, showtime_id: str, skip: int = 0, limit: int = 100):
    return db.query(Reservation).filter(Reservation.user_id == user_id, Reservation.showtime_id == showtime_id).offset(skip).limit(limit).all()

def get_reservations_showtime(db: Session, showtime_id: str, skip: int = 0, limit: int = 100):
    return db.query(Reservation).filter(Reservation.showtime_id == showtime_id).offset(skip).limit(limit).all()