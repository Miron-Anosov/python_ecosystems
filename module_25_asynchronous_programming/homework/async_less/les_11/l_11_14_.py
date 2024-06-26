import asyncio
import random
from asyncio import Condition, Event


class DataProcessor:
    def __init__(self):
        self.condition = Condition()
        self.data_queue = []
        self.stop_event = Event()
        self.pause_event = Event()
        self.pause_event.set()  # Изначально не на паузе

    async def collect_data(self):
        while not self.stop_event.is_set():
            await self.pause_event.wait()  # Ждем, если на паузе
            data = await self.simulate_data_collection()
            async with self.condition:
                self.data_queue.append(data)
                print(f"Collected data: {data}")
                self.condition.notify()
            await asyncio.sleep(random.uniform(0.1, 0.5))

    async def process_data(self, processor_id):
        while not self.stop_event.is_set():
            await self.pause_event.wait()  # Ждем, если на паузе
            async with self.condition:
                while not self.data_queue and not self.stop_event.is_set():
                    await self.condition.wait()
                if self.stop_event.is_set():
                    break
                data = self.data_queue.pop(0)
            await self.simulate_data_processing(processor_id, data)

    async def simulate_data_collection(self):
        return random.randint(1, 100)

    async def simulate_data_processing(self, processor_id, data):
        processing_time = random.uniform(0.5, 2)
        await asyncio.sleep(processing_time)
        print(f"Processor {processor_id} processed data: {data} in {processing_time:.2f} seconds")

    def pause(self):
        self.pause_event.clear()
        print("System paused")

    def resume(self):
        self.pause_event.set()
        print("System resumed")

    def stop(self):
        self.stop_event.set()
        self.resume()  # Чтобы все задачи могли завершиться
        print("System stopping")

    async def run(self, num_processors=3):
        tasks = [asyncio.create_task(self.collect_data())]
        tasks.extend([asyncio.create_task(self.process_data(i)) for i in range(num_processors)])

        # Демонстрация управления процессом
        await asyncio.sleep(10)
        self.pause()
        await asyncio.sleep(5)
        self.resume()
        await asyncio.sleep(10)
        self.stop()

        await asyncio.gather(*tasks)


async def main():
    processor = DataProcessor()
    await processor.run()


asyncio.run(main())
