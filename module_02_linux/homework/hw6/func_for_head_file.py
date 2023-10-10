import os.path
from typing import Optional


def func_for_head_file(path: str) -> str:
    """
    Функция принимает путь к файлу и возвращает ссылку и текст файла.

    Args:
        path: str: Путь к файлу

    Returns:
        str: Будет возвращен результат выполнения функции или же вернутся
        ответ о том что возникли проблемы со чтением файла.

    Raises:
        ValueError: Возникает при попытке получения параметра ссылки size.
    """
    try:
        size: Optional[int] = int(''.join(size_ for size_ in path.split('/')[0] if size_.isdigit()))
    except ValueError:
        size: Optional[int] = None

    if size:  # Удаляем из path начало строки, которая была передана в size.
        path: str = path[len(str(size)) + 1:]
        if path.startswith('/'):  # Проверяем, на случай если пользователь ввел число с точкой.
            path = path[1:]
    path: str = os.path.abspath(path)
    return make_text_output(path=path, size=size)


def make_text_output(path: str, size: Optional[int] = None) -> str:
    """
    Функция формирует информацию для вывода.

    Args:
        path: str: Путь к файлу для чтения.
        size: Optional[int] = None : Применяя данный параметр будет возвращена часть текста.

    Returns:
        str: Будет возвращен результат выполнения функции или же вернутся
        ответ о том что возникли проблемы со чтением файла.

    Raises:
        FileNotFoundError: будет вызвано в случае отсутствия файла в дирректории.
    """
    try:
        if os.path.exists(path):
            with open(path, 'r') as file:
                if size is not None:   # Если параметр передан, то будет возвращена часть текста.

                    output_str: str = file.read(size)
                    return f"<a title='file://{path}', href='file://{path}'><strong>{path}</strong></a>" \
                           f" {len(output_str)}<br>{output_str}"
                else:

                    output_str: str = file.read()
                    return f"<a title='link_of_file', href='file:///{path}'><strong>{path}</strong></a>" \
                           f" {len(output_str)}<br>{output_str}"
        else:
            raise FileNotFoundError('Файл не обнаружен по указанному пути.')
    except FileNotFoundError as er:
        return f'Возникли проблемы с указанным файлом: {path}<br> <a><strong>{er}</strong></a>'
