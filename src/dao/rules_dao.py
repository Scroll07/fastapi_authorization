from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.models import AccessRules, Roles, Resources
from src.schemas.api_schema import ResourceNames
from src.schemas.db_schema import UserRoles

class RulesDao:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        
    async def create_rule(
        self, 
        role_id: int, 
        resource_id: int,
        can_read: bool = False,
        can_create: bool = False,
        can_update: bool = False,
        can_delete: bool = False,
    ) -> AccessRules:
        new_rule = AccessRules(
            role_id=role_id,
            resource_id=resource_id,
            can_read=can_read,
            can_create=can_create,
            can_update=can_update,
            can_delete=can_delete
        )
        
        self.session.add(new_rule)
        await self.session.flush()
        return new_rule
    
    async def get_rule(self, role_id: int, resource_id: int) -> AccessRules | None:
        query = select(AccessRules).where(AccessRules.role_id==role_id, AccessRules.resource_id==resource_id)
        result = await self.session.execute(query)
        rule = result.scalar_one_or_none()
        return rule
    
    async def initialize_rules(self, roles: list[Roles], resources: list[Resources]) -> None:
        for role in roles:
            for resource in resources:
                if resource.name == ResourceNames.USERS and role.name == UserRoles.USER:
                    await self.create_rule(
                        role_id=role.id, 
                        resource_id=resource.id,
                        can_read=True,
                        can_create=True,
                        can_update=True,
                        can_delete=True
                        )
                    

