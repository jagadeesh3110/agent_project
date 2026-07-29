from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Executive Search Platform"
    DEBUG: bool = False
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"


settings = Settings()
