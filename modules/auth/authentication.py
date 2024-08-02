from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from Salary_Calculation.shared.models_schemas.schemas import TokenData
from Salary_Calculation.shared.models_schemas.models import User


exception_error = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, 
                        detail="could not validate credentials",
                        headers={"WWW-Authenticate": "Bearer"},)


# secret key for JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password:str, hashed_password:str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password:str) -> str:
    return pwd_context.hash(password)

def create_access_token(data:dict, expire_delta:Optional[timedelta] = None):
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token:str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email : str = payload.get("sub")
        role : str = payload.get("role")
        if not email or not role:
            raise JWTError
        token_data = TokenData(email=email, role=role)
    except JWTError:
        raise exception_error
    return token_data
        

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token:str = Depends(oauth2_scheme)):
    try:
        return decode_access_token(token)
    except JWTError:
        raise exception_error