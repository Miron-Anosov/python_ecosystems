import logging
import time

from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from module_18_documentation.homework.hw1.client import APIClient, get_authors_by_id_without_session


def test_get_authors_by_id_with_session_and_without_threading(repeat: int, port: int) -> float:
    api_client = APIClient()
    start = time.time()
    while repeat != 0:
        _ = api_client.get_authors_by_id(port=port)
        repeat -= 1
    total_time = time.time() - start
    return total_time


def test_get_authors_by_id_with_threading_and_session(repeat: int, port: int) -> float:
    api_client = APIClient()
    start = time.time()
    with ThreadPool(processes=cpu_count() * 3) as tp:
        request_thread = [tp.apply_async(func=api_client.get_authors_by_id, args=(port,)) for _ in range(repeat)]
        for i_request in request_thread:
            i_request.ready()
    total_time = time.time() - start
    return total_time


def test_get_authors_by_id_without_session_and_threading(repeat: int, port: int) -> float:
    start = time.time()
    while repeat != 0:
        _ = get_authors_by_id_without_session(port)
        repeat -= 1
    total_time = time.time() - start
    return total_time


def test_get_authors_by_id_with_threading_without_session(repeat: int, port: int) -> float:
    start = time.time()
    with ThreadPool(processes=cpu_count() * 3) as tp:
        request_thread = [tp.apply_async(func=get_authors_by_id_without_session, args=(port,)) for _ in range(repeat)]
        for i_request in request_thread:
            i_request.ready()
    total_time = time.time() - start
    return total_time


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    port_http_1_0 = 8080
    port_http_1_1 = 5000
    repeats = (10, 100, 1000)
    benchmark_of_request = {}

    for i_repeat in repeats:
        benchmark = test_get_authors_by_id_without_session_and_threading(repeat=i_repeat, port=port_http_1_0)
        benchmark_two = test_get_authors_by_id_without_session_and_threading(repeat=i_repeat, port=port_http_1_1)

        benchmark_three = test_get_authors_by_id_with_threading_without_session(repeat=i_repeat, port=port_http_1_0)
        benchmark_four = test_get_authors_by_id_with_threading_without_session(repeat=i_repeat, port=port_http_1_1)

        benchmark_five = test_get_authors_by_id_with_session_and_without_threading(repeat=i_repeat, port=port_http_1_0)
        benchmark_six = test_get_authors_by_id_with_threading_and_session(repeat=i_repeat, port=port_http_1_0)

        benchmark_seven = test_get_authors_by_id_with_session_and_without_threading(repeat=i_repeat, port=port_http_1_1)
        benchmark_eight = test_get_authors_by_id_with_threading_and_session(repeat=i_repeat, port=port_http_1_1)

        benchmark_of_request[f'{i_repeat} запросов -O  -S  -T : '] = benchmark
        benchmark_of_request[f'{i_repeat} запросов -O  -S  +T : '] = benchmark_three
        benchmark_of_request[f'{i_repeat} запросов -O  +S  -T : '] = benchmark_five
        benchmark_of_request[f'{i_repeat} запросов -O  +S  +T : '] = benchmark_six

        benchmark_of_request[f'{i_repeat} запросов +O  -S  -T : '] = benchmark_two
        benchmark_of_request[f'{i_repeat} запросов +O  -S  +T : '] = benchmark_four
        benchmark_of_request[f'{i_repeat} запросов +O  +S  -T : '] = benchmark_seven
        benchmark_of_request[f'{i_repeat} запросов +O  +S  +T : '] = benchmark_eight

    for message, result in benchmark_of_request.items():
        print(f'{message} {result:.3f}')
