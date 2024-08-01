from fastapi import APIRouter, HTTPException, Depends, status
from jose import JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from Salary_Calculation.crud import create_user, get_user_by_email, get_all_user
from Salary_Calculation.schemas import UserCreate, Token, TokenData
from Salary_Calculation.utils import verify_password, create_access_token, decode_access_token
from Salary_Calculation.models import UserInDB
from typing import List

router = APIRouter()

# User endpoints

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token:str = Depends(oauth2_scheme)) -> TokenData:
    try:
        return decode_access_token(token)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="could not validate credentials",
                        headers={"WWW-Authenticate": "Bearer"},)

@router.post("/signup", response_model=Token)
async def signup(user:UserCreate):
    db_user = await get_user_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registerd")
    user_obj = await create_user(user)
    access_token = create_access_token(data={"sub":user_obj.email})
    return {"access_token":access_token, "token_type":"bearer"} 
    

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data:OAuth2PasswordRequestForm=Depends()):
    user = await get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, 
                        detail="incorrect email or password",
                        headers={"WWW-Authenticate": "Bearer"},)
    access_token = create_access_token(data={"sub":user.email})
    return {"access_token":access_token, "token_type":"bearer"} 
    

@router.get("/users", response_model=List[UserInDB])
async def get_users():
    users = await get_all_user()
    return users
