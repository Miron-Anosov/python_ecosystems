"""
В этом файле будут секретные данные

Для создания почтового сервиса воспользуйтесь следующими инструкциями

- Yandex: https://yandex.ru/support/mail/mail-clients/others.html
- Google: https://support.google.com/mail/answer/7126229?visit_id=638290915972666565-928115075
"""
import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

ENV_PATH = os.path.abspath(os.path.join('./.env'))
ENV_PATH_2 = os.path.abspath(os.path.join('./flask_app/.env'))


class Settings(BaseSettings):
    smtp_user: str = Field(validation_alias='SMTP_USER')
    smtp_host: str = Field(validation_alias='SMTP_HOST')
    smtp_password: str = Field(validation_alias='SMTP_PASSWORD')
    smtp_port: int = Field(validation_alias='SMTP_PORT')
    broker_url: str
    result_backend: str
    model_config = SettingsConfigDict(env_file=(ENV_PATH, ENV_PATH_2))


setting = Settings()
