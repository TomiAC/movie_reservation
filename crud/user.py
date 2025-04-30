from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate, UserEmail

async def create_user(db: Session, new_user: UserCreate):
    check_user = db.query(User).filter(new_user.email==User.email).first()
    if check_user:
        return None
    
    registered_user = User(**new_user.model_dump())
    db.add(registered_user)
    db.commit()
    db.refresh(registered_user)
    return registered_user

def get_user(db: Session, user: str):
    user_search = db.query(User).filter(user==User.email).first()
    return user_search

async def check_credentials(db: Session, email: str, password: str):
    user = db.query(User).filter(email==User.email).first()
    if user and user.password == password:
        return user

async def change_role(db: Session, new_role: str, user_email: UserEmail):
    user = db.query(User).filter(user_email.email==User.email).first()
    user.role = new_role
    db.commit()
    db.refresh(user)
    return user