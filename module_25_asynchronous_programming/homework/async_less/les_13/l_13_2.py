import asyncio
from asyncio.subprocess import Process


async def main():
    process: Process = await asyncio.create_subprocess_exec('sleep', '3')
    print(f'Process pid is: {process.pid}')
    try:
        status_code = await asyncio.wait_for(process.wait(), timeout=1.0)
        print(status_code)
    except asyncio.TimeoutError:
        print('Timed out waiting to finish, terminating...')
        process.terminate()
        status_code = await process.wait()
        print(status_code)


asyncio.run(main())

"""
Здесь мы создаем подпроцесс, который работает 3 секунды, но оборачиваем его в сопрограмму `wait_for` 
с односекундным тайм-аутом. По истечении 1 секунды `wait_for` возбуждает исключение `TimeoutError`, 
и в блоке `except` мы вызываем метод `terminate` для завершения процесса и ждем, когда он завершится. 
После завершения мы печатаем код состояния процесса.
При написании собственного кода следует иметь в виду, что вызов `wait` внутри блока `except` также может 
занимать длительное время; если это беспокоит, оберните его в сопрограмму `wait_for`.
"""
