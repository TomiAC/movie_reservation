from models import SeatReservation, Reservation
from sqlalchemy.orm import Session

def create_seat_reservation(db: Session, seat_id: str, reservation_id: str):
    db_seat_reservation = SeatReservation(seat_id=seat_id, reservation_id=reservation_id)
    db.add(db_seat_reservation)
    db.commit()
    db.refresh(db_seat_reservation)
    return db_seat_reservation

def check_seat_reservation(db: Session, seat_id: str, reservation_id: str):
    return db.query(SeatReservation).filter(SeatReservation.seat_id == seat_id, SeatReservation.reservation_id == reservation_id).first()

def get_seat_by_reservation_showtime(db: Session, reservation_id: str, showtime_id: str, seat_id: str):
    return db.query(SeatReservation).join(Reservation).filter(SeatReservation.reservation_id == reservation_id, Reservation.showtime_id == showtime_id, SeatReservation.seat_id == seat_id).first()

def delete_seat_reservation(db: Session, seat_id: str, reservation_id: str):
    db_seat_reservation = db.query(SeatReservation).filter(SeatReservation.seat_id == seat_id, SeatReservation.reservation_id == reservation_id).first()
    db.delete(db_seat_reservation)
    db.commit()
    return db_seat_reservation