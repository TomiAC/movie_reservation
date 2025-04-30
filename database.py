from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL="sqlite:///./test.db"

# Configurar el motor de SQLAlchemy
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Crear sesión para consultas
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()