from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence

from src.models.models import Roles
from src.schemas.db_schema import UserRoles


class RoleDAO:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        
    async def _get_roles(self) -> Sequence[Roles]:
        qeury = select(Roles)
        result = await self.session.execute(qeury)
        roles = result.scalars().all()
        return roles

    async def _create_roles(self):
        user_roles = [r.value for r in UserRoles]
        for r in user_roles:
            role = Roles(name=r)
            self.session.add(role)
        await self.session.commit()
        
    async def create_basic_roles(self) -> None:
        try:
            roles = await self._get_roles()
            if roles:
                return None
            await self._create_roles()
        except Exception:
            await self.session.rollback()