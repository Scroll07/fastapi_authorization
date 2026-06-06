from enum import StrEnum


class UserRoles(StrEnum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"
    GUEST = "guest"
    
class UserFields(StrEnum):
    ID = "id"
    EMAIL = "email"