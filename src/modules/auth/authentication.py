from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from shared.models_schemas.schemas import TokenData


exception_error = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, 
                        detail="could not validate credentials",
                        headers={"WWW-Authenticate": "Bearer"},)


# secret key for JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_ECPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password:str, hashed_password:str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password:str) -> str:
    return pwd_context.hash(password)

def create_access_token(data:dict, expire_delta:Optional[timedelta] = None):
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data:dict, expire_delta:Optional[timedelta] = None):
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_ECPIRE_DAYS)
    
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
        
        
def create_verification_token(email:str) ->str:
    expire = datetime.now(timezone.utc) + timedelta(hours=1)
    to_encode = {"email":email, "exp":expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_verification_token(token:str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("email")
    except ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token expired")
    except InvalidTokenError:
        raise HTTPException(status_code=400, detail=" Invalid token")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token:str = Depends(oauth2_scheme)):
    try:
        return decode_access_token(token)
    except JWTError:
        raise exception_error
    
