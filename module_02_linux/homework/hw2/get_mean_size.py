"""
Удобно направлять результат выполнения команды напрямую в программу с помощью конвейера (pipe):

$ ls -l | python3 get_mean_size.py

Напишите функцию get_mean_size, которая на вход принимает результат выполнения команды ls -l,
а возвращает средний размер файла в каталоге.
"""

import sys


def get_mean_size(ls_output: list) -> float:
    count_bite: float = 0.0
    count_file: int = 0
    with open('ls.txt', 'w', encoding='utf-8') as file:
        for line in ls_output:
            file.write(f'{line}')
    try:
        for line in ls_output:
            float_dig: float = float(line.split()[4])
            count_bite += float_dig
            count_file += 1
        count_bite = count_bite / count_file
        return count_bite
    except ZeroDivisionError:
        return 0.0


if __name__ == '__main__':
    data: list = sys.stdin.readlines()[1:]
    mean_size: float = get_mean_size(data)
    print(mean_size)
