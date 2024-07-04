from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path

ENV_PATH = Path(__file__).parent.parent.parent / '.env'
ENV_PATH_TEST = Path(__file__).parent.parent.parent / '.test.env'


class Setting(BaseSettings):
    MODE: str
    DB_HOST: str = Field(validation_alias='DB_HOST')
    DB_PORT: int
    DB_USER: str
    DB_DATABASE: str
    DB_PASSWORD: str
    ECHO: bool

    model_config = SettingsConfigDict(env_file=(ENV_PATH,))

    @property
    def host_database_sqlalchemy(self):
        """postgresql+asyncpg://user:password@localhost:5432/dbname"""
        return (f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:'
                f'{self.DB_PORT}/{self.DB_DATABASE}')


class SettingTest(Setting):
    model_config = SettingsConfigDict(env_file=(ENV_PATH_TEST,))


class Configs:

    @property
    @lru_cache()
    def test(self):
        return SettingTest()

    @property
    @lru_cache()
    def prod(self):
        return Setting()


setting = Configs()
