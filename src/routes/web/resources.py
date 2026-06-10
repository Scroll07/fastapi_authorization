from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.routing import APIRouter
from fastapi import Depends, Form, HTTPException
from pydantic import ValidationError

from src.dependencies import get_db, verify_user
from src.core.ressource_access import ResourceAccess
from src.schemas.api_schema import ResourceNames



web_resources = APIRouter()


@web_resources.get("/admin-page")
async def get_admin_page(
    db: AsyncSession = Depends(get_db),
    data = Depends(verify_user)    
):
    resource_name = ResourceNames.ADMINS
    resource_access = ResourceAccess(session=db, resource_name=resource_name)
    rule = await resource_access.get_rule(user_id=int(data.sub))
    if not rule or not rule.can_read:
        raise HTTPException(403, "You do not have permisiion to read this page")
    
    return "Admin page"    