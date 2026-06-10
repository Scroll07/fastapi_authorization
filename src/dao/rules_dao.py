from datetime import datetime
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.models import AccessRules, Roles, Resources
from src.schemas.api_schema import ResourceNames
from src.schemas.db_schema import UserRoles


PERMISSION_MATRIX: dict[UserRoles, dict[ResourceNames, dict[str, bool]]] = {
    UserRoles.USER: {
        ResourceNames.USER: {
            "can_read": True,
            "can_update": True,
            "can_delete": True
        },
        ResourceNames.ADMINS: {}
    },
    UserRoles.ADMIN: {
        ResourceNames.USER: {
            "can_read": True,
            "can_create": True,
            "can_update": True,
            "can_delete": True    
        },
        ResourceNames.ADMINS: {
            "can_read": True,
            "can_create": True,
            "can_update": True,
            "can_delete": True    
        }
    },
    UserRoles.MANAGER: {
        ResourceNames.USER: {
            "can_read": True,
            "can_update": True,
        },
        ResourceNames.ADMINS: {
            "can_read": True,
        }
    },
    UserRoles.GUEST: {
        ResourceNames.USER: {},
        ResourceNames.ADMINS: {}
    }
}




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
    
    async def _get_all_rules(self) -> Sequence[AccessRules]:
        query = select(AccessRules)
        result = await self.session.execute(query)
        rules = result.scalars().all()
        return rules
    
    async def initialize_rules(self, roles: list[Roles], resources: list[Resources]) -> None:
        rules_sould_be = len(UserRoles) * len(ResourceNames)
        rules = await self._get_all_rules()
        if len(rules) < rules_sould_be:
            return None
        
        roles_map = {r.name: r for r in roles}
        resources_map = {r.name: r for r in resources}
        for role_name, permisions in PERMISSION_MATRIX.items():
            role = roles_map.get(role_name)
            if not role:
                continue
            for resource_name, perms in permisions.items():
                resource = resources_map.get(resource_name)
                if not resource:
                    continue
                await self.create_rule(
                    role_id=role.id,
                    resource_id=resource.id,
                    can_read=perms.get("can_read", False),
                    can_create=perms.get("can_create", False),
                    can_update=perms.get("can_update", False),
                    can_delete=perms.get("can_delete", False)
                )