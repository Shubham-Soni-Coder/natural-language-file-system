from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    # AI
    GEMINI_API_KEY: str | None = None
    GEMINI_MODEL:str | None = None

    # Database
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    # Logging (with default fallbacks)
    LOG_LEVEL: str = "INFO"
    LOG_FILE_PATH: str = "app.log"

    # folder path
    FOLDER_PATH:str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Prevents crashing on extra .env variables
    )


settings = Settings()
