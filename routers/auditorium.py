from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from crud.auditorium import get_auditorium, create_auditorium, delete_auditorium, get_auditoriums, update_auditorium
from schemas import AuditoriumCreate, AuditoriumUpdate
from dependencies import get_db, has_role

auditorium_router = APIRouter(prefix="/auditorium", tags=["Auditorium"])

@auditorium_router.get("/")
async def get_auditoriums_route(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return await get_auditoriums(db, skip, limit)

@auditorium_router.post("/")
async def create_auditorium_route(auditorium: AuditoriumCreate, db: Session = Depends(get_db), current_user: str = Depends(has_role("admin"))):
    return await create_auditorium(db, auditorium)

@auditorium_router.get("/{auditorium_id}")
async def get_auditorium_route(auditorium_id: str, db: Session = Depends(get_db)):
    return await get_auditorium(db, auditorium_id)

@auditorium_router.put("/{auditorium_id}")
async def update_auditorium_route(auditorium_id: str, auditorium: AuditoriumUpdate, db: Session = Depends(get_db), current_user: str = Depends(has_role("admin"))):
    return await update_auditorium(db, auditorium_id, auditorium)

@auditorium_router.delete("/{auditorium_id}")
async def delete_auditorium_route(auditorium_id: str, db: Session = Depends(get_db), current_user: str = Depends(has_role("admin"))):
    return await delete_auditorium(db, auditorium_id)