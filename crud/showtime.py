from sqlalchemy.orm import Session, aliased
from sqlalchemy import select, and_
from models import Showtime, Seat, SeatReservation, Reservation
from schemas import ShowtimeCreate
from datetime import datetime

async def create_showtime(db: Session, showtime: ShowtimeCreate, end_time: str):
    db_showtime = Showtime(**showtime.model_dump(), end_time=end_time)
    db.add(db_showtime)
    db.commit()
    db.refresh(db_showtime)
    return db_showtime

def get_movie_active_showtimes(db: Session, movie_id: str, skip: int = 0, limit: int = 100):
    active_showtimes = []
    actual_date = datetime.now()
    for showtime in db.query(Showtime).filter(Showtime.movie_id == movie_id).offset(skip).limit(limit).all():
        start_time = datetime.strptime(showtime.start_time, "%Y-%m-%d %H:%M")
        if start_time > actual_date:
            active_showtimes.append(showtime)
    return active_showtimes

async def get_movie_history_showtimes(db: Session, movie_id: str, skip: int = 0, limit: int = 100):
    return db.query(Showtime).filter(Showtime.movie_id == movie_id).offset(skip).limit(limit).all()

async def get_showtime(db: Session, showtime_id: str):
    return db.query(Showtime).filter(Showtime.id == showtime_id).first()

async def update_showtime(db: Session, showtime_id: str, update_data: dict) -> Showtime | None:
    db_showtime = db.query(Showtime).filter(Showtime.id == showtime_id).first()
    if db_showtime:
        for key, value in update_data.items():
            setattr(db_showtime, key, value)
        db.commit()
        db.refresh(db_showtime)
        return db_showtime
    return None

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

async def update_deleted_reservation(db: Session, showtime_id: str, tickets: int):
    db_showtime = db.query(Showtime).filter(Showtime.id == showtime_id).first()
    result = db_showtime.avaible_tickets + tickets
    db_showtime.avaible_tickets = result
    db.commit()
    db.refresh(db_showtime)
    return db_showtime

def get_showtimes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Showtime).offset(skip).limit(limit).all()

def get_showtimes_date(db: Session, date: str, skip: int = 0, limit: int = 100):
    return db.query(Showtime).filter(Showtime.start_time == date).offset(skip).limit(limit).all()

def check_availability(db: Session, showtime_id: str):
    db_showtime = db.query(Showtime).filter(Showtime.id == showtime_id).first()
    if db_showtime.avaible_tickets > 0:
        return db_showtime.avaible_tickets
    return False

def get_available_seats_for_showtime(db: Session, showtime_id: str):
    """
    Get available sets for a showtime.
    """
    # Obtener el showtime y su auditorio
    showtime = db.query(Showtime).filter(Showtime.id == showtime_id).first()
    if not showtime or not showtime.auditorium_id:
        return []

    auditorium_id = showtime.auditorium_id

    reserved_seat_ids_subquery = (
        select(SeatReservation.seat_id)
        .join(Reservation, Reservation.id == SeatReservation.reservation_id)
        .where(Reservation.showtime_id == showtime_id)
        .scalar_subquery()
    )

    available_seats = db.query(Seat).filter(
        and_(
            Seat.auditorium_id == auditorium_id,
            Seat.id.notin_(reserved_seat_ids_subquery)
        )
    ).all()

    return available_seats

def are_seats_available(db: Session, showtime_id: str, requested_seat_ids: list[int]) -> bool:
    """
    Check if a list of seat IDs are available for a specific showtime.
    """
    already_reserved = db.query(SeatReservation).join(
        Reservation, Reservation.id == SeatReservation.reservation_id
    ).filter(
        and_(
            SeatReservation.seat_id.in_(requested_seat_ids),
            Reservation.showtime_id == showtime_id
        )
    ).count()

    return already_reserved == 0