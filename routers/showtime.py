from schemas import ShowtimeCreate, ShowtimeUpdate
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db, has_role
from crud.showtime import create_showtime, get_showtime, get_movie_active_showtimes, delete_showtime, get_showtimes, get_showtimes_date, update_showtime, check_availability, get_movie_history_showtimes, get_available_seats_for_showtime
from crud.movie import get_movie_id
from crud.auditorium import get_auditorium
from crud.reservation import get_reservations_showtime
from datetime import datetime, timedelta

showtime_router = APIRouter(prefix="/showtime", tags=["Showtime"])

@showtime_router.post("/")
async def create_showtime_route(showtime: ShowtimeCreate, db:Session = Depends(get_db), current_user: str = Depends(has_role("admin"))):
    movie = await get_movie_id(db, showtime.movie_id)
    auditorium = get_auditorium(db, showtime.auditorium_id)
    end_time = datetime.strptime(showtime.start_time, "%Y-%m-%d %H:%M") + timedelta(minutes=movie.duration)
    end_time_str = end_time.strftime("%Y-%m-%d %H:%M")
    list_showtimes = get_showtimes_date(db, showtime.start_time)
    for showtime_aux in list_showtimes:
        if showtime_aux.auditorium_id == showtime.auditorium_id:
            raise HTTPException(status_code=400, detail="Auditorium is already reserved")
    if showtime.avaible_tickets <= 0:
        showtime.avaible_tickets = auditorium.seats
    if showtime.avaible_tickets > auditorium.seats:
        raise HTTPException(status_code=400, detail="Not enough seats")
    return await create_showtime(db, showtime, end_time_str)

@showtime_router.get("/{showtime_id}")
async def get_showtime_route(showtime_id: str, db: Session = Depends(get_db)):
    showtime_searched = await get_showtime(db, showtime_id)
    if not showtime_searched:
        raise HTTPException(status_code=404, detail="Showtime not found")
    available_seats = get_available_seats_for_showtime(db, showtime_id)
    return {"showtime_searched": showtime_searched, "available_seats": available_seats}

@showtime_router.get("/availability/{showtime_id}")
async def check_availability_route(showtime_id: str, db: Session = Depends(get_db)):
    check_showtime = await get_showtime(db, showtime_id)
    if not check_showtime:
        raise HTTPException(status_code=404, detail="Showtime not found")
    return check_availability(db, showtime_id)

@showtime_router.get("/movie/{movie_id}")
async def get_movie_showtimes(movie_id: str, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    movie = await get_movie_id(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    active_showtimes = get_movie_active_showtimes(db, movie_id, skip, limit)
    return active_showtimes

@showtime_router.get("/movie/history/{movie_id}")
async def get_movie_showtimes_history(movie_id: str, db: Session = Depends(get_db), skip: int = 0, limit: int = 100, current_user: str = Depends(has_role("admin"))):
    return await get_movie_history_showtimes(db, movie_id, skip, limit)

@showtime_router.get("/")
def get_showtimes_route(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return get_showtimes(db, skip, limit)

@showtime_router.put("/{showtime_id}")
async def update_showtime_route(showtime_id: str, showtime: ShowtimeUpdate, db: Session = Depends(get_db), current_user: str = Depends(has_role("admin"))):
    db_showtime = await get_showtime(db, showtime_id)
    if db_showtime is None:
        raise HTTPException(status_code=404, detail="Showtime not found")
    
    reservations_showtime = get_reservations_showtime(db, showtime_id)
    if reservations_showtime:
        raise HTTPException(status_code=400, detail="Showtime has reservations")

    update_data = showtime.model_dump(exclude_unset=True)

    if "start_time" in update_data.keys():
        start_time_date = datetime.strptime(update_data["start_time"], "%Y-%m-%d %H:%M")
        if start_time_date < datetime.now():
            raise HTTPException(status_code=400, detail="Invalid start time")
        movie_showtime = await get_movie_id(db, db_showtime.movie_id)
        end_time_date = start_time_date + timedelta(minutes=movie_showtime.duration)
        update_data["end_time"] = end_time_date.strftime("%Y-%m-%d %H:%M")

    if "avaible_tickets" in update_data.keys():
        if update_data["avaible_tickets"] < 0:
            raise HTTPException(status_code=400, detail="Invalid avaible tickets")
        auditorium_showtime = get_auditorium(db, db_showtime.auditorium_id)
        if update_data["avaible_tickets"] > auditorium_showtime.seats:
            raise HTTPException(status_code=400, detail="Not enough seats")
        
    if "auditorium_id" in update_data.keys():
        auditorium_showtime = await get_auditorium(db, db_showtime.auditorium_id)
        if update_data["auditorium_id"] != db_showtime.auditorium_id:
            list_showtimes = get_showtimes_date(db, update_data["start_time"])
            for showtime_aux in list_showtimes:
                if showtime_aux.auditorium_id == update_data["auditorium_id"]:
                    raise HTTPException(status_code=400, detail="Auditorium is already reserved")
            if "avaible_tickets" in update_data.keys():
                if update_data["avaible_tickets"] > auditorium_showtime.seats:
                    raise HTTPException(status_code=400, detail="Not enough seats")
                else:
                    if update_data["avaible_tickets"] <= 0:
                        update_data["avaible_tickets"] = auditorium_showtime.seats

    return await update_showtime(db, showtime_id, update_data)

@showtime_router.delete("/{showtime_id}")
async def delete_showtime_route(showtime_id: str, db: Session = Depends(get_db), current_user: str = Depends(has_role("admin"))):
    showtime_searched = await get_showtime(db, showtime_id)
    if not showtime_searched:
        raise HTTPException(status_code=404, detail="Showtime not found")
    return await delete_showtime(db, showtime_id)
    
