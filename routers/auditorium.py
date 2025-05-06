from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from crud.auditorium import get_auditorium, create_auditorium, delete_auditorium, get_auditoriums, update_auditorium
from crud.seats import create_seat, get_seats_auditorium
from schemas import AuditoriumCreate, AuditoriumUpdate, AuditoriumRead
from dependencies import get_db, has_role

auditorium_router = APIRouter(prefix="/auditorium", tags=["Auditorium"])

@auditorium_router.post("/", response_model=AuditoriumRead)
def create_auditorium_route(auditorium: AuditoriumCreate, db: Session = Depends(get_db), current_user: str = Depends(has_role("admin"))):
    if not (auditorium.seats == auditorium.rows * auditorium.columns):
        raise HTTPException(status_code=400, detail="Invalid seats, rows and columns")
    new_auditorium = create_auditorium(db, auditorium)
    for i in range(auditorium.rows):
        for j in range(auditorium.columns):
            code = chr(ord('A') + i) + str(j)
            create_seat(db, code, new_auditorium.id)
    return new_auditorium

@auditorium_router.get("/{auditorium_id}")
def get_auditorium_route(auditorium_id: str, db: Session = Depends(get_db)):
    return get_auditorium(db, auditorium_id)

@auditorium_router.get("/")
def get_auditoriums_route(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return get_auditoriums(db, skip, limit)

@auditorium_router.put("/{auditorium_id}", response_model=AuditoriumRead)
def update_auditorium_route(auditorium_id: str, auditorium: AuditoriumUpdate, db: Session = Depends(get_db), current_user: str = Depends(has_role("admin"))):
    updated_auditorium = update_auditorium(db, auditorium_id, auditorium)
    if updated_auditorium is None:
        raise HTTPException(status_code=404, detail="Auditorium not found")
    return updated_auditorium

@auditorium_router.delete("/{auditorium_id}", response_model=AuditoriumRead)
def delete_auditorium_route(auditorium_id: str, db: Session = Depends(get_db), current_user: str = Depends(has_role("admin"))):
    deleted_auditorium = delete_auditorium(db, auditorium_id)
    if not deleted_auditorium:
        raise HTTPException(status_code=404, detail="Auditorium not found")
    return deleted_auditorium