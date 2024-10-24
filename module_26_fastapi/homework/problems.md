#### Pytest problems:

Что бы тесты запускались нужно распаковывать с дополнительными библиотеками: <br>
> pip install pytest[anyio] <br>
> pip install tri

        Так же необходимо сознать в корне __init__.py для того что бы тесты запускались без ошибки ModuleError

Так же, после этого нужно сознать конфиг файл pytest.ini и в нем указать настройки для работы с импортом и окружением:
> [pytest] <br>
> pythonpath = . api  <br>
> env_files =
> .test.env

Тесты нормально считывают файл настроек, если сам файл находится в корне проекте

Источники:

- https://pypi.org/project/pytest-dotenv/
- https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
- https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.asyncpg
- https://fastapi.tiangolo.com/ru/tutorial/bigger-applications/
- https://fastapi.tiangolo.com/ru/tutorial/metadata/
- https://github.com/florimondmanca/asgi-lifespan#usage Для запуска асинхронных тестов