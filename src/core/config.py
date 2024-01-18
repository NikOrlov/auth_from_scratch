from pydantic_settings import BaseSettings
from pydantic import BaseModel
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = Path(BASE_DIR, 'certs', 'jwt-private.pem')
    public_key_path: Path = Path(BASE_DIR, 'certs', 'jwt-public.pem')
    algorithm: str = 'RS256'
    access_token_expire_minutes: int = 15
    refresh_token_expire_minutes: int = 300
    token_type: str = 'Bearer'


class Settings(BaseSettings):
    PROJECT_NAME: str = ...

    POSTGRES_HOST: str = 'localhost'
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = 'users'
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = ...
    POSTGRES_SCHEME: str = 'postgresql+asyncpg'
    AUTH_JWT: AuthJWT = AuthJWT()

    @property
    def PG_DSN_ASYNC(self):
        return f'{self.POSTGRES_SCHEME}://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'

    class Config:
        env_file = '.env'


settings = Settings()
