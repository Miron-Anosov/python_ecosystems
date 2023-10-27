"""
Напишите код, который выводит сам себя.
Обратите внимание, что скрипт может быть расположен в любом месте.
"""
import os
import sys

path_dir = os.path.dirname(__file__)
path_full = os.path.join(path_dir, __file__)

result = 0
for n in range(1, 11):
    result += n ** 2

with open(path_full, 'r', encoding='utf-8') as pyfile:
    code = pyfile.read()
    sys.stdout.write(code)

