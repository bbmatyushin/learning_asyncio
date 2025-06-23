"""Сопрограмма для повторного вызова корутин"""

import asyncio
import logging
from typing import Callable, Awaitable


class TooManyRetries(Exception):
    pass


async def retry(coro: Callable[[], Awaitable],
                max_retry: int,
                timeout: float,
                retry_interval: float):
    for retry_num in range(1, 1 + max_retry):
        try:
            print(f"Пробуем {retry_num} {coro.__name__}")
            return await asyncio.wait_for(coro(), timeout=timeout)  # ждать ответа, пока не истечет timeout
        except Exception as e:
            # Если возникло исключение, то сообщаем об этом и ждем заданное время
            logging.exception(f"Во время ожидания произошло исключение (попытка {retry_num}), пробуем ещё раз...",
                              exc_info=e)
            await asyncio.sleep(retry_interval)
    raise TooManyRetries()
