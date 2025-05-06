from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from crud.user import get_user, create_user, check_credentials, update_password, update_email, change_role, delete_user
from schemas import UserCreate, UserEmail, UserRead, UserPassword, UserRole
from dependencies import get_db, create_access_token, create_refresh_token, get_current_user, has_role
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta
import jwt
import os
from hashing import hash_password

SECRET_KEY = os.getenv("SECRET_KEY", "clave_por_defecto_si_no_hay_env")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

auth_router = APIRouter(prefix="/auth", tags=["User"])

@auth_router.post("/register", response_model=UserRead)
async def register_user_route(user: UserCreate, db: Session = Depends(get_db)):
    user.password = hash_password(user.password)
    new_user = await create_user(db, user)
    if not new_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return new_user

@auth_router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:Session = Depends(get_db)):
    user = await check_credentials(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": user.email}
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@auth_router.post("/refresh")
async def refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        new_access_token = create_access_token({"sub": username})
        return {"access_token": new_access_token}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token has expired")
    except:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
@auth_router.put("/email")
async def update_email_route(new_email: UserEmail, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return await update_email(db, new_email.email, current_user)

@auth_router.put("/password")
async def update_password_route(passwords: UserPassword, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    user = await check_credentials(db, current_user, passwords.old_password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect password")
    new_password = hash_password(passwords.new_password)
    return await update_password(db, new_password, current_user)

@auth_router.put("/role")
async def change_role_route(new_role: UserRole, db: Session = Depends(get_db), current_user: str = Depends(has_role("admin"))):
    if new_role.role not in ["admin", "user", "guest"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    return await change_role(db, new_role.role, new_role.promoted_user)

@auth_router.delete("/user")
async def delete_user_route(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return await delete_user(db, current_user)