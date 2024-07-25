# Этот код реализует асинхронный процесс генерации данных с использованием библиотеки aiohttp

import asyncio
from asyncio import Task
from typing import TypeAlias

from aiohttp import ClientSession, ClientTimeout, ClientResponseError, ServerTimeoutError
from aiohttp import web_response

DATA_TYPE: TypeAlias = tuple[list[dict], list[dict]]


class GenerateData:
    FAIL: int = 0  # fail response

    def __init__(self) -> None:
        self.timeout: float = 5.0

    @staticmethod
    async def request_to_api(session, url: str) -> dict:
        """
        Статический асинхронный метод, который отправляет GET-запрос по указанному URL и возвращает JSON-ответ.
        Args:
            url: str :
            session: aiohttp ClientSession
        Returns:
            response.json() : dict: данные с api: "https://random-data-api.com/api/"
        Notes:
            Если код состояния равен 200 (OK).
            Если код состояния равен 429 (Слишком много запросов),он генерирует asyncio.TimeoutError
        """
        async with session.get(url=url) as response:
            if response.status == web_response.HTTPStatus.OK:
                return await response.json()
            if response.status == web_response.HTTPStatus.TOO_MANY_REQUESTS:
                raise ServerTimeoutError(response.status)
            if response.status == web_response.HTTPStatus.INTERNAL_SERVER_ERROR:
                raise ClientResponseError(request_info=response.request_info,
                                          history=response.history,
                                          status=response.status,
                                          message=f"INTERNAL_SERVER_ERROR\n")

    async def get_request(self, url: str) -> dict:
        """
            Метод отвечает за открытие сессии и передачи ее в __request() для дальнейшей обработки.
        Args:
            url: str: ресурс api.
        Returns:
            data: dict: Рандомные сгенерированные данные.
        """
        data: dict = {}
        max_retries = 5
        fail = 1
        async with ClientSession(timeout=ClientTimeout(total=self.timeout, connect=self.timeout / 2)) as session:
            while len(data) == self.FAIL:
                try:
                    return await self.request_to_api(session=session, url=url)
                except ServerTimeoutError as err:
                    await asyncio.sleep(0.5)
                    if max_retries == self.FAIL:
                        raise err
                    max_retries -= fail
            else:
                return data


async def generate_data(request_client: GenerateData) -> DATA_TYPE:
    """
    Функция координирует асинхронные задачи.
    """
    str_url_address = " https://random-data-api.com/api/address/random_address?size=10"
    str_url_coffee = "https://random-data-api.com/api/coffee/random_coffee?size=10"

    addresses: Task = asyncio.create_task(request_client.get_request(str_url_address))
    coffees: Task = asyncio.create_task(request_client.get_request(str_url_coffee))

    return await asyncio.gather(addresses, coffees)


def generate_run() -> DATA_TYPE:
    """Предоставляет способ вызова процесса генерации данных."""
    request_client = GenerateData()
    return asyncio.run(generate_data(request_client=request_client))
