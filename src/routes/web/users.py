from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.routing import APIRouter
from fastapi import Depends, Form, HTTPException
from pydantic import ValidationError

from src.dependencies import get_db, verify_user
from src.dao.user_dao import UserDao
from src.schemas.db_schema import UserFields, UserCreateData
from src.schemas.api_schema import JWTDecodedData, RegisterRequestData
from src.security import PasswordService
from src.jwt_service import jwt_service
from src.dao.session_dao import SessionDao
from src.settings import ACCESS_TOKEN_EXPIRE_IN_MIN




web_users = APIRouter()

@web_users.post("/register", status_code=201)
async def register(
    first_name: str = Form(..., min_length=1, max_length=30),
    last_name: str = Form(..., min_length=1, max_length=30),
    middle_name: str = Form(..., min_length=1, max_length=30),
    email: str = Form(..., min_length=6, max_length=50), #add validation
    password: str = Form(..., min_length=6, max_length=30), #add validation
    db: AsyncSession = Depends(get_db),
):
    try:
        user_data = RegisterRequestData(
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            email=email,
            password=password
        )
    except ValidationError as e:
        raise HTTPException(422, e.errors()[0].get("msg"))
    try:
        user_dao = UserDao(session=db)
        user = await user_dao.get_user_by_field(field=UserFields.EMAIL, value=user_data.email)
        if user is not None:
            raise HTTPException(409, "User with this email already exists")
        
        password_hash = PasswordService.hash_password(password=password)
        create_data = UserCreateData(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            middle_name=user_data.middle_name,
            email=user_data.email,
            password_hash=password_hash
        )
        user = await user_dao.create_user(data=create_data)
    
        return {
            "ok": True,
            "detail": "Account was successfully created",
        }    
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(500, "Internal server error")
    


@web_users.post("/login")
async def login(
    email: str = Form(..., ), #add validation
    password: str = Form(..., ), #add validation
    db: AsyncSession = Depends(get_db),
):
    user_dao = UserDao(session=db)
    user = await user_dao.get_user_by_field(field=UserFields.EMAIL, value=email)
    if user is None:
        raise HTTPException(401, "Wrong user data")
    if not user.is_active:
        raise HTTPException(401, "This accaunt is not active")
    
    
    if not PasswordService.verify_password(password=password, hashed_password=user.password_hash):
        raise HTTPException(401, "Wrong user data")
    
    session_dao = SessionDao(session=db)
    expires = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_IN_MIN)
    exp_timestamp = int(expires.timestamp())
    user_session = await session_dao.create_session(user_id=user.id, expires_at=expires)
    token_data = JWTDecodedData(
        sub=str(user.id),
        sid=user_session.id,
        exp=exp_timestamp
    )
    token = jwt_service.create_access_token(data=token_data)
    await db.commit()
    
    return {
        "ok": True,
        "detail": "Login successful",
        "access_token": token
    }    
    

@web_users.post("/logout")
async def logout(
    db: AsyncSession = Depends(get_db),
    data: JWTDecodedData = Depends(verify_user)
):    
    session_dao = SessionDao(session=db)

    await session_dao.make_unactive_session(session_id=data.sid)
    await db.commit()
    
    #probably redirect to other page
    return {
        "ok": True,
        "detail": "Logout successful",
    }    
    

@web_users.delete("/me")
async def soft_delete(
    db: AsyncSession = Depends(get_db),
    data: JWTDecodedData = Depends(verify_user)
):    
    session_dao = SessionDao(session=db)
    await session_dao.make_unactive_session(session_id=data.sid)

    user_dao = UserDao(session=db)
    await user_dao.make_unactive_user(user_id=int(data.sub))
    await db.commit()
    
    #probably redirect to other page
    return {
        "ok": True,
        "detail": "Account was successully deleted",
    }    
    

# @web_users.patch("/me")
# async def patch_user(
#     db: AsyncSession = Depends(get_db),
#     data: JWTDecodedData = Depends(verify_user)
# ):    
#     session_dao = SessionDao(session=db)
#     await session_dao.make_unactive_session(session_id=data.sid)

#     user_dao = UserDao(session=db)
#     assert data.sub is int
#     await user_dao.make_unactive_user(user_id=data.sub)
#     await db.commit()
    
#     #probably redirect to other page
#     return {
#         "ok": True,
#         "detail": "Account was successully deleted",
#     }    
    


    