from tortoise import Tortoise, fields, run_async
from tortoise.functions import Coalesce, Count, Length, Lower, Min, Sum, Trim, Upper, Max
from tortoise.models import Model
from tortoise.query_utils import Q


class Tournament(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    desc = fields.TextField(null=True)

    events: fields.ReverseRelation["Event"]

    def __str__(self):
        return self.name


class Event(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    tournament = fields.ForeignKeyField(
        "models.Tournament", related_name="events"
    )
    participants = fields.ManyToManyField(
        "models.Team", related_name="events", through="event_team"
    )

    def __str__(self):
        return self.name


class Team(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()

    events: fields.ManyToManyRelation[Event]

    def __str__(self):
        return self.name


async def run():
    await Tortoise.init(db_url="mysql://root:123456@localhost:55555/test_demo", modules={"models": ["__main__"]})
    await Tortoise.generate_schemas()
    tournament = await Tournament.create(name="New Tournament", desc="great")
    await tournament.save()
    await Tournament.create(name="Second tournament")
    await Tournament.create(name=" final tournament ")
    await Event(name="Without participants", tournament_id=tournament.id).save()
    event = Event(name="Test", tournament_id=tournament.id)
    await event.save()
    participants = []
    for i in range(10):
        team = Team(name=f"Team {(i + 1)}")
        await team.save()
        participants.append(team)

    await event.participants.add(*participants)

    # await event.participants.add(participants[0], participants[1])

    print(await Tournament.all().annotate(events_count=Count("events")).filter(events_count__lte=3).values())
    print(
        await Tournament
        .annotate(events_count_with_filter=Count("events", _filter=Q(name="New Tournament")))
        .filter(events_count_with_filter__gte=0).values()
    )

    print(await Event.annotate(lowest_team_id=Count("participants__id")).values())

    print(await Tournament.annotate(events_count=Count("events")).order_by("events_count"))

    print(await Event.annotate(tournament_test_id=Sum("tournament__id")).first())

    print(
        await Tournament.annotate(clean_desciption=Coalesce("desc", "hehe")).values()
    )

    print(
        await Tournament.annotate(trimmed_name=Trim("name")).values()
    )

    print(
        await Tournament.annotate(name_len=Length("name")).filter(
            name_len__gt=len("New Tournament")
        )
    )

    print(await Tournament.annotate(name_lo=Lower("name")).filter(name_lo="new tournament").values())
    print(await Tournament.annotate(name_lo=Upper("name")).filter(name_lo="NEW TOURNAMENT").values())

    print()

if __name__ == "__main__":
    run_async(run())