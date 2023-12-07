import random
import logging
import time
from threading import Thread
from queue import PriorityQueue

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Producer(Thread):
    """
    Класс создает задачи и назначает им приоритетностьБ затем передает задачу в очередь.
    Класса является потомком Thread.
    """

    def __init__(self, queue_task: PriorityQueue, name: str) -> None:
        super().__init__(name=name)
        self.queue_task: PriorityQueue = queue_task
        logger.info('Create Producer')

    def run(self):
        """
        Метод создает задачи, присваивает им уровень приоритета и отправляет их в очередь используя для этого
        класс PriorityQueue.
        Returns:
            None
        """
        priority_task: int = 1
        while priority_task:
            priority_task: int = random.randint(0, 10)
            name_task: str = f'Some task. Priority number {priority_task}'
            task_to_queue: tuple[int, str] = (priority_task, name_task)
            self.queue_task.put(task_to_queue)
            logger.info(f'Create new task: {task_to_queue}')


class Consumer(Thread):
    """
    Класс обрабатывает задачи в приоритетном порядке. Класса является потомком Thread.
    """

    def __init__(self, queue_task: PriorityQueue, name: str) -> None:
        super().__init__(name=name)
        self.queue_task: PriorityQueue = queue_task
        logger.info('Create Consumer')

    def run(self) -> None:
        """
        Метод принимает задачи в приоритетной очереди используя для этого класс PriorityQueue
        Returns:
            None
        """

        while not self.queue_task.empty():
            _, task = self.queue_task.get()
            time.sleep(random.randint(1, 3))
            logger.info(f'Get new task: {task}')
            self.queue_task.task_done()


class TaskManager:
    """
    Менеджер запускает потоки и по завершению их работы, объединяет их в главный поток.
    """

    def __init__(self, producer: Producer, consumer: Consumer, task_line: PriorityQueue):
        self.producer: Producer = producer
        self.consumer: Consumer = consumer
        self.task_line: PriorityQueue = task_line
        logger.info('Start TaskManager')

    def queue_run(self) -> None:
        """
         Метод запускает потоки, а после чего вызывается метод queue_stop()
        Returns:
            None
        """
        self.producer.start()
        time.sleep(1)
        self.consumer.start()
        self.queue_stop()

    def queue_stop(self) -> None:
        """
        Метод объединяет потоки.
        Returns:
            None
        """
        self.producer.join()
        self.consumer.join()
        logger.info(f'{self.consumer.name} finished')
        logger.info(f'{self.producer.name} finished')


if __name__ == '__main__':
    queue = PriorityQueue(maxsize=3)
    producer_worker = Producer(queue_task=queue, name='Producer')
    some_consumer = Consumer(queue_task=queue, name='Consumer')
    manager = TaskManager(producer_worker, some_consumer, queue)
    manager.queue_run()
