"""
Каждый лог содержит в себе метку времени, а значит, правильно организовав логирование,
можно отследить, сколько времени выполняется функция.

Программа, которую вы видите, по умолчанию пишет логи в stdout. Внутри неё есть функция measure_me,
в начале и в конце которой пишется "Enter measure_me" и "Leave measure_me".
Сконфигурируйте логгер, запустите программу, соберите логи и посчитайте среднее время выполнения функции measure_me.
"""
import json
import logging
import random
from datetime import datetime, timedelta
from typing import List

logger = logging.getLogger(__name__)


def get_data_line(sz: int) -> List[int]:
    try:
        logger.debug("Enter get_data_line")
        return [random.randint(-(2 ** 31), 2 ** 31 - 1) for _ in range(sz)]
    finally:
        logger.debug("Leave get_data_line")


def measure_me(nums: List[int]) -> List[List[int]]:
    logger.debug("Enter measure_me")
    results = []
    nums.sort()

    for i in range(len(nums) - 2):
        logger.debug(f"Iteration {i}")
        left = i + 1
        right = len(nums) - 1
        target = 0 - nums[i]
        if i == 0 or nums[i] != nums[i - 1]:
            while left < right:
                s = nums[left] + nums[right]
                if s == target:
                    logger.debug(f"Found {target}")
                    results.append([nums[i], nums[left], nums[right]])
                    logger.debug(
                        f"Appended {[nums[i], nums[left], nums[right]]} to result"
                    )
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    left += 1
                    right -= 1
                elif s < target:
                    logger.debug(f"Increment left (left, right) = {left, right}")
                    left += 1
                else:
                    logger.debug(f"Decrement right (left, right) = {left, right}")

                    right -= 1

    logger.debug("Leave measure_me")

    return results


if __name__ == "__main__":
    logging.basicConfig(
        filename=f'{__name__}.log',
        filemode='w',
        encoding='utf-8',
        level="DEBUG",
        format='{"time" : "%(asctime)s,%(msecs)d", "message" : "%(message)s"}',
        datefmt='%H:%M:%S',

    )

    for it in range(15):
        data_line = get_data_line(10 ** 3)
        measure_me(data_line)

    list_worked_func: list = []
    log_time_for_one_cycle: list = []
    with open(f'{__name__}.log', 'r', ) as log_files:
        for time_logs in log_files:
            log: dict = json.loads(time_logs)

            if log.get("message") == "Enter measure_me":
                time_start: str = log.get("time")
                microsecond_start: int = datetime.strptime(time_start, "%H:%M:%S,%f").microsecond
                log_time_for_one_cycle.append(microsecond_start)

            if log.get("message") == "Leave measure_me":
                time_finish: str = log.get("time")
                microsecond_finish: int = datetime.strptime(time_finish, "%H:%M:%S,%f").microsecond
                log_time_for_one_cycle.append(microsecond_finish)

            if len(log_time_for_one_cycle) == 2:
                time_func: int = abs(log_time_for_one_cycle.pop() - log_time_for_one_cycle.pop())
                list_worked_func.append(time_func)

    if list_worked_func:
        time_func_around: float = sum(list_worked_func) / len(list_worked_func)
        second_run: timedelta = timedelta(microseconds=time_func_around)
        print(f'Среднее затраченное время работы функции measure_me():  {second_run}')
