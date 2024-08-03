from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from Salary_Calculation.shared.models_schemas.models import Login
from Salary_Calculation.config.database.database import user_collection
from .users_crud import create_user, get_user_by_email, get_all_user
from Salary_Calculation.shared.models_schemas.schemas import TokenData, UserCreate, TokenRefresh
from Salary_Calculation.modules.auth.authentication import create_access_token, verify_password, create_refresh_token

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_ECPIRE_DAYS = 7


exception_error = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, 
                        detail="could not validate credentials",
                        headers={"WWW-Authenticate": "Bearer"},)
        
async def signup(user:UserCreate):
    db_user = await get_user_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registerd")
    user_obj = await create_user(user)
    access_token = create_access_token(data={"sub":user_obj.email, "role":user.role})
    return {"message":"user created"}
    
    

async def login(form_data: Login):
    user = await get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, 
                        detail="incorrect email or password",
                        headers={"WWW-Authenticate": "Bearer"},)
    
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub":user.email, "role":user.role}, expire_delta=access_token_expires)
    
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_ECPIRE_DAYS)
    refresh_token = create_refresh_token(data={"sub":user.email, "role":user.role}, expire_delta=refresh_token_expires)

    return {"access_token":access_token, "refresh_token":refresh_token, "token_type":"bearer"} 
    


async def refresh_access_token(token_refresh:TokenRefresh):
    try:
        payload = jwt.decode(token_refresh.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email : str = payload.get("sub")
        role : str = payload.get("sub")
        if not email or not role:
            raise exception_error
        token_data = TokenData(email=email, role=role)
    except JWTError:
        raise exception_error
    
    user = await user_collection.find_one({"email":token_data.email})
    if user is None:
        raise exception_error
    
    # check if the refresh token has expired 
    now = datetime.now(timezone.utc)
    if now >  datetime.utcfromtimestamp(payload["exp"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expires")
        

    # generate new access and refresh token 
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub":user.email, "role":user.role}, expire_delta=access_token_expires)
    
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_ECPIRE_DAYS)
    refresh_token = create_refresh_token(data={"sub":user.email, "role":user.role}, expire_delta=refresh_token_expires)

    return {"access_token":access_token, "refresh_token":refresh_token, "token_type":"bearer"} 
    

async def get_users():
    users = await get_all_user()
    return users
