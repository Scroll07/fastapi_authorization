from enum import StrEnum


class UserRoles(StrEnum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"
    GUEST = "guest"