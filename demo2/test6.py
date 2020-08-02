"""
This example demonstrates how you can use Tortoise if you have to
separate databases

Disclaimer: Although it allows to use two databases, you can't
use relations between two databases

Key notes of this example is using db_route for Tortoise init
and explicitly declaring model apps in class Meta
"""
from tortoise import Tortoise, fields, run_async
from tortoise.exceptions import OperationalError
from tortoise.models import Model


class Tournament(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()

    def __str__(self):
        return self.name

    class Meta:
        app = "tournaments"


class Event(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    tournament_id = fields.IntField()
    # Here we make link to events.Team, not models.Team
    participants: fields.ManyToManyRelation["Team"] = fields.ManyToManyField(
        "events.Team", related_name="events", through="event_team"
    )

    def __str__(self):
        return self.name

    class Meta:
        app = "events"


class Team(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()

    events: fields.ManyToManyRelation[Event]

    def __str__(self):
        return self.name

    class Meta:
        app = "events"


async def run():
    await Tortoise.init(
        {
            "connections": {
                "first": 'mysql://root:123456@localhost:55555/test_demo',
                "second": 'mysql://root:123456@localhost:55555/test_demo2',
            },
            "apps": {
                "tournaments": {"models": ["__main__"], "default_connection": "first"},
                "events": {"models": ["__main__"], "default_connection": "second"},
            },
        }
    )
    # await Tortoise.generate_schemas()
    client = Tortoise.get_connection("first")
    second_client = Tortoise.get_connection("second")

    tournament = await Tournament.create(name="Tournament")
    await Event(name="Event", tournament_id=tournament.id).save()

    try:
        # await client.execute_query('SELECT * FROM event')
        print(await Tournament.all())
    except OperationalError:
        print("Expected it to fail")
    results = await second_client.execute_query('SELECT * FROM event')
    print(results)
    event = await Event.filter(id=1).first()
    if event:
        team = Team(name='cjs')
        await team.save()
        await event.participants.add(team)
        print(await event.participants.all())


if __name__ == "__main__":
    run_async(run())
