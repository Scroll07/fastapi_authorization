from datetime import datetime
from typing import Literal
from pydantic import BaseModel


class JWTDecodedData(BaseModel):
    sub: int
    sid: int
    exp: datetime
    
token_types = Literal["access", "refresh"]
    
class Token(BaseModel):
    token: str
    type: token_types