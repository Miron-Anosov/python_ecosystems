"""
Консольная утилита lsof (List Open Files) выводит информацию о том, какие файлы используют какие-либо процессы.
Эта команда может рассказать много интересного, так как в Unix-подобных системах всё является файлом.

Но нам пока нужна лишь одна из её возможностей.
Запуск lsof -i :port выдаст список процессов, занимающих введённый порт.
Например, lsof -i :5000.

Как мы с вами выяснили, наш сервер отказывается запускаться, если кто-то занял его порт. Напишите функцию,
которая на вход принимает порт и запускает по нему сервер. Если порт будет занят,
она должна найти процесс по этому порту, завершить его и попытаться запустить сервер ещё раз.
"""
import subprocess
from typing import List

from flask import Flask

app = Flask(__name__)


def get_pids(port: int) -> List[int]:
    """
    Возвращает список PID процессов, занимающих переданный порт
    @param port: порт
    @return: список PID процессов, занимающих порт
    """
    if not isinstance(port, int):
        raise ValueError

    pids: List[int] = []
    command: str = f'lsof -i :{port}'
    with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True) as procs:
        procs.wait()
        if procs.returncode != 1:
            ports_line: List[str] = procs.stdout.read().strip().split('\n')  # разбиваем на строки.
            top_line_output = ports_line[0].split()  # извлекаем шапку таблицы.
            index_pid: int = top_line_output.index('PID')  # извлекаем индекс.
            for i_process in range(1, len(ports_line)):  # обход строк со второй строки.
                try:  # извлекаем pid и преобразуем строковый тип данных в целочисленный
                    pid: int = int(ports_line[i_process].split()[index_pid])
                    pids.append(pid)
                except TypeError:
                    raise TypeError(f'{pid} is not integer')

    return pids


def free_port(port: int) -> None:
    """
    Завершает процессы, занимающие переданный порт
    @param port: порт
    """
    command = 'kill'
    pids: List[int] = get_pids(port)
    if pids:
        list_process = []
        for i_procs in pids:
            process = subprocess.Popen([command, str(i_procs)])
            list_process.append(process)
        for proc in list_process:
            try:
                proc.wait()
            except subprocess.TimeoutExpired:
                subprocess.run(f'kill -9 {proc}', capture_output=True)


def run(port: int) -> None:
    """
    Запускает flask-приложение по переданному порту.
    Если порт занят каким-либо процессом, завершает его.
    @param port: порт
    """
    free_port(port)
    app.run(port=port)


if __name__ == '__main__':
    run(5000)
