from datetime import datetime, timezone
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship

from src.schemas.db_schema import UserRoles


class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__="users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    middle_name: Mapped[str]
    email: Mapped[str]
    password_hash: Mapped[str]
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True) ,default=lambda: datetime.now(timezone.utc))

class Roles(Base):
    __tablename__="roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[UserRoles]

class Sessions(Base):
    __tablename__="sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
        
class Resources(Base):
    __tablename__="resources"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    is_public: Mapped[bool] = mapped_column(default=False)

class AccessRules(Base):
    __tablename__="access_rules"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    resource_id: Mapped[int] = mapped_column(ForeignKey("resources.id"))
    can_read: Mapped[bool] = mapped_column(default=False)
    can_create: Mapped[bool] = mapped_column(default=False)
    can_update: Mapped[bool] = mapped_column(default=False)
    can_delete: Mapped[bool] = mapped_column(default=False)
    