# Настройки извлекают данные из app/.env
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

ENV = Path(__file__).parent.parent.parent / '.env'


class Settings(BaseSettings):
    postgres_user: str = Field(min_length=3)
    postgres_password: str = Field(min_length=8)
    postgres_host: str
    postgres_port: int
    postgres_db: str

    @property
    def connection_url_to_db(self):
        return (f"postgresql+psycopg2://{self.postgres_user}:"
                f"{self.postgres_password}@{self.postgres_host}:"
                f"{self.postgres_port}/{self.postgres_db}")

    model_config = SettingsConfigDict(env_file=ENV)


def create_setting():
    return Settings()


settings = create_setting()
