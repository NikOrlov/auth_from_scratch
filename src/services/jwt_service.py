from functools import lru_cache
from datetime import datetime, timedelta
import jwt
from core.config import settings
from models.jwt import TokenInfo


class JWTService:
    @staticmethod
    def encode_jwt(payload: dict,
                   private_key: str = settings.AUTH_JWT.private_key_path.read_text(),
                   algorithm: str = settings.AUTH_JWT.algorithm,
                   expire_minutes: int = settings.AUTH_JWT.access_token_expire_minutes) -> bytes:
        to_encode = payload.copy()
        now = datetime.utcnow()
        expire = now + timedelta(expire_minutes)
        to_encode.update(iat=now,
                         exp=expire)
        encoded = jwt.encode(to_encode, private_key, algorithm)
        return encoded

    @staticmethod
    def create_token(jwt_token: bytes,
                     token_type: str = settings.AUTH_JWT.token_type) -> TokenInfo:
        return TokenInfo(access_token=jwt_token, token_type=token_type)

    @staticmethod
    def decode_jwt(encoded: str | bytes,
                   public_key: str = settings.AUTH_JWT.public_key_path.read_text(),
                   algorithm: str = settings.AUTH_JWT.algorithm):
        decoded = jwt.decode(encoded, public_key, algorithms=[algorithm])
        return decoded


@lru_cache()
def get_jwt_service() -> JWTService:
    return JWTService()
