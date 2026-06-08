from enum import StrEnum

from pydantic import BaseModel, EmailStr


class UserRoles(StrEnum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"
    GUEST = "guest"
    
class UserFields(StrEnum):
    ID = "id"
    EMAIL = "email"
    
class UserCreateData(BaseModel):
    first_name: str 
    last_name: str
    middle_name: str
    email: EmailStr
    password_hash: str