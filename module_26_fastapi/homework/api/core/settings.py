import os
import sys
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path

ENV_PATH = Path(__file__).parent.parent.parent / '.env'
ENV_PATH_TEST = Path(__file__).parent.parent.parent / '.test.env'


class BaseAppSettings(BaseSettings):
    MODE: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_DATABASE: str
    DB_PASSWORD: str
    ECHO: bool

    @property
    def host_database_sqlalchemy(self):
        return (f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:'
                f'{self.DB_PORT}/{self.DB_DATABASE}')


class ProdSettings(BaseAppSettings):
    model_config = SettingsConfigDict(env_file=ENV_PATH)


class TestSettings(BaseAppSettings):
    model_config = SettingsConfigDict(env_file=ENV_PATH_TEST)


class Configs:
    @lru_cache()
    def get_settings(self):
        env = os.getenv('MODE')
        if env == 'test' or 'pytest' in sys.modules:
            return TestSettings()
        return ProdSettings()


settings = Configs().get_settings()
