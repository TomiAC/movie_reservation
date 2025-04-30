from fastapi import HTTPException, Depends, APIRouter
from crud.reservation import get_reservations, get_reservation, create_reservation, delete_reservation, get_user_active_reservations_on_showtime, get_user_reservations
from crud.user import get_user
from crud.showtime import register_reservation_showtime, get_showtimes_date, update_deleted_reservation
from schemas import ReservationCreate
from sqlalchemy.orm import Session
from dependencies import get_db, get_current_user
from datetime import datetime

reservation_router = APIRouter(prefix="/reservation", tags=["Reservation"])

@reservation_router.post("/")
async def create_reservation_route(reservation: ReservationCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    user = get_user(db, current_user)
    if(not user):
        HTTPException(status_code=400, detail="Invalid user")
    check_reservation = get_user_active_reservations_on_showtime(db, user.id, reservation.showtime_id)
    if(check_reservation):
        raise HTTPException(status_code=400, detail="User already has an active reservation on this showtime")
    await register_reservation_showtime(db, reservation.showtime_id, reservation.amount)
    new_reservation = create_reservation(db, reservation, user.id)
    return new_reservation

@reservation_router.get("/")
async def get_reservations_route(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return get_reservations(db, skip, limit)

@reservation_router.get("/user/active/{user_id}")
async def get_user_active_reservations_route(user_id: str, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    actives_showtimes = get_showtimes_date(db, now_str, skip, limit)
    active_reservations = []
    for showtime in actives_showtimes:
        active_reservations.add(get_user_reservations(db, user_id, showtime.id))
    return active_reservations

@reservation_router.get("/user/history/{user_id}")
async def get_user_reservations_route(user_id: str, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return get_user_reservations(db, user_id, skip, limit)

@reservation_router.get("/{reservation_id}")
async def get_reservation_route(reservation_id: str, db: Session = Depends(get_db)):
    return get_reservation(db, reservation_id)

@reservation_router.delete("/{reservation_id}")
async def delete_reservation_route(reservation_id: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    user = get_user(db, current_user)
    if(not user):
        HTTPException(status_code=400, detail="Invalid user")
    await update_deleted_reservation(db, reservation_id)
    return delete_reservation(db, reservation_id, user.id)