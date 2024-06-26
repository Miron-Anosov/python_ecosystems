import asyncio
import random
import string
import time
from asyncio.subprocess import Process


async def encrypt(text: str) -> bytes:
    program = ['gpg', '-c', '--batch', '--passphrase', '3ncryptm3', '--cipher-algo', 'TWOFISH']

    process: Process = await asyncio.create_subprocess_exec(*program,
                                                            stdout=asyncio.subprocess.PIPE,
                                                            stdin=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate(text.encode())
    return stdout


async def main():
    text_list = [''.join(random.choice(string.ascii_letters) for _ in range(1000)) for _ in range(100)]

    s = time.time()
    tasks = [asyncio.create_task(encrypt(text)) for text in text_list]
    encrypted_text = await asyncio.gather(*tasks)
    e = time.time()

    print(f'Total time: {e - s}')
    print(encrypted_text)


asyncio.run(main())

"""
Здесь определена сопрограмма `encrypt`, которая создает процесс `gpg` и с помощью `communicate` передает ему подлежащий 
шифрованию текст. Для простоты мы лишь возвращаем результат, записанный на стандартный вывод, и не пытаемся обрабатывать 
ошибки; реальное приложение следовало бы сделать более надежным.

Затем в сопрограмме `main` мы создаем список случайных текстов и для каждого из них — задачу `encrypt`. Эти задачи 
конкурентно выполняются с помощью `gather`, после чего печатается время работы и зашифрованные тексты. 
Время конкурентной работы можно сравнить со временем синхронной работы, поместив `await` перед `asyncio.create_task` и 
убрав `gather`; выигрыш существенный.
"""