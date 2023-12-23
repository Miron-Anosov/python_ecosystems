import logging

from sw_request_worker import major_thread as main_thread, ather_threads

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    ather_threads(name_db='sw_threads')
    main_thread(name_db='sw_thread')
