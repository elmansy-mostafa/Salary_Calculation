from fastapi import HTTPException, status
from Salary_Calculation.shared.models_schemas.models import Login
from .users_crud import create_user, get_user_by_email, get_all_user
from Salary_Calculation.shared.models_schemas.schemas import UserCreate
from Salary_Calculation.modules.auth.authentication import create_access_token, verify_password


        
async def signup(user:UserCreate):
    db_user = await get_user_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registerd")
    user_obj = await create_user(user)
    access_token = create_access_token(data={"sub":user_obj.email, "role":user.role})
    return {"access_token":access_token, "token_type":"bearer"} 
    
    

async def login(form_data: Login):
    user = await get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, 
                        detail="incorrect email or password",
                        headers={"WWW-Authenticate": "Bearer"},)
    access_token = create_access_token(data={"sub":user.email, "role":user.role})
    return {"access_token":access_token, "token_type":"bearer"} 
    
    
async def get_users():
    users = await get_all_user()
    return users
