import os

from pydantic import BaseModel


ACCESS_TOKEN_EXPIRE_IN_MIN = 15

class Settings(BaseModel):
    DB_HOST: str = os.getenv("DB_HOST", default="db") 
    DB_PORT: str = os.getenv("DB_PORT", default="5432") 
    DB_NAME: str = os.getenv("DB_NAME", default="test_db") 
    DB_USER: str = os.getenv("DB_USER", default="test_user") 
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", default="test_password") 

    SECRET_KEY: str = os.getenv("SECRET_KEY", default="test_key")

settings = Settings()

