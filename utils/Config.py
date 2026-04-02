from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    # ai 
    GEMINI_API_KEY : str 
 
    # Db 
    DB_USER : str
    DB_PASSWORD : str
    DB_HOST : str
    DB_PORT : int 
    DB_NAME: str

    # log 
    LOG_LEVEL :  str
    LOG_FILE_PATH : str


    model_config = SettingsConfigDict(env_file=".env")



settings = Settings()