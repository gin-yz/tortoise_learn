import asyncio
import aioredis


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    print(loop.__dict__)
    loop.run_forever()