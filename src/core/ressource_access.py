from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.api_schema import ResourceNames
from src.schemas.db_schema import UserFields
from src.dao.user_dao import UserDao
from src.dao.rules_dao import RulesDao
from src.dao.resource_dao import ResourceDAO
from src.models.models import AccessRules

class ResourceAccess:
    def __init__(self, session: AsyncSession, resource_name: ResourceNames) -> None:
        self.session = session
        self.resource_name = resource_name
        
    async def get_rule(self, user_id: int) -> AccessRules | None:
        user_dao = UserDao(session=self.session)
        rules_dao = RulesDao(session=self.session)
        resource_dao = ResourceDAO(session=self.session)
        user = await user_dao.get_user_by_field(field=UserFields.ID, value=user_id)
        if not user:
            raise ValueError(f"User with such id does not exist - id={user_id}")
        resource = await resource_dao.get_resource(resource_name=self.resource_name)
        if not resource:
            raise ValueError(f"Resource with such name does not exist")
        
        rule = await rules_dao.get_rule(role_id=user.role_id, resource_id=resource.id)
        return rule
        