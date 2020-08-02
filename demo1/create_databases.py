from tortoise import Tortoise
import asyncio

async def init():
    user = 'root'
    password = '123456'
    db_name = 'test_demo'
    await Tortoise.init(
        #指定mysql信息
        db_url=f'mysql://{user}:{password}@127.0.0.1:55555/{db_name}',
        #指定models
        modules={'models': ['demo1.modes']}
    )
    #按照模型生成表
    await Tortoise.generate_schemas()

asyncio.run(init())