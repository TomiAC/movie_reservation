from models import Seat
from sqlalchemy.orm import Session

def letra_a_numero(letra: str) -> int:
    """Convierte una letra mayúscula del alfabeto (sin ñ) a su número correspondiente (A=1, B=2, ...)."""
    if not 'A' <= letra <= 'Z' or len(letra) != 1:
        raise ValueError("La entrada debe ser una única letra mayúscula del alfabeto inglés.")
    return ord(letra) - ord('A') + 1

def numero_a_letra(numero: int) -> str:
    """Convierte un número entero positivo a su representación alfanumérica (1=A, 2=B, ..., 27=AA, ...)."""
    if not isinstance(numero, int) or numero <= 0:
        raise ValueError("La entrada debe ser un entero positivo.")

    resultado = ""
    while numero > 0:
        residuo = (numero - 1) % 26
        resultado = chr(ord('A') + residuo) + resultado
        numero = (numero - 1) // 26
    return resultado

def get_seats_auditorium(db: Session, auditorium_id: str, skip: int = 0, limit: int = 100):
    return db.query(Seat).filter(Seat.auditorium_id == auditorium_id).offset(skip).limit(limit).all()

async def create_seat(db: Session, code: str, auditorium_id: str):
    db_seat = Seat(code=code, auditorium_id=auditorium_id)
    db.add(db_seat)
    db.commit()
    db.refresh(db_seat)
    return db_seat

def get_seat_by_code(db: Session, code: str, auditorium_id: str):
    return db.query(Seat).filter(Seat.code == code, Seat.auditorium_id == auditorium_id).first()