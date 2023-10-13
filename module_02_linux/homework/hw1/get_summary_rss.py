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
    size_count = 0
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
            rss_iter = int(rss)
            while rss_iter >= 1024:
                rss_iter = rss_iter // 1024
                size_count += 1
            rss = rss // (1024 * size_count)
            match size_count:
                case 0:
                    return f'{rss:,} байт'
                case 1:
                    return f'{rss:,} килобайт'
                case 2:
                    return f'{rss:,} мегабайт'
                case 3:
                    return f'{rss:,} гигабайт'
    except (FileNotFoundError, IOError, ValueError) as er:
        print(er)


if __name__ == '__main__':
    path: str = os.path.abspath(os.path.join('output_file.txt'))
    summary_rss: str = get_summary_rss(path)
    print(summary_rss)
