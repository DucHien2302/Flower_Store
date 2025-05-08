from fastapi import Depends
from sqlalchemy.orm import Session
from auth.authentication import get_user_dependency
from models.models import Informations as Info, SysUser
from schemas.informations import CreateInformation, UpdateInformation, ReponseInformation
from globals import sessions

def create_information(
        db: Session, 
        information: CreateInformation,
        user_id: int = Depends(get_user_dependency(sessions))
    ): 
    db_information = Info(
        first_name=information.first_name,
        last_name=information.last_name,
        full_name= information.first_name + " " + information.last_name,
        date_of_birth=information.date_of_birth,
        address=information.address,
        gender = information.gender,
        user_id=user_id
    )
    db.add(db_information)
    db.commit()
    db.refresh(db_information)
    return db_information

def update_information(db: Session, information_id: int, information: UpdateInformation):
    db_information = db.query(Info).filter(Info.id == information_id).first()
    if db_information:
        db_information.first_name = information.first_name
        db_information.last_name = information.last_name
        db_information.full_name = information.first_name + " " + information.last_name
        db_information.date_of_birth = information.date_of_birth
        db_information.address = information.address
        db.commit()
        db.refresh(db_information)
    return db_information

def get_information_by_user_id(db: Session, user_id: int):
    db_information = db.query(Info).filter(Info.user_id == user_id).first()
    db_user = db.query(SysUser).filter(SysUser.id == user_id).first()
    if db_information is None or db_user is None:
        return None
    
    res_info = ReponseInformation(
        id=db_information.id,
        first_name=db_information.first_name,
        last_name=db_information.last_name,
        full_name=db_information.full_name,
        date_of_birth=db_information.date_of_birth,
        gender = "Male" if db_information else "Female",
        address=db_information.address,
        user_id=db_information.user_id,
        email=db_user.email,
        password=db_user.password
    )
    return res_info