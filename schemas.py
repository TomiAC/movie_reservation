from pydantic import BaseModel, EmailStr, HttpUrl
from enums import UserRole

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str

class UserRead(BaseModel):
    name: str
    email: EmailStr
    role: str

class UserEmail(BaseModel):
    email: EmailStr

class MovieCreate(BaseModel):
    name: str
    description: str
    poster: HttpUrl
    duration: int
    genre: str

class ReservationCreate(BaseModel):
    amount: int
    showtime_id: str

class ShowtimeCreate(BaseModel):
    start_time: str
    avaible_tickets: int
    status: str
    movie_id: str
    auditorium_id: str

class selectAuditorium(BaseModel):
    number: str

class AuditoriumCreate(BaseModel):
    number: int
    seats: int