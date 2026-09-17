import asyncio, random

async def retry_async(fn, attempts=5, base_delay=0.5, max_delay=30):
    last = None
    for i in range(attempts):
        try:
            return await fn()
        except Exception as exc:
            last = exc
            if i == attempts - 1:
                raise
            delay = min(max_delay, base_delay * (2 ** i))
            await asyncio.sleep(delay * (0.5 + random.random()))
    raise last
