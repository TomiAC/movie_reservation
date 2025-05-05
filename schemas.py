from pydantic import BaseModel, EmailStr, HttpUrl
from enums import UserRole
from typing import Optional, List

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
    seats_list: List[str]

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
    rows: int
    columns: int

class ShowtimeUpdate(BaseModel):
    start_time: Optional[str] = None
    avaible_tickets: Optional[int] = None
    status: Optional[str] = None
    auditorium_id: Optional[str] = None

class AuditoriumUpdate(BaseModel):
    seats: Optional[int] = None

class MovieUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    poster: Optional[HttpUrl] = None
    duration: Optional[int] = None
    genre: Optional[str] = None

class ReservationRead(BaseModel):
    id: str
    amount: int
    showtime_id: str
    user_id: str

class ShowtimeRead(BaseModel):
    id: str
    start_time: str
    avaible_tickets: int
    status: str

class AuditoriumRead(BaseModel):
    id: str
    number: int
    seats: int
    rows: int
    columns: int