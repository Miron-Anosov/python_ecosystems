import threading
from threading import Semaphore, Thread
import time

sem: Semaphore = Semaphore()


def fun1():
    while True:
        sem.acquire()
        print(1)
        sem.release()
        time.sleep(0.25)


def fun2():
    while True:
        sem.acquire()
        print(2)
        sem.release()
        time.sleep(0.25)


t1: Thread = Thread(target=fun1, daemon=True)
t2: Thread = Thread(target=fun2, daemon=True)
try:
    t1.start()
    t2.start()
    while t1.is_alive() or t2.is_alive():  # TODO вместо цикла лучше джойнить оба потока (t1.join(), ..) ведь это блокирующий метод
        time.sleep(0.25)
except KeyboardInterrupt:
    print('\nReceived keyboard interrupt, quitting threads.')
    exit(1)
