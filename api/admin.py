import click
import model
from main import api


@api.cli.command()
def clear_db():
    click.echo('Clearing the database')
    api.user_repository.clear_db()
    api.house_repository.clear_db()
    api.room_repository.clear_db()
    api.device_repository.clear_db()
    api.devicegroup_repository.clear_db()
    api.trigger_repository.clear_db()
    click.echo("Done.")


def init_hardcoded_data():
    user1 = model.User("Jack Xia", "xxxxxxxx", "nobody@gmail.com", False)
    api.user_repository.add_user(user1)
    house1 = model.House("Jack's house", user1.get_user_id())
    api.house_repository.add_house(house1)
    room1 = model.Room("Kitchen", house1.get_house_id())
    api.room_repository.add_room(room1)
    room2 = model.Room("Bathroom", house1.get_house_id())
    api.room_repository.add_room(room2)
    room3 = model.Room("Living Room", house1.get_house_id())
    api.room_repository.add_room(room3)
    # device1 = model.Device("house_id_1", "'room_id_1", "device_id_1", "Thermostat", 1)
    # device_repository.add_device(device1)
    devicegroup = model.DeviceGroup("Group 1")
    api.devicegroup_repository.add_device_group(devicegroup)


@api.cli.command()
def fill_hardcoded_db():
    click.echo("Filling the database with dummy data")
    init_hardcoded_data()
    click.echo("Done.")
