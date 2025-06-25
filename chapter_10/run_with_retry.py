import asyncio
from coroutine_retry import retry, TooManyRetries


async def main():
    async def always_fail():
        raise Exception('Программа, которая всегда падает')

    async def always_timeout():
        await asyncio.sleep(1)

    try:
        await retry(always_fail,
                    max_retry=3,
                    timeout=.1,
                    retry_interval=.1)
    except TooManyRetries:
        print('Слишком много попыток')

    try:
        await retry(always_timeout,
                    max_retry=3,
                    timeout=.1,
                    retry_interval=.1)
    except TooManyRetries:
        print('Слишком много попыток')


if __name__ == '__main__':
    asyncio.run(main())
