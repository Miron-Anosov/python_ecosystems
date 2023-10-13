"""
С помощью команды ps можно посмотреть список запущенных процессов.
С флагами aux эта команда выведет информацию обо всех процессах, запущенных в системе.

Запустите эту команду и сохраните выданный результат в файл:

$ ps aux > output_file.txt

Столбец RSS показывает информацию о потребляемой памяти в байтах.

Напишите функцию get_summary_rss, которая на вход принимает путь до файла с результатом выполнения команды ps aux,
а возвращает суммарный объём потребляемой памяти в человекочитаемом формате.
Это означает, что ответ надо перевести в байты, килобайты, мегабайты и так далее.
"""
import os.path
import subprocess


def get_summary_rss(ps_output_file_path: str) -> str:
    """
    Функция создает файл и извлекает из него данные из столбца RSS для форматирования данных и возврата в виде str.

    Arg:
        ps_output_file_path: str: Путь к файлу.
    Returns:
        str: RAM mb
    """
    rss: int = 0
    index_rss: int | None = None
    try:
        with open(ps_output_file_path, 'w', encoding='utf-8') as file_create:
            subprocess.run(['ps', 'aux'], stdout=file_create, text=True)
            with open(ps_output_file_path, 'r', encoding='utf-8') as file_read:
                for line in file_read:
                    bite_date = line.split()
                    if index_rss is None:
                        index_rss = bite_date.index('RSS')
                    if bite_date[index_rss].isdigit():
                        rss += int(bite_date[index_rss])
            rss = int(rss / (1024 * 2))  # TODO почему 2? Надо делить на 1024 пока результат деления не станет равен
                                         #  меньше 1024 и считать итерации, соответственно, размерность будет байт,
                                         #  килобайты, мегабайты, гигабайты в зависимости от количества итераций
        return f'{rss} Mb'
    except (FileNotFoundError, IOError) as er:
        print(er)


if __name__ == '__main__':
    path: str = os.path.abspath(os.path.join('output_file.txt'))
    summary_rss: str = get_summary_rss(path)
    print(summary_rss)
