from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from Salary_Calculation.shared.models_schemas.models import Login
from Salary_Calculation.config.database.database import user_collection
from .users_crud import create_user, get_user_by_email, get_all_user
from Salary_Calculation.config.mailer.email import send_verification_email
from Salary_Calculation.shared.models_schemas.schemas import TokenData, UserCreate, TokenRefresh
from Salary_Calculation.modules.auth.authentication import create_access_token, verify_password, create_refresh_token, create_verification_token, decode_verification_token
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'env', '.env')
load_dotenv(dotenv_path)

SECRET_KEY = os.getenv("SECRET_KEY")
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
    
    await create_user(user)
    
    token = create_verification_token(user.email)
    
    await send_verification_email(user.email, token)
    return {"msg":"Please check your email to verify your account"}
    
    

async def login(form_data: Login):
    user = await get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, 
                        detail="incorrect email or password",
                        headers={"WWW-Authenticate": "Bearer"},)
    if not user.is_verified:
        raise HTTPException(status_code=400, detail="Email is not verified")
    print(user.is_verified)
    
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
    


async def verify_email(token:str):
    
    email = decode_verification_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expire token")
        
    result = await user_collection.update_one({"email":email}, {"$set":{"is_verified":True}})
    if result.matched_count==0:
        raise HTTPException(status_code=400, detail="User not found")

    return {"msg":"Email verified successfully"}



async def delete_user(email:str):
    result = await user_collection.delete_one({"email":email})
    if result.deleted_count == 0:
        raise HTTPException(status_code=400, detail="User not found")
    return {"message":"User deleted successfully"}  


async def get_users():
    users = await get_all_user()
    return users
