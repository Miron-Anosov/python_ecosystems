import random
import requests
import time
import platform
import signal
from concurrent.futures import ThreadPoolExecutor
from prometheus_client import Counter, start_http_server

request_counter = Counter('http_requests_test_client', 'HTTP request', ["status_code", "instance"])

URLS = [
    'http://api_app:5000',
    'http://api_app:5000/error_not_found',
    'http://api_app:5000/test_error',
    'http://api_app:5000/something',
    'http://api_app:5000/main',
    'http://api_app:5000/long-running',
]

running = True


def get_url():
    """Функция для выполнения HTTP-запроса и обновления счетчика"""
    url = random.choice(URLS)
    try:
        response = requests.get(url)
        status_code = response.status_code
    except requests.RequestException as e:
        print(f'Error fetching {url}: {e}')
        status_code = 'error'

    print(f'{status_code=}, {url=}')
    request_counter.labels(status_code=f'{status_code}', instance=platform.node()).inc()

    time.sleep(random.random())


def do_thread_pool(num_threads=5):
    """Функция для создания пула потоков и выполнения задач"""
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(get_url) for _ in range(num_threads)]
        for future in futures:
            try:
                future.result()
            except Exception as e:
                print(f'Error in thread pool: {e}')


def signal_handler(sig, frame):
    global running
    running = False


if __name__ == '__main__':
    start_http_server(8000)

    signal.signal(signal.SIGINT, signal_handler)

    while running:
        do_thread_pool()
        time.sleep(random.random())
