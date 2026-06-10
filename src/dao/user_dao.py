from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.schemas.db_schema import UserFields, UserCreateData
from src.models.models import Users
from src.schemas.api_schema import PatchRequestData



class UserDao:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_user(
        self,
        data: UserCreateData,
        role_id: int
    ) -> Users:
        user = Users(
            first_name=data.first_name,
            last_name=data.last_name,
            middle_name=data.middle_name,
            email=data.email, 
            password_hash=data.password_hash,
            role_id=role_id
        )
        self.session.add(user)
        await self.session.flush()
        await self.session.commit()
        return user
    
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
    
    async def make_unactive_user(self, user_id: int) -> None:
        user = await self.get_user_by_field(field=UserFields.ID, value=user_id)
        if user is None:
            raise ValueError("Wrong user id")
        user.is_active = False
        # await self.session.commit()
        
    async def patch_user(self, user_id: int, data: PatchRequestData) -> None:
        user = await self.get_user_by_field(field=UserFields.ID, value=user_id)
        if not user:
            raise ValueError(f"User with such id does not exist - {user_id}")
        user.first_name = data.first_name
        user.last_name = data.last_name
        user.middle_name = data.middle_name
        user.email = data.email
        
        return None
    
    
    
    