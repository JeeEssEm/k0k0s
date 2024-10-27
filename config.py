from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = 'localhost'
    DB_PORT: int = 0
    DB_NAME: str = 'db'
    DB_USER: str = 'pguser'
    DB_PASSWORD: str = 'password'
    INIT_MODELS: bool = True
    HOST: str = '127.0.0.1'
    PORT: int = 8000

    ALGORITHM: str = 'HS256'
    VERIFIED: bool = True
    SECRET_KEY: str = 'NON-SECRET-KEY'
    REFRESH_TOKEN_EXPIRES: int = 30
    ACCESS_TOKEN_EXPIRES: int = 30

    S3_ACCESS_KEY_ID: str = 'access key'
    S3_SECRET_ACCESS_KEY: str = 'secret key'
    S3_ENDPOINT: str = 'endpoint url'


settings = Settings()


def get_database_url():
    return 'sqlite+aiosqlite:///./db.sqlite'
