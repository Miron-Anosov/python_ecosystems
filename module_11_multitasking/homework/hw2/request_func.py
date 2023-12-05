from typing import Tuple, Optional

import requests
import logging

logger: logging = logging.getLogger(__name__)


def star_wars_request(num_person: int) -> Tuple[str, str, str] | Optional[bool]:
    url: str = f"https://swapi.dev/api/people/{num_person}"

    require: requests.Response = requests.get(url=url)
    logger.info(f'{url} status_code: {require.status_code}')
    try:
        if require.status_code == 200:
            person: dict = require.json()
            return person.get('name'), person.get('birth_year'), person.get('gender')
        else:
            raise requests.exceptions.RequestException(f'The request fails: {url}')
    except requests.exceptions.RequestException as er:
        logger.error(er)
        return False


if __name__ == '__main__':
    print(star_wars_request(1))
