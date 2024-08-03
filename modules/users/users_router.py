from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from Salary_Calculation.shared.models_schemas.schemas import Token, TokenRefresh, UserCreate
from Salary_Calculation.shared.models_schemas.models import User
from Salary_Calculation.modules.auth.authorizations import get_admin
from .users_controller import signup, login, get_users, refresh_access_token
from typing import List

router = APIRouter()

@router.post("/signup", response_model=Token)
async def signup_endpoint(user:UserCreate):
    return await signup(user)

@router.post("/signin", response_model=Token)
async def login_endpoint(form_data:OAuth2PasswordRequestForm=Depends()):
    return await login(form_data)

@router.post("/refresh", response_model=Token)
async def refresh_access_token_endpoint(token_refresh:TokenRefresh):
    return await refresh_access_token(token_refresh)

@router.get("/users", response_model=List[User], dependencies=[Depends(get_admin)])
async def get_users_endpoints():
    return await get_users()