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
    user1 = api.user_repository.add_user("Jack Xia", "xxxxxxxx", "nobody@gmail.com", False)
    house1 = api.house_repository.add_house(user1, "Jack's House")
    room1 = api.room_repository.add_room(house1.get_house_id(), "Kitchen")
    room2 = api.room_repository.add_room(house1.get_house_id(), "Bathroom")
    room3 = api.room_repository.add_room(house1.get_house_id(), "Living Room")
    device1 = model.Device(house1.get_house_id(), room1, "My Thermostat", "Thermostat", 1)
    api.device_repository.add_device(device1)
    devicegroup = model.DeviceGroup("Group 1")
    api.devicegroup_repository.add_device_group(devicegroup)


@api.cli.command()
def fill_hardcoded_db():
    click.echo("Filling the database with dummy data")
    init_hardcoded_data()
    click.echo("Done.")
