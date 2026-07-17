from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    ORACLE_USER:str
    ORACLE_PASSWORD:str
    ORACLE_DSN:str
    GROQ_API_KEY: str

    class Config:
        env_file =".env"

settings = Settings()
