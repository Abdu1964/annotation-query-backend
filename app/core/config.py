import os
import secrets
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, field_validator
import yaml

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Annotation Query Backend"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    # Redis
    REDIS_URL: str = "redis://redis:6379/0"
    REDIS_EXPIRATION: int = 3600

    # Mail
    MAIL_SERVER: Optional[str] = None
    MAIL_PORT: Optional[int] = None
    MAIL_USE_TLS: bool = False
    MAIL_USE_SSL: bool = False
    MAIL_USERNAME: Optional[str] = None
    MAIL_PASSWORD: Optional[str] = None
    MAIL_DEFAULT_SENDER: Optional[str] = None

    # Database
    DATABASE_TYPE: str = "cypher"

    # Elasticsearch
    ES_URL: Optional[str] = None
    ES_API_KEY: Optional[str] = None
    
    # App
    APP_PORT: int = 8000
    
    # Auth
    JWT_SECRET: Optional[str] = None
    SECRET_KEY: Optional[str] = None # Legacy support
    
    # Mongo
    MONGO_URI: Optional[str] = None
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore" # Allow extra env vars without validation error

    @field_validator("DATABASE_TYPE", mode="before")
    @classmethod
    def load_db_type_from_yaml(cls, v):
        # Fallback to loading from yaml if not set, or override? 
        # Existing app loads from config/config.yaml
        try:
            config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'config.yaml')
            if os.path.exists(config_path):
                with open(config_path, 'r') as file:
                    config = yaml.safe_load(file)
                    if config and 'database' in config and 'type' in config['database']:
                        return config['database']['type']
        except Exception:
            pass
        return v

settings = Settings()
