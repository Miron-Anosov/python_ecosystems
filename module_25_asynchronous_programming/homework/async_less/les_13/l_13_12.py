import asyncio
from asyncio import StreamWriter, StreamReader
from asyncio.subprocess import Process


async def consume_and_send(text_list, stdout: StreamReader, stdin: StreamWriter):
    for text in text_list:
        line = await stdout.read(2048)
        print(line)
        stdin.write(text.encode())
        await stdin.drain()


async def main():
    program = ['python3', 'l_13_11.py']
    process: Process = await asyncio.create_subprocess_exec(*program,
                                                            stdout=asyncio.subprocess.PIPE,
                                                            stdin=asyncio.subprocess.PIPE)

    text_input = ['one\n', 'two\n', 'three\n', 'four\n', 'quit\n']

    await asyncio.gather(consume_and_send(text_input, process.stdout, process.stdin), process.wait())


asyncio.run(main())

"""
Здесь сопрограмма `consume_and_send` читает стандартный вывод, пока не получит ожидаемое сообщение, 
предлагающее пользователю ввести данные. Получив сообщение, она копирует его на стандартный вывод приложения, 
а очередную строку из списка `text_list` на стандартный ввод. Эти действия повторяются, пока все данные не 
будут переданы подпроцессу. 
При выполнении программы мы увидим, что весь вывод был передан подпроцессу и корректно скопирован на консоль.
"""