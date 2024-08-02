# from dotenv import load_dotenv
# from pydantic_settings import BaseSettings
# from pathlib import Path
# import os

# # Load environment variables from the .env file
# dotenv_path = Path(__file__).resolve().parent.parent / 'config' / 'env' / '.env'
# load_dotenv(dotenv_path)

# class Settings(BaseSettings):
#     DATABASE_URL: str
#     SECRET_KEY: str
#     ALGORITHM: str
#     ACCESS_TOKEN_EXPIRE_MINUTES: int

#     class Config:
#         # This tells pydantic to use the environment variables directly
#         env_file = None

# settings = Settings()

# print("DATABASE_URL:", settings.DATABASE_URL)
# print("SECRET_KEY:", settings.SECRET_KEY)
# print("ALGORITHM:", settings.ALGORITHM)
# print("ACCESS_TOKEN_EXPIRE_MINUTES:", settings.ACCESS_TOKEN_EXPIRE_MINUTES)