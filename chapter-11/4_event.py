"""Объект Event предоставляе механизм, позволяющий ждать ничего не делая,
пока что-то не произойдет, какое-нибудь внешнее событие."""

import asyncio
import functools
from asyncio import Event


def trigger_event(event: Event):
    print('Активация события!')
    event.set()  # устанавливает значение события в True и уведомляет всех, кто ожидает события


async def work_on_event(event: Event):
    print('Ожидание события...')
    await event.wait()  # ждать события
    print('Работаю!')
    await asyncio.sleep(2)
    print('Работа завершена!')
    print(f"Event is set - {event.is_set()}")
    event.clear()  # сбрасывает значения в False и любой, кто ожидает события, будет блокирован
    print(f"Event is set - {event.is_set()}")


async def main():
    event = asyncio.Event()
    print(f"Event is set - {event.is_set()}")
    # метод call_later для активации trigger_event через 5 секунд
    asyncio.get_running_loop().call_later(5.0, functools.partial(trigger_event, event))
    await asyncio.gather(work_on_event(event), work_on_event(event))


if __name__ == '__main__':
    asyncio.run(main())
