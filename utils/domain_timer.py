import asyncio, time
from collections import defaultdict

last_call: dict[str, float] = defaultdict(lambda: 0.0)
domain_locks: dict[str, asyncio.Lock] = defaultdict(asyncio.Lock)

async def rate_limit(domain: str) -> None:
    delay = 0.5

    async with domain_locks[domain]:
        now = time.monotonic()
        delta = now - last_call[domain]

        if delta < delay:
            await asyncio.sleep(delay - delta)

        last_call[domain] = time.monotonic()