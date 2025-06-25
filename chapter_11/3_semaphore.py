"""Семафор служит для ограничения уровня конкурентности. Т.е. ограничивае количество задач,
кторые могут выполняться конкурентно."""

import asyncio
from asyncio import Semaphore


async def operation(semaphore: Semaphore, task_id: int):
    print(f'Жду возможность захватить Семафор. {task_id=}')
    async with semaphore:
        print(f'Семафо захвачен!. {task_id=}')
        await asyncio.sleep(2)
    print(f'Семафор освобожден!. {task_id=}')


async def main():
    semaphore = Semaphore(2)  # 2 - предел ограничени кнкурентно выполняемых задач
    await asyncio.gather(*[operation(semaphore, task_id=i) for i, _ in enumerate(range(6), start=1)])


if __name__ == '__main__':
    asyncio.run(main())
