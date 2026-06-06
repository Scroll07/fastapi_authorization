from sqlalchemy.ext.asyncio import AsyncSession
from enum import StrEnum

from src.models.models import Users

    


class UserDao:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_user(
        self,
        email: str,
        password_hash: str 
    ) -> Users:
        user = Users(email=email, password_hash=password_hash)
        self.session.add(user)
        await self.session.refresh(user)
        await self.session.flush()
        await self.session.commit()
        return user
    
    
    
    
    