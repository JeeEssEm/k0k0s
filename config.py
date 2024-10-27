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

    S3_ACCESS_KEY_ID: str = 'VmhtJUnARhUxhfr5ESwH'
    S3_SECRET_ACCESS_KEY: str = '1kXBbusINVTQVsjvebupg3sx5D3kj2JlMmCaTaO8'
    S3_ENDPOINT: str = 'http://127.0.0.1:9000'


settings = Settings()


def get_database_url():
    return 'sqlite+aiosqlite:///./db.sqlite'
