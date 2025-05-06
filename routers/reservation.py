from fastapi import HTTPException, Depends, APIRouter
from crud.reservation import get_reservations, get_reservation, create_reservation, delete_reservation, get_user_active_reservations_on_showtime, get_user_reservations
from crud.user import get_user
from crud.showtime import register_reservation_showtime, get_showtimes_date, update_deleted_reservation, get_showtime, are_seats_available
from crud.seats import get_seat
from crud.seat_reservation import create_seat_reservation, delete_seat_reservation, get_seats_of_reservation
from sqlalchemy.orm import Session
from dependencies import get_db, get_current_user, has_role
from datetime import datetime
from schemas import ReservationCreate, ReservationRead
from models import SeatReservation, Seat

reservation_router = APIRouter(prefix="/reservation", tags=["Reservation"])

@reservation_router.post("/", response_model=ReservationRead)
async def create_reservation_route(reservation: ReservationCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    user = get_user(db, current_user)
    if(not user):
        HTTPException(status_code=400, detail="Invalid user")
    
    if reservation.amount != len(reservation.seats_list):
        raise HTTPException(status_code=400, detail="Amount of seats does not match reservation amount")
    
    check_reservation = get_user_active_reservations_on_showtime(db, user.id, reservation.showtime_id)
    if(check_reservation):
        raise HTTPException(status_code=400, detail="User already has an active reservation on this showtime")
    
    showtime = await get_showtime(db, reservation.showtime_id)
    if(not showtime):
        raise HTTPException(status_code=400, detail="Invalid showtime id")

    seats = []
    for seat_id in reservation.seats_list:
        seat = get_seat(db, seat_id)
        if not seat:
            raise HTTPException(status_code=400, detail=f"Invalid seat code")
        seats.append(seat)

    for seat in seats:
        if seat.auditorium_id != showtime.auditorium_id:
            raise HTTPException(status_code=400, detail="Seat does not belong to the showtime's auditorium")

    check_seat_availability = are_seats_available(db, reservation.showtime_id, reservation.seats_list)
    if not check_seat_availability:
        raise HTTPException(status_code=400, detail="One or more seats are already reserved")

    await register_reservation_showtime(db, reservation.showtime_id, reservation.amount)
    new_reservation = create_reservation(db, reservation.amount, reservation.showtime_id, user.id)

    for seat in seats:
        create_seat_reservation(db, seat.id, new_reservation.id)

    return new_reservation

@reservation_router.get("/")
async def get_reservations_route(db: Session = Depends(get_db), skip: int = 0, limit: int = 100, current_user: str = Depends(has_role("admin"))):
    return get_reservations(db, skip, limit)

@reservation_router.get("/user/active")
async def get_user_active_reservations_route(db: Session = Depends(get_db), skip: int = 0, limit: int = 100, current_user: str = Depends(get_current_user)):
    user = get_user(db, current_user)
    if(not user):
        HTTPException(status_code=400, detail="Invalid user")
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    actives_showtimes = get_showtimes_date(db, now_str, skip, limit)
    active_reservations = []
    for showtime in actives_showtimes:
        active_reservations.add(get_user_reservations(db, user.id, showtime.id))
    return active_reservations

@reservation_router.get("/user/history")
async def get_user_reservations_route(db: Session = Depends(get_db), skip: int = 0, limit: int = 100, current_user: str = Depends(get_current_user)):
    user = get_user(db, current_user)
    if(not user):
        HTTPException(status_code=400, detail="Invalid user")
    return get_user_reservations(db, user.id, skip, limit)

@reservation_router.get("/{reservation_id}")
async def get_reservation_route(reservation_id: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    user = get_user(db, current_user)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid user")
    searched_reservation = get_reservation(db, reservation_id)
    if not searched_reservation:
        raise HTTPException(status_code=400, detail="Invalid reservation id")
    if user.id != searched_reservation.user_id:
        raise HTTPException(status_code=400, detail="Invalid user for reservation")
    return searched_reservation

@reservation_router.delete("/{reservation_id}")
async def delete_reservation_route(reservation_id: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    user = get_user(db, current_user)
    if(not user):
        HTTPException(status_code=400, detail="Invalid user")
    searched_reservation = get_reservation(db, reservation_id)
    if(not searched_reservation):
        raise HTTPException(status_code=400, detail="Invalid reservation id")
    if(user.id != searched_reservation.user_id):
        raise HTTPException(status_code=400, detail="Invalid user for reservation")
    await update_deleted_reservation(db, searched_reservation.showtime_id, searched_reservation.amount)
    for seat_reservation in get_seats_of_reservation(db, reservation_id):
        delete_seat_reservation(db, seat_reservation.seat_id, reservation_id)
    delete_reservation(db, reservation_id, user.id)
    return {"message": "Reservation deleted"}