# tests/conftest.py

import pytest
from sqlalchemy.orm import Session
from .db_override import override_get_db, Base, engine_test
from models import User
from dependencies import create_access_token
from hashing import hash_password
from main import app
from dependencies import get_db

app.dependency_overrides[get_db] = override_get_db

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
def admin_token(admin_user):
    return create_access_token(data={"sub": admin_user.email, "role": admin_user.role})