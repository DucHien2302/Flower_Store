from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import get_db
from schemas.users import User as UserSchema, UserCreate, UserLogin
from controller.users import create_user, get_user, get_users, authenticate_user

router = APIRouter(
    prefix="/users"
)

@router.get("/", response_model=list[UserSchema])
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{id}", response_model=UserSchema)
async def read_user(id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id=id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserSchema)
async def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db, user=user)
    return db_user

@router.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, email=user.email, password=user.password)
    if db_user is None:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return db_user