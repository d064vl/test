from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

# Get .env-File
class BaseConfig(BaseSettings):
    ENV_STATE: Optional[str] = None # Optional ? .env.ENV_STATE : None

    """Loads the dotenv file. Including this is necessary to get
    pydantic to load a .env file."""
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

# Get (var) from .env-file
class GlobalConfig(BaseConfig):
    DATABASE_URL: Optional[str] = None # Optional ? .env.DATABASE_URL : None
    DB_FORCE_ROLL_BACK: bool = False
    KAFKA_TOPIC_NAME: Optional[str] = None
    KAFKA_SERVER: Optional[str] = None
    KAFKA_PORT: Optional[str] = None


# Dev
class DevConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="DEV_") # Get (var) Prefix (DEV_)

# Prod
class ProdConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="PROD_") # Get (var) Prefix (PROD_)

# Test
class TestConfig(GlobalConfig):
    # Default values, If No exist
    DATABASE_URL: str = "sqlite:///test.db"
    DB_FORCE_ROLL_BACK: bool = False

    model_config = SettingsConfigDict(env_prefix="TEST_") # Get (var) Prefix (TEST_)


@lru_cache() # cache Call Fun
def get_config(env_state: str):
    """Instantiate config based on the environment."""
    configs = {"dev": DevConfig, "prod": ProdConfig, "test": TestConfig}
    return configs[env_state]()

# fnc external called
config = get_config(
                    BaseConfig().ENV_STATE # Call BaseConfig usig ENV_STATE from .env-file
                    )