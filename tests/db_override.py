# tests/db_override.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from models import *  # importa tus modelos

# Base de datos en memoria (puede ser archivo si preferís persistencia)
TEST_DATABASE_URL = "sqlite:///./test.db"  # o "sqlite:///:memory:" para memoria

engine_test = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine_test, autocommit=False, autoflush=False)

# Crear las tablas
Base.metadata.create_all(bind=engine_test)

# Override de get_db
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()