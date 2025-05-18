from sqlalchemy.orm import Session
from models.models import SysUserRole

def create_sysuserrole(db: Session, userId: int):
    db_sysUserRole = SysUserRole(
        user_id = userId,
        role_id = 1 # value 1: is customer
    )
    db.add(db_sysUserRole)
    db.commit()
    db.refresh(db_sysUserRole)
    return db_sysUserRole