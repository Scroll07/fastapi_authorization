from datetime import datetime, timezone

from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__="users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column()
    password_hash: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))

class Roles(Base):
    __tablename__="roles"

    id:
    name:

class Sessions(Base):
    __tablename__="sessions"

    id:
    user_id:
    expires_at:
    is_active:
    created_at:
        
class Resources(Base):
    __tablename__="resources"

    id:
    name:
    is_public:

class AccessRules(Base):
    __tablename__="access_rules"
    
    id:
    role_id:
    user_id:
    resource_id:
    can_read:
    can_create:
    can_update:
    can_delete:
    