"""Создания подпроцессов для вызова команд из другой среды/программы"""

import asyncio
from asyncio.subprocess import Process


async def main1():
    process: Process = await asyncio.create_subprocess_exec('cmd', 'dir')
    print(f"pid: {process.pid}")
    status_code = await process.wait()  # wait() блокирует выполнение пока процесс не завершится (может и не завершиться)
    print(f"{status_code=}")


async def main2():
    program = ['D:\Coding\PythonLearn\Asyncio_Learning\.venv\Scripts\python.exe', '-c',
               '[print("Hello!") for _ in range(1000)]']
    process: Process = await asyncio.create_subprocess_exec(*program)
    await process.wait()


if __name__ == '__main__':
    asyncio.run(main2())
