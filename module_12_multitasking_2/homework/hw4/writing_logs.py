import logging
import sys

import requests
from threading import Thread
from time import time, sleep
from queue import Queue

logger = logging.getLogger(__name__)
fh = logging.FileHandler(filename='hw4.log', mode='w')
fh.setLevel(level=logging.WARNING)
sh = logging.StreamHandler(stream=sys.stdout)
sh.setLevel(level=logging.INFO)
logger.propagate = False
logger.addHandler(fh)
logger.addHandler(sh)

line = Queue()


class RequestLogs(Thread):

    def __init__(self, queue_response: Queue):
        super().__init__()
        self.daemon: bool = True
        self.__queue: Queue = queue_response
        self.base_url = 'http://127.0.0.1:8080//timestamp/'

    def run(self):
        logger.info(f'Started: {self.name}')
        cycle: int = 20

        while cycle:
            log: str = self.__get_date_from_server()
            self.__queue.put(log)
            cycle -= 1
            sleep(1)

        logger.info(f'Finished: {self.name}')

    def __get_date_from_server(self):
        timestamp_url: str = "".join(self.base_url + str(time()))
        response: requests.Response = requests.get(url=timestamp_url, timeout=0.2, )
        for_logs: str = response.text
        return for_logs


class LogThread(Thread):
    def __init__(self, queue_response: Queue):
        super().__init__()
        self.__queue: Queue = queue_response
        self.__count_response: int = 0
        self.stop: bool = False

    @property
    def stop_thread(self):
        return self.stop

    @stop_thread.setter
    def stop_thread(self, bool_value):
        if isinstance(bool_value, bool):
            self.stop = bool_value

    def run(self):
        while not self.stop:
            while not self.__queue.empty():
                logger.warning(self.__queue.get())
                self.__count_response += 1
                self.__queue.task_done()
            sleep(0.01)

        logger.info(f'Finish {self.name}')
        logger.info(f'Completed tasks: {self.__count_response}')


def run():
    logger.info("Program starts")
    start: float = time()
    request_threads: list[RequestLogs] = []
    writing_logs = LogThread(line)
    writing_logs.start()

    for _ in range(10):
        request_thread: RequestLogs = RequestLogs(line)
        request_thread.start()
        request_threads.append(request_thread)
        sleep(1)

    while any(thr.is_alive() for thr in request_threads):
        sleep(0.01)
    else:
        for thr in request_threads:
            thr.join()
        writing_logs.join(timeout=0.1)
        writing_logs.stop = True

    finish: float = time() - start
    logger.info(f'Runtime: {finish:.2f} sec.')
    logger.info("Program is closed")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run()
