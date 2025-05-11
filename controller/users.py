from sqlalchemy.orm import Session
from models.models import SysUser
from schemas.users import UserAuth

def create_user(db: Session, user: UserAuth):
    db_user = SysUser(
        email=user.email,
        password=user.password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(SysUser).filter(SysUser.id == user_id).first()

def authenticate_user(db: Session, user: UserAuth):
    db_user = db.query(SysUser).filter(SysUser.email == user.email).first()
    if db_user is None or db_user.password != user.password:
        return None
    return db_user