from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from shared.models_schemas.schemas import Token, TokenRefresh, UserCreate, SignupResponse
from shared.models_schemas.models import User
from modules.auth.authorizations import get_admin, get_superadmin
from .users_controller import signup, login, get_all_users, refresh_access_token, verify_email, delete_user
from typing import List

router = APIRouter()

@router.post("/signup", response_model=SignupResponse)
async def signup_endpoint(user:UserCreate):
    return await signup(user)

@router.post("/signin", response_model=Token)
async def login_endpoint(form_data:OAuth2PasswordRequestForm=Depends()):
    return await login(form_data)

@router.post("/refresh", response_model=Token)
async def refresh_access_token_endpoint(token_refresh:TokenRefresh):
    return await refresh_access_token(token_refresh)

@router.get("/verify_email/{token}")
async def verify_email_endpoint(token:str):
    return await verify_email(token)


@router.delete("/users/{email}", dependencies=[Depends(get_superadmin)])
async def delete_user_endpoint(email:str):
    return await delete_user(email)

@router.get("/users", response_model=List[User], dependencies=[Depends(get_admin)])
async def get_all_users_endpoints():
    return await get_all_users()