from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence

from src.models.models import Resources
from src.schemas.api_schema import ResourceNames


class ResourceDAO:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        
    async def _get_resources(self) -> Sequence[Resources]:
        qeury = select(Resources)
        result = await self.session.execute(qeury)
        roles = result.scalars().all()
        return roles

    async def _create_resources(self) -> list[Resources]:
        res_names = [r.value for r in ResourceNames]
        resources = []
        for r in res_names:
            resource = Resources(name=r)
            self.session.add(resource)
            resources.append(resource)
        return resources
        
    async def initialize_resources(self) -> list[Resources] | None:
        resuorces = await self._get_resources()
        if resuorces:
            return None
        return await self._create_resources()