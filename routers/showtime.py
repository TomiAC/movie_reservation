from schemas import ShowtimeCreate
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db, has_role
from crud.showtime import create_showtime, get_showtime, get_movie_active_showtimes, delete_showtime, get_showtimes, get_showtimes_date
from crud.movie import get_movie_id
from crud.auditorium import get_auditorium
from datetime import datetime, timedelta

showtime_router = APIRouter(prefix="/showtime", tags=["Showtime"])

@showtime_router.post("/")
async def create_showtime_route(showtime: ShowtimeCreate, db:Session = Depends(get_db), current_user: str = Depends(has_role("admin"))):
    movie = await get_movie_id(db, showtime.movie_id)
    auditorium = await get_auditorium(db, showtime.auditorium_id)
    end_time = datetime.strptime(showtime.start_time, "%Y-%m-%d %H:%M") + timedelta(minutes=int(movie.duration))
    end_time_str = end_time.strftime("%Y-%m-%d %H:%M")
    list_showtimes = get_showtimes_date(db, showtime.start_time)
    for showtime_aux in list_showtimes:
        if showtime_aux.auditorium_id == showtime.auditorium_id:
            raise HTTPException(status_code=400, detail="Auditorium is already reserved")
    if showtime.avaible_tickets <= 0:
        showtime.avaible_tickets = auditorium.seats
    return await create_showtime(db, showtime, end_time_str)

@showtime_router.get("/")
async def get_showtimes(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return await get_showtimes(db, skip, limit)

@showtime_router.get("/movie/{movie_name}")
async def get_movie_showtimes(movie_name: str, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return await get_movie_active_showtimes(db, movie_name, skip, limit)

@showtime_router.get("/{showtime_id}")
async def get_showtime_route(showtime_id: str, db: Session = Depends(get_db)):
    return await get_showtime(db, showtime_id)

@showtime_router.delete("/{showtime_id}")
async def delete_showtime_route(showtime_id: str, db: Session = Depends(get_db), current_user: str = Depends(has_role("admin"))):
    return await delete_showtime(db, showtime_id)
    
