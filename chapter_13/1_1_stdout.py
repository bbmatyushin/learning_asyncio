import asyncio
from asyncio import StreamReader
from asyncio.subprocess import Process


async def write_output(prefix: str, stdout: StreamReader):
    while line := await stdout.readline():
        print(f"[{prefix}]:  {line.rstrip().decode()}")


async def main():
    # program = ['cmd', '/d', 'dir']
    program = ['D:\Coding\PythonLearn\Asyncio_Learning\.venv\Scripts\python.exe', '-c',
               '[print("Hello!") for _ in range(1000)]']
    # asyncio.subprocess.PIPE - для чтения вывода внешней команды, для его обработки в коде Python
    process: Process = await asyncio.create_subprocess_exec(*program,
                                                            stdout=asyncio.subprocess.PIPE)

    stdout_task = asyncio.create_task(write_output(str(program[0]), process.stdout))
    # await stdout_task
    # await write_output(' '.join(program), process.stdout)
    await asyncio.gather(process.wait(), stdout_task)


if __name__ == '__main__':
    asyncio.run(main())
