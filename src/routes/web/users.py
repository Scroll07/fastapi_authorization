from datetime import datetime, timedelta, timezone

from fastapi.routing import APIRouter
from fastapi import Depends, Form, HTTPException

from src.dependencies import get_db
from src.dao.user_dao import UserDao
from src.schemas.db_schema import UserFields
from src.schemas.api_schema import JWTDecodedData
from src.security import PasswordService
from src.jwt_service import jwt_service
from src.dao.session_dao import SessionDao
from src.settings import ACCESS_TOKEN_EXPIRE_IN_MIN




web_users = APIRouter()

@web_users.post("/register", status_code=201)
async def register(
    email: str = Form(..., ), #add validation
    password: str = Form(..., ), #add validation
    db = Depends(get_db),
):
    user_dao = UserDao(session=db)
    user = await user_dao.get_user_by_field(field=UserFields.EMAIL, value=email)
    if user is not None:
        raise HTTPException(409, "User with this email already exists")
    password_hash = PasswordService.hash_password(password=password)
    
    user = await user_dao.create_user(email=email, password_hash=password_hash)
    
    return {
        "ok": True,
        "detail": "Account was successfully created",
    }    
    


@web_users.post("/login")
async def login(
    email: str = Form(..., ), #add validation
    password: str = Form(..., ), #add validation
    db = Depends(get_db),
):
    user_dao = UserDao(session=db)
    user = await user_dao.get_user_by_field(field=UserFields.EMAIL, value=email)
    if user is None:
        raise HTTPException(401, "Wrong user data")
    
    if not PasswordService.verify_password(password=password, hashed_password=user.password_hash):
        raise HTTPException(401, "Wrong user data")
    
    session_dao = SessionDao(session=db)
    expires = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_IN_MIN)
    user_session = await session_dao.create_session(user_id=user.id, expires_at=expires)
    token_data = JWTDecodedData(
        sub=user.id,
        sid=user_session.id,
        exp=expires
    )
    token = jwt_service.create_access_token(data=token_data)
    
    
    return {
        "ok": True,
        "detail": "Login successful",
        "access_token": token
    }    
    


    
    