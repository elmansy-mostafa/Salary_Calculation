from fastapi import Depends, HTTPException
from .authentication import get_current_user
from Salary_Calculation.shared.models_schemas.models import User

exception_error = HTTPException(status_code=403, detail="not enough permissions")


def  get_current_active_user(current_user:User=Depends(get_current_user)):        
    return current_user

def get_superadmin(current_user:User=Depends(get_current_active_user)):
    if current_user.role != "superadmin":
        raise exception_error
    return current_user
    
def get_admin(current_user:User=Depends(get_current_active_user)):
    if current_user.role not in ["superadmin", "admin"]:
        raise exception_error
    return current_user