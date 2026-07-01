from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=('.env', '../.env'), env_file_encoding='utf8', extra='ignore')
    SECRET_KEY: str
    APP_NAME: str = 'ApplicationApp'
    VERSION: str = '1.0.0'
    HOST: str = '127.0.0.1'
    PORT: int = 8000
    RELOAD: bool = True
    TOKEN_EXPIRES_SECONDS: int = 3600
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    ALLOW_ORIGINS: list[str]
    ALLOW_METHODS: list[str]
    ALLOW_HEADERS: list[str]
    ALLOW_CREDENTIALS: bool

    @property
    def DATABASE_URL(self) -> str:
        return "sqlite+aiosqlite:///applications.db"
    
    @property
    def TEST_DATABASE_URL(self) -> str:
        return "sqlite+aiosqlite:///:memory:"

settings = Settings()
