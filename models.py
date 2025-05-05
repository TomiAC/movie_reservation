from database import Base
from sqlalchemy import Column, String, Integer, ForeignKey
from uuid import uuid4

class User(Base):
    __tablename__ = "user"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    name = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(String, default="user")


class Movie(Base):
    __tablename__ = "movie"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    name = Column(String)
    description = Column(String)
    poster = Column(String)
    duration = Column(Integer)
    genre = Column(String)
    format = Column(String)

class Reservation(Base):
    __tablename__ = "reservation"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    amount = Column(Integer)
    user_id = Column(String, ForeignKey("user.id"), nullable=False, index=True)
    showtime_id = Column(String, ForeignKey("showtime.id"), nullable=False, index=True)

class Showtime(Base):
    __tablename__ = "showtime"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    start_time = Column(String)
    end_time = Column(String)
    avaible_tickets = Column(Integer)
    status = Column(String)
    movie_id = Column(String, ForeignKey("movie.id"), nullable=False, index=True)
    auditorium_id = Column(String, ForeignKey("auditorium.id"), nullable=False, index=True)

class Auditorium(Base):
    __tablename__= "auditorium"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    number = Column(Integer)
    seats = Column(Integer)
    rows = Column(Integer)
    columns = Column(Integer)

class Seat(Base):
    __tablename__= "seat"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    code = Column(String)
    auditorium_id = Column(String, ForeignKey("auditorium.id"), nullable=False, index=True)

class SeatReservation(Base):
    __tablename__= "seats_reservation"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    seat_id = Column(String, ForeignKey("seat.id"), nullable=False, index=True)
    reservation_id = Column(String, ForeignKey("reservation.id"), nullable=False, index=True)