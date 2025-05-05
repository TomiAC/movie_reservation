from fastapi import Depends, HTTPException, APIRouter
from crud.movie import get_movie, create_movie, delete_movie, get_movies, get_movie_id, update_movie
from schemas import MovieCreate, MovieUpdate, MovieRead
from sqlalchemy.orm import Session
from dependencies import get_db, has_role

movie_router = APIRouter(prefix="/movie", tags=["Movie"])

@movie_router.post("/")
async def create_movie_route(movie: MovieCreate, db: Session = Depends(get_db), current_user: str = Depends(has_role("admin"))):	
    return await create_movie(db, movie)

@movie_router.get("/")
async def get_movies_route(db: Session = Depends(get_db)):
    return await get_movies(db)

@movie_router.get("/{movie_name}")
async def get_movie_route(movie_name: str, db: Session = Depends(get_db)):
    return await get_movie(db, movie_name)

@movie_router.get("/id/{movie_id}")
async def get_movie_id_route(movie_id: str, db: Session = Depends(get_db)):
    return await get_movie_id(db, movie_id)

@movie_router.put("/{movie_id}", response_model=MovieRead)
async def update_movie_route(movie_id: str, movie: MovieUpdate, db: Session = Depends(get_db), current_user: str = Depends(has_role("admin"))):
    updated_movie = await update_movie(db, movie_id, movie)
    if updated_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return updated_movie

@movie_router.delete("/{movie_id}")
async def delete_movie_route(movie_id: str, db: Session = Depends(get_db), current_user: str = Depends(has_role("admin"))):
    return await delete_movie(db, movie_id)
