from tortoise import Tortoise, fields, run_async
from tortoise.models import Model


class Event(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    datetime = fields.DatetimeField(auto_now=True, null=True)

    class Meta:
        table = "hehe"

    def __str__(self):
        return self.name


async def run():
    await Tortoise.init(db_url="mysql://root:123456@localhost:55555/test_demo", modules={"models": ["__main__"]})
    # await Tortoise.generate_schemas()

    # event = await Event.create(name="Test")
    # await Event.filter(id=event.id).update(name="Updated name")
    #
    # print(await Event.filter(name="Updated name").first())
    # >>> Updated name

    event = await Event.create(name='cjs')

    event2 = Event()
    event2.name = "hehe"
    await event2.save()
    print(await Event.all().values_list("id",flat=True))
    # >>> [1, 2]
    print(await Event.all().values('id','name'))
    # >>> [{'id': 1, 'name': 'Updated name'}, {'id': 2, 'name': 'Test 2'}]


if __name__ == "__main__":
    run_async(run())
