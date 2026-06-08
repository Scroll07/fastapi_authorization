from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field, field_validator, validate_email, EmailStr


class JWTDecodedData(BaseModel):
    sub: str
    sid: int
    exp: int
    
token_types = Literal["access", "refresh"]
    
class Token(BaseModel):
    token: str
    type: token_types
    
    
class RegisterRequestData(BaseModel):
    first_name: str 
    last_name: str
    middle_name: str
    email: EmailStr
    password: str
    
    @field_validator('first_name')
    def validate_fisrt_name(cls, value: str):
        value = value.strip()
        if " " in value:
            raise ValueError("String must not contain spaces")
        return value
    
    @field_validator('last_name')
    def validate_last_name(cls, value: str):
        value = value.strip()
        if " " in value:
            raise ValueError("String must not contain spaces")
        return value
    
    @field_validator('middle_name')
    def validate_middle_name(cls, value: str):
        value = value.strip()
        if " " in value:
            raise ValueError("String must not contain spaces")
        return value
    
    @field_validator('password')
    def validate_password(cls, value: str):
        value = value.strip()
        if " " in value:
            raise ValueError("Password must not contain spaces")
        return value
    
