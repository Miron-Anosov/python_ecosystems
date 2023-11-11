"""
Ваш коллега, применив JsonAdapter из предыдущей задачи, сохранил логи работы его сайта за сутки
в файле skillbox_json_messages.log. Помогите ему собрать следующие данные:

1. Сколько было сообщений каждого уровня за сутки.
2. В какой час было больше всего логов.
3. Сколько логов уровня CRITICAL было в период с 05:00:00 по 05:20:00.
4. Сколько сообщений содержит слово dog.
5. Какое слово чаще всего встречалось в сообщениях уровня WARNING.
"""
import json
import os.path
import subprocess
import shlex
from typing import Dict, List
from collections import defaultdict


def read_log_file() -> List[dict]:
    """
    Функция извлекает данные из лог-файла в формате json.
    Returns:
         Список состоит из словарей формата json, которые в свою очередь являются логами.
         List[dict]
    """
    json_list: List[dict] = []
    skillbox_json_messages_file: str = os.path.abspath(os.path.join('skillbox_json_messages.log'))
    try:

        with open(skillbox_json_messages_file, 'r', ) as log_file:
            for skillbox_log_messages in log_file:
                json_file: dict = json.loads(skillbox_log_messages)
                json_list.append(json_file)

    except FileNotFoundError:
        return []
    return json_list


json_objects: List[dict] = read_log_file()
file = os.path.abspath(os.path.join('skillbox_json_messages.log'))


def task1() -> Dict[str, int]:
    """
    1. Сколько было сообщений каждого уровня за сутки.
    @return: словарь вида {уровень: количество}
    """
    call_logs: Dict[str, int] = defaultdict(int)
    for log in json_objects:
        call_logs[log.get('level')] += 1
    return dict(call_logs)


def task2() -> int:
    """
    2. В какой час было больше всего логов.
    @return: час
    """
    try:
        call_logs = defaultdict(int)
        for log in json_objects:
            call_logs[log.get('time')[:2]] += 1
        max_call_in_hour: int = sorted(call_logs.items(), key=lambda x: x[1]).pop()[0]
        return max_call_in_hour
    except IndexError:
        return 0


def task3() -> int:
    """
    3. Сколько логов уровня CRITICAL было в период с 05:00:00 по 05:20:00.
    @return: количество логов
    """

    cmd_str = f'grep -c \\"time\\":\\ \\"05:[0-1][0-9]:[0-5][0-9]\\",\\ \\""level\\": \\"CRITICAL\\"" {shlex.quote(file)}'
    # TODO регэкспами можно чуть проще сделать:
    #  PATTERN: str = r'"time": "05:[01].:..", "level": "CRITICAL"'
    cmd_list: List[str] = shlex.split(cmd_str)
    with subprocess.Popen(cmd_list, stdout=subprocess.PIPE, text=True, encoding='utf-8') as result:
        count_call = int(result.stdout.read())
    return count_call


def task4() -> int:
    """
    4. Сколько сообщений содержат слово dog.
    @return: количество сообщений
    """
    try:
        cmd_str: str = f"""grep -ciw "dog" {shlex.quote(file)}"""
        cmd_list: List[str] = shlex.split(cmd_str)
        with subprocess.Popen(cmd_list, stdout=subprocess.PIPE, text=True, encoding='utf-8') as result:
            count_dog: int = int(result.stdout.read())
        return count_dog
    except IndexError:
        return 0


def task5() -> str:
    """
    5. Какое слово чаще всего встречалось в сообщениях уровня WARNING.
    @return: слово
    """
    try:
        include_in_warn = defaultdict(int)
        for log in json_objects:
            if log.get("level") == "WARNING":
                for message in log.get('message').split():
                    include_in_warn[message.lower()] += 1
        word: str = sorted(include_in_warn.items(), key=lambda x: x[1]).pop()[0]
        return word
    except IndexError:
        return 'not found word'


if __name__ == '__main__':
    tasks = (task1, task2, task3, task4, task5)
    for i, task_fun in enumerate(tasks, 1):
        task_answer = task_fun()
        print(f'{i}. {task_answer}')
