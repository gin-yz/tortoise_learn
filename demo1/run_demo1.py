from tortoise import Tortoise
from demo1.modes import Tournament
import asyncio

async def init():
    user = 'root'
    password = '123456'
    db_name = 'test_demo'
    await Tortoise.init(
        db_url=f'mysql://{user}:{password}@127.0.0.1:55555/{db_name}',
        modules={'models': ['demo1.modes']}
    )

async def tournament_create():
    tournament = Tournament(name='New Tournament')
    await tournament.save()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()

    task1 = loop.create_task(init())
    loop.run_until_complete(task1)

    task2 = loop.create_task(tournament_create())
    loop.run_until_complete(task2)