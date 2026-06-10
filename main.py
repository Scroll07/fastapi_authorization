from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.database import async_engine, async_session
from src.dao.role_dao import RoleDAO
from src.dao.resource_dao import ResourceDAO
from src.dao.rules_dao import RulesDao

from src.routes.web.users import web_users
from src.routes.web.resources import web_resources


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_session() as session:
        roles_dao = RoleDAO(session=session)
        resources_dao = ResourceDAO(session=session)
        rules_dao = RulesDao(session=session)
        
        roles = await roles_dao.initialize_roles()
        resources = await resources_dao.initialize_resources()
        if roles is not None and resources is not None:
            await session.flush()
            await rules_dao.initialize_rules(roles=roles, resources=resources)
        
        await session.commit()
        
        
        
    yield
    
    await async_engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(web_users, prefix="/web", tags=["USERS", "WEB"])
app.include_router(web_resources, prefix="/web", tags=["RESOURCES", "WEB", "ADMIN"])


