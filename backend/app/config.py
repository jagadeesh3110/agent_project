from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Executive Search Platform"
    DEBUG: bool = False
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o"

    STEP1_MAX_CONCURRENCY: int = 5
    STEP1_TIMEOUT_SECONDS: int = 120

    class Config:
        env_file = ".env"


settings = Settings()
