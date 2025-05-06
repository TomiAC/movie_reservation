from fastapi import FastAPI
from routers.user import auth_router
from routers.reservation import reservation_router
from routers.movie import movie_router
from routers.auditorium import auditorium_router
from routers.showtime import showtime_router
from fastapi.security import OAuth2PasswordBearer
from database import engine, Base, SessionLocal
from dotenv import load_dotenv
from hashing import hash_password
from models import User, Reservation, Showtime, Auditorium, Movie, Seat, SeatReservation
import os

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

def populate_database():
    db = SessionLocal()
    try:
        
        if db.query(User).count() == 0:
            
            admin_user = User(
                name="Admin User",
                email="admin@example.com",
                password=hash_password("admin123"),
                role="admin"
            )
            db.add(admin_user)

            
            users_to_create = [
                {"name": "User One", "email": "user1@example.com", "password": "user1pass"},
                {"name": "User Two", "email": "user2@example.com", "password": "user2pass"},
                {"name": "User Three", "email": "user3@example.com", "password": "user3pass"},
                {"name": "User Four", "email": "user4@example.com", "password": "user4pass"},
            ]
            for user_data in users_to_create:
                db_user = User(name=user_data["name"], email=user_data["email"], password=hash_password(user_data["password"]))
                db.add(db_user)

            db.commit()
            print("Usuarios iniciales creados.")

        if db.query(Movie).count() == 0:
            
            movies_to_create = [
                {"name": "The Great Adventure", "description": "A thrilling adventure story.", "poster": "adventure.jpg", "duration": 120, "genre": "Adventure", "format": "2D"},
                {"name": "Romantic Sunset", "description": "A heartwarming romantic drama.", "poster": "romance.jpg", "duration": 105, "genre": "Romance", "format": "2D"},
                {"name": "Space Explorers 3D", "description": "An immersive sci-fi experience.", "poster": "scifi.jpg", "duration": 135, "genre": "Sci-Fi", "format": "3D"},
            ]
            for movie_data in movies_to_create:
                db_movie = Movie(**movie_data)
                db.add(db_movie)

            db.commit()
            print("Películas iniciales creadas.")

        if db.query(Auditorium).count() == 0:
            
            auditoriums_to_create = [
                {"number": 1, "seats": 100, "rows": 10, "columns": 10},
                {"number": 2, "seats": 150, "rows": 10, "columns": 15},
            ]
            for auditorium_data in auditoriums_to_create:
                db_auditorium = Auditorium(**auditorium_data)
                db.add(db_auditorium)

            db.commit()
            print("Auditorios iniciales creados.")

        
        movies = db.query(Movie).all()
        auditoriums = db.query(Auditorium).all()
        users = db.query(User).all()

        if auditoriums:
            
            for auditorium in auditoriums:
                for i in range(auditorium.rows):
                    for j in range(auditorium.columns):
                        code = chr(ord('A') + i) + str(j)
                        seat = Seat(code=code, auditorium_id=auditorium.id)
                        db.add(seat)

            db.commit()
            print("Asientos creados.")

        if movies and auditoriums and db.query(Showtime).count() < 5:
            
            showtimes_to_create = [
                {"start_time": "2025-04-20 18:00", "end_time": "2025-04-20 20:00", "avaible_tickets": auditoriums[0].seats - 5, "status": "active", "movie_id": movies[0].id, "auditorium_id": auditoriums[0].id},
                {"start_time": "2025-04-20 20:30", "end_time": "2025-04-20 22:15", "avaible_tickets": auditoriums[1].seats - 1, "status": "active", "movie_id": movies[1].id, "auditorium_id": auditoriums[1].id},
                {"start_time": "2025-04-10 15:00", "end_time": "2025-04-10 17:15", "avaible_tickets": auditoriums[0].seats - 2, "status": "active", "movie_id": movies[2].id, "auditorium_id": auditoriums[0].id},
                {"start_time": "2025-05-10 21:00", "end_time": "2025-05-10 23:00", "avaible_tickets": auditoriums[1].seats, "status": "inactive", "movie_id": movies[0].id, "auditorium_id": auditoriums[1].id},
                {"start_time": "2025-05-20 19:00", "end_time": "2025-05-20 20:45", "avaible_tickets": auditoriums[0].seats, "status": "active", "movie_id": movies[1].id, "auditorium_id": auditoriums[0].id},
            ]
            for showtime_data in showtimes_to_create:
                db_showtime = Showtime(**showtime_data)
                db.add(db_showtime)

            db.commit()
            print("Showtimes iniciales creados.")

        showtimes = db.query(Showtime).all()
        if users and showtimes and db.query(Reservation).count() < 4:
            
            reservations_to_create = [
                {"amount": 2, "user_id": users[1].id, "showtime_id": showtimes[0].id},
                {"amount": 1, "user_id": users[2].id, "showtime_id": showtimes[1].id},
                {"amount": 3, "user_id": users[3].id, "showtime_id": showtimes[0].id},
                {"amount": 2, "user_id": users[4].id, "showtime_id": showtimes[2].id},
            ]
            for reservation_data in reservations_to_create:
                db_reservation = Reservation(**reservation_data)
                db.add(db_reservation)

            db.commit()
            print("Reservas iniciales creadas.")

            seats = db.query(Seat).all()  
            reservations = db.query(Reservation).all()

        if seats:
            seat_reservations_to_create = []
            
            seat_reservations_to_create.append(SeatReservation(seat_id=seats[10].id, reservation_id=reservations[0].id))
            seat_reservations_to_create.append(SeatReservation(seat_id=seats[11].id, reservation_id=reservations[0].id))

            
            seat_reservations_to_create.append(SeatReservation(seat_id=seats[150].id, reservation_id=reservations[1].id))

            
            seat_reservations_to_create.append(SeatReservation(seat_id=seats[33].id, reservation_id=reservations[2].id))
            seat_reservations_to_create.append(SeatReservation(seat_id=seats[34].id, reservation_id=reservations[2].id))
            seat_reservations_to_create.append(SeatReservation(seat_id=seats[35].id, reservation_id=reservations[2].id))

            
            seat_reservations_to_create.append(SeatReservation(seat_id=seats[126].id, reservation_id=reservations[3].id))
            seat_reservations_to_create.append(SeatReservation(seat_id=seats[127].id, reservation_id=reservations[3].id))

            for seat_reservation in seat_reservations_to_create:
                db.add(seat_reservation)
            db.commit()

            print("Asientos reservados.")
        


        db.commit()
    finally:
        db.close()

if os.getenv("ENV") != "test":
    app.add_event_handler("startup", populate_database)

@app.get("/")
def home():
    return {"message": "hello"}

