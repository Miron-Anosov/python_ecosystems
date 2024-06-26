import asyncio
from asyncio.subprocess import Process


async def main():
    program = ['python3', 'l_13_9.py']
    process: Process = await asyncio.create_subprocess_exec(*program,
                                                            stdout=asyncio.subprocess.PIPE,
                                                            stdin=asyncio.subprocess.PIPE)

    stdout, stderr = await process.communicate(b'Zoot')
    print(stdout)
    print(stderr)


asyncio.run(main())

"""
При выполнении этой программы мы увидим на консоли строку `b'Введите имя пользователя: Вы ввели имя Zoot\n'`, 
потому что приложение завершается сразу после ввода имени. Если степень интерактивности приложения выше, 
то это не годится. Например, рассмотрим приложение, которое в цикле запрашивает данные и копирует их на 
стандартный вывод, пока пользователь не завершит программу.
"""