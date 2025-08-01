# app/core/config.py

from pydantic_settings import BaseSettings,SettingsConfigDict

class Config(BaseSettings):
    url: str  # This is the database URL
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')