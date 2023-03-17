import asyncio


class BlockChain:
    async def check(self):
        for x in range(20):
            print(x)
            await asyncio.sleep(1)
