# tests/conftest.py

import pytest
from sqlalchemy.orm import Session
from .db_override import override_get_db, Base, engine_test
from models import User
from dependencies import create_access_token
from hashing import hash_password
from dependencies import get_db
from fastapi.testclient import TestClient
import os
os.environ["ENV"] = "test"


@pytest.fixture(scope="session")
def test_db():
    Base.metadata.create_all(bind=engine_test)
    db = Session(bind=engine_test)
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine_test)

@pytest.fixture
def admin_user(test_db):
    hashed_password = hash_password("admin123")
    user = User(
        email="admin@test.com",
        password=hashed_password,
        name="Admin",
        role="admin"
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user

@pytest.fixture
def user_user(test_db):
    hashed_password = hash_password("user123")
    user = User(
        email="user@test.com",
        password=hashed_password,
        name="User",
        role="user"
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user

@pytest.fixture
def admin_token(admin_user):
    return create_access_token(data={"sub": admin_user.email, "role": admin_user.role})

@pytest.fixture
def user_user_token(user_user):
    return create_access_token(data={"sub": user_user.email, "role": user_user.role})

@pytest.fixture
def client():
    from main import app
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.fixture
def created_movie(client, admin_token):
    response = client.post(
        "/movie/",
        json={"name": "Test Movie", "description": "Test Description", "poster": "https://example.com/poster.jpg", "duration": 120, "genre": "Action"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    return response.json()["id"]

@pytest.fixture
def created_auditorium(client, admin_token):
    response = client.post(
        "/auditorium/",
        json={"number": "1", "seats": 100, "rows": 10, "columns": 10},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    return response.json()["id"]

@pytest.fixture
def created_small_auditorium(client, admin_token):
    response = client.post(
        "/auditorium/",
        json={"number": "2", "seats": 20, "rows": 10, "columns": 2},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    return response.json()["id"]

@pytest.fixture
def created_showtime(client, created_movie, created_auditorium, admin_token):
    response = client.post(
        "/showtime/",
        json={"movie_id": created_movie, "auditorium_id": created_auditorium, "start_time": "2025-05-20 12:00", "avaible_tickets": 0, "status": "active"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    return response.json()["id"]

@pytest.fixture
def created_showtime_old(client, created_movie, created_auditorium, admin_token):
    response = client.post(
        "/showtime/",
        json={"movie_id": created_movie, "auditorium_id": created_auditorium, "start_time": "2024-05-20 12:00", "avaible_tickets": 0, "status": "active"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    return response.json()["id"]