from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from requests import Session

URL = 'https://cataas.com/cat'
OUT_PATH = Path(__file__).parent / 'cats'
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()


def get_cat(session: Session, url: str) -> bytes:
    with session.get(url, timeout=15) as conn:
        return conn.content


def create_cat_png(data: tuple[int, bytes]) -> None:
    name, img = data
    file = OUT_PATH / f'{name}.png'
    with open(file, 'wb') as file:
        file.write(img)


def process_cats(cats=10) -> None:
    session = Session()
    with ProcessPoolExecutor(32) as pool:
        tasks: list = [pool.submit(get_cat, session, URL) for _ in range(cats)]
        results: list = [(index, task.result()) for index, task in enumerate(tasks)]
        pool.map(create_cat_png, results)


if __name__ == '__main__':
    process_cats()
