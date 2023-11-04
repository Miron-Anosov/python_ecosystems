"""
Иногда возникает необходимость перенаправить вывод в нужное нам место внутри программы по ходу её выполнения.
Реализуйте контекстный менеджер, который принимает два IO-объекта (например, открытые файлы)
и перенаправляет туда стандартные потоки stdout и stderr.

Аргументы контекстного менеджера должны быть непозиционными,
чтобы можно было ещё перенаправить только stdout или только stderr.
"""
import sys
import traceback
from types import TracebackType
from typing import Type, Literal, IO


class Redirect:
    def __init__(self, stdout: IO = None, stderr: IO = None) -> None:
        self.default_stdout = sys.stdout
        self.default_stderr = sys.stderr
        self.stdout = stdout
        self.stderr = stderr

    def __enter__(self):
        if self.stdout:
            sys.stdout = self.stdout
        if self.stderr:
            sys.stderr = self.stderr
        return self

    def __exit__(self, exc_type: Type[BaseException] | None, exc_val: BaseException | None,
                 exc_tb: TracebackType | None) -> Literal[True] | None:
        try:
            if self.stderr and exc_type:
                self.stderr.write(traceback.format_exc())
                return True
            elif exc_type:
                raise exc_val
            else:
                return True
        finally:
            if self.stdout:
                sys.stdout = self.default_stdout
            if self.stderr:
                sys.stderr = self.default_stderr


if __name__ == '__main__':
    print('First code is outside the manager')
    with open('stdout.txt', 'w', encoding='utf-8') as file_out, open('stderr.txt', 'w', encoding='utf-8') as file_err:
        print('First code is inside the manager')
        try:
            raise Exception('First raise occurred inside the manager')
        except Exception as err:
            print(f"Except text: {err}\n{'-' * 50}")
        with Redirect(stdout=file_out, stderr=file_err):
            print('Second code is inside manager')
            raise Exception('Second raise occurred inside the manager')
        print(f"\n{'-' * 50}\nThird code is inside the manager")

    print('Third code is outside the manager')
