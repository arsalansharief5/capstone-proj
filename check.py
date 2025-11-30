import asyncio
import aiohttp
import time

URL = "https://capstone-django-777268942678.asia-south1.run.app/api/get-upload-url"

async def hit(session):
    async with session.get(URL) as resp:
        await resp.text()

async def main():
    total = 100  # number of concurrent users
    start = time.time()

    async with aiohttp.ClientSession() as session:
        tasks = [hit(session) for _ in range(total)]
        await asyncio.gather(*tasks)

    print("Total time:", time.time() - start)

asyncio.run(main())
