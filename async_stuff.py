import asyncio
import time
from typing import Awaitable, Any


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)


async def run_program(program: int, wait=5) -> None:
    print(f"Executing program {program} for {wait} seconds... ")
    await asyncio.sleep(wait)
    print(f"=====END OF PROGRAM====== {program}")


async def main() -> None:
    print(f"started at {time.strftime('%X')}")
    await run_parallel(
        run_program(1, 4),
        run_program(2, 4),
        run_sequence(
            run_program(3, 4),
            run_program(4, 4)
        ),
        run_program(5, 4),
    )
    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())
