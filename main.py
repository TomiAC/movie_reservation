from fastapi import FastAPI
from routers.user import auth_router
from routers.reservation import reservation_router
from routers.movie import movie_router
from routers.auditorium import auditorium_router
from routers.showtime import showtime_router
from fastapi.security import OAuth2PasswordBearer
from database import engine, Base
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(reservation_router)
app.include_router(movie_router)
app.include_router(auditorium_router)
app.include_router(showtime_router)

@app.get("/")
def home():
    return {"message": "hello"}