from uuid import UUID
from pydantic import BaseModel


class TokenPayload(BaseModel):
    sub: UUID
    login: str


class TokenInfo(BaseModel):
    access_token: bytes
    token_type: str
