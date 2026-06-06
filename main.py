from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.database import async_engine, async_session
from src.dao.role_dao import RoleDAO

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_session() as session:
        dao = RoleDAO(session=session)
        await dao.create_basic_roles()
    
    yield
    
    await async_engine.dispose()


app = FastAPI(lifespan=lifespan)


