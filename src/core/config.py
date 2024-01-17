from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = ...

    POSTGRES_HOST: str = 'localhost'
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = 'users'
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = ...
    POSTGRES_SCHEME: str = 'postgresql+asyncpg'

    @property
    def PG_DSN_ASYNC(self):
        return f'{self.POSTGRES_SCHEME}://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'

    class Config:
        env_file = '.env'


settings = Settings()
