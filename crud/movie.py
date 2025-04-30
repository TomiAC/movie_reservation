from sqlalchemy.orm import Session
from models import Movie
from schemas import MovieCreate

async def create_movie(db: Session, movie: MovieCreate):
    db_movie = Movie(**movie.model_dump(mode="json"))
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

async def get_movies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Movie).offset(skip).limit(limit).all()

async def get_movie(db: Session, movie_name: str):
    return db.query(Movie).filter(Movie.name == movie_name).first()

async def get_movie_id(db: Session, movie_id: str):
    return db.query(Movie).filter(Movie.id == movie_id).first()

async def delete_movie(db: Session, movie_id: str):
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    db.delete(db_movie)
    db.commit()
    return db_movie