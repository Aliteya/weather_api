from pydantic_settings import  BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: str
    DB_HOST: str
    API_KEY: str

    model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.env"), extra="ignore")

    def get_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
settings = Settings()
