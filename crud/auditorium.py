from sqlalchemy.orm import Session
from models import Auditorium
from schemas import AuditoriumCreate

async def create_auditorium(db: Session, auditorium: AuditoriumCreate):
    db_auditorium = Auditorium(**auditorium.model_dump())
    db.add(db_auditorium)
    db.commit()
    db.refresh(db_auditorium)
    return db_auditorium

async def get_auditorium(db: Session, auditorium_id: str):
    return db.query(Auditorium).filter(Auditorium.id == auditorium_id).first()

async def get_auditoriums(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Auditorium).offset(skip).limit(limit).all()

async def delete_auditorium(db: Session, auditorium_id: str):
    db_auditorium = db.query(Auditorium).filter(Auditorium.id == auditorium_id).first()
    db.delete(db_auditorium)
    db.commit()
    return db_auditorium