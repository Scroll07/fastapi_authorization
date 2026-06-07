from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.schemas.db_schema import UserFields
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
        await self.session.flush()
        await self.session.commit()
        return user #CREATE SESSION
    
    async def get_user_by_field(
        self, 
        field: UserFields,
        value: str | int
    ) -> Users | None:
        column = getattr(Users, field)
        query = select(Users).where(column == value)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        return user
    
    
    
    