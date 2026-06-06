from fastapi.routing import APIRouter
from fastapi import Depends, Form, HTTPException

from src.dependencies import get_db
from src.dao.user_dao import UserDao
from src.schemas.db_schema import UserFields
from src.security import PasswordService

web_users = APIRouter()

@web_users.post("/register", status_code=201)
async def register(
    email: str = Form(..., ), #add validation
    password: str = Form(..., ), #add validation
    db = Depends(get_db),
):
    dao = UserDao(session=db)
    user = await dao.get_user_by_field(field=UserFields.EMAIL, value=email)
    if user is not None:
        raise HTTPException(409, "User with this email already exists")
    password_hash = PasswordService.hash_password(password=password)
    
    user = await dao.create_user(email=email, password_hash=password_hash)
    
    #create_session for user
    
    
    
    