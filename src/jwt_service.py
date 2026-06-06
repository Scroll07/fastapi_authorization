from datetime import datetime, timedelta, timezone
import jwt

from src.schemas.api_schema import JWTDecodedData, Token
from src.settings import settings as s, ACCESS_TOKEN_EXPIRE_IN_MIN

class JWT_Service:
    def __init__(
        self,
        secret_key: str,
        algoritm: str,
        access_token_expire_in_min: int
    ) -> None:
        self.secret_key = secret_key
        self.algoritm = algoritm
        self.access_expire = access_token_expire_in_min
        
    def create_access_token(self, data: JWTDecodedData) -> str:
        encoded = jwt.encode(data.model_dump(), self.secret_key, self.algoritm)
        return encoded            
    
    def decode_token(self, token: str) -> JWTDecodedData:
        payload = jwt.decode(token, self.secret_key, algorithms=[self.algoritm])
        data = JWTDecodedData.model_validate(payload)
        return data



jwt_service = JWT_Service(
    secret_key=s.SECRET_KEY,
    algoritm="SHA256",
    access_token_expire_in_min=ACCESS_TOKEN_EXPIRE_IN_MIN
)
                