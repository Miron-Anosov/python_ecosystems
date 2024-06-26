import asyncio
from asyncio import StreamWriter, StreamReader, Event
from asyncio.subprocess import Process


async def output_consumer(input_ready_event: Event, stdout: StreamReader):
    while (data := await stdout.read(1024)) != b'':
        print(data)
        if data.decode().endswith("Enter text to echo: "):
            input_ready_event.set()


async def input_writer(text_data, input_ready_event: Event, stdin: StreamWriter):
    for text in text_data:
        await input_ready_event.wait()
        stdin.write(text.encode())
        await stdin.drain()
        input_ready_event.clear()


async def main():
    program = ['python3', 'l_13_13.py']
    process: Process = await asyncio.create_subprocess_exec(*program,
                                                            stdout=asyncio.subprocess.PIPE,
                                                            stdin=asyncio.subprocess.PIPE)

    input_ready_event = asyncio.Event()

    text_input = ['one\n', 'two\n', 'three\n', 'four\n', 'quit\n']

    await asyncio.gather(output_consumer(input_ready_event, process.stdout),
                         input_writer(text_input, input_ready_event, process.stdin),
                         process.wait())


asyncio.run(main())

"""
Здесь мы сначала определяем сопрограмму `output_consumer`. Она принимает событие `input_ready_event`, а также объект 
`StreamReader`, ссылающийся на стандартный вывод, и читает стандартный вывод, пока не встретит строку "Введите текст:". 
В этот момент мы знаем, что подпроцесс готов принимать данные из стандартного ввода, поэтому 
устанавливаем событие `input_ready_event`.

Сопрограмма `input_writer` обходит список входных строк и ждет готовности события `input_ready_event`. 
Как только подпроцесс будет готов к приему данных, мы записываем данные на стандартный ввод и очищаем событие, 
так что следующая итерация цикла `for` будет заблокирована в ожидании готовности к вводу. В этой реализации есть 
две сопрограммы, и у каждой своя четко определенная сфера ответственности: одна пишет на стандартный ввод, 
а другая читает стандартный вывод. Код стал понятнее и удобнее для сопровождения.
"""