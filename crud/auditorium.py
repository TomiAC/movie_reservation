from sqlalchemy.orm import Session
from models import Auditorium
from schemas import AuditoriumCreate

def create_auditorium(db: Session, auditorium: AuditoriumCreate):
    db_auditorium = Auditorium(**auditorium.model_dump())
    db.add(db_auditorium)
    db.commit()
    db.refresh(db_auditorium)
    return db_auditorium

def get_auditorium(db: Session, auditorium_id: str):
    return db.query(Auditorium).filter(Auditorium.id == auditorium_id).first()

def get_auditoriums(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Auditorium).offset(skip).limit(limit).all()

def update_auditorium(db: Session, auditorium_id: str, auditorium: AuditoriumCreate):
    db_auditorium = db.query(Auditorium).filter(Auditorium.id == auditorium_id).first()
    if not db_auditorium:
        return None
    db_auditorium.seats = auditorium.seats
    db.commit()
    db.refresh(db_auditorium)
    return db_auditorium

def delete_auditorium(db: Session, auditorium_id: str):
    db_auditorium = db.query(Auditorium).filter(Auditorium.id == auditorium_id).first()
    if not db_auditorium:
        return None
    db.delete(db_auditorium)
    db.commit()
    return db_auditorium