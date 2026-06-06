from datetime import datetime, timezone

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from dao.user_dao import UserDao
from schemas.db_schema import UserFields
from src.schemas.api_schema import JWTDecodedData
from src.database import async_session
from src.jwt_service import jwt_service
from src.dao.session_dao import SessionDao



async def get_db():
    async with async_session() as session:
        yield session
        
security = HTTPBearer()


    

async def verify_user(
    db = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> JWTDecodedData:
    try:
        token_data = jwt_service.decode_token(token=credentials.credentials)
    except Exception:
        raise HTTPException(401, "Wrong token")
    try:
        user_dao = UserDao(session=db)
        user = await user_dao.get_user_by_field(field=UserFields.ID, value=token_data.sub)
        if user is None:
            raise HTTPException(401, "Wrong user data")
        if not user.is_active:
            raise HTTPException(401, "This accaunt is not active")
        
        dao = SessionDao(session=db)
        session = await dao.get_session(session_id=token_data.sid)
        if session is None:
            raise HTTPException(401, "Wrong session id, session does not exists")
        if not session.is_active:
            raise HTTPException(403, "Session was expired, try to login")
    
        now = datetime.now(timezone.utc)
        if now > session.expires_at:
            raise HTTPException(401, "Token was expired")
    
        return token_data
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(500, "Internal server error")
        
    