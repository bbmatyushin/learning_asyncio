"""Построение API которое может работать с корутинами и обычными функциями"""

import asyncio
from asyncio import AbstractEventLoop
from dataclasses import dataclass, field, InitVar


@dataclass
class TaskRunner:
    loop: AbstractEventLoop = field(init=False, default=asyncio.new_event_loop())
    tasks: list = field(init=False, default_factory=list)

    def add_task(self, func):
        self.tasks.append(func)

    async def _run_all(self):
        awaitable_tasks = []
        for task in self.tasks:
            if asyncio.iscoroutine(task):
                awaitable_tasks.append(asyncio.create_task(task))
            elif asyncio.iscoroutinefunction(task):
                awaitable_tasks.append(asyncio.create_task(task()))
            else:
                self.loop.call_soon(task)

        await asyncio.gather(*awaitable_tasks)

    def run(self):
        # Запуск цисла событий и выполнения корутины, пока она не завершится
        # run_until_complete - работает только с одной корутиной
        self.loop.run_until_complete(self._run_all())


if __name__ == '__main__':
    def regular_func():
        print('Сообщение из регулярной функции!')

    async def coroutine_func():
        print('Сообщение из корутиный! Засыпаю на 2 сек...')
        await asyncio.sleep(2)
        print('Проснулась!')

    runner = TaskRunner()
    runner.add_task(coroutine_func)
    runner.add_task(coroutine_func())
    runner.add_task(regular_func)

    runner.run()

    # print(t)
