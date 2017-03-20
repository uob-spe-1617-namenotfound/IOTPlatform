import click

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
    # user2 = api.user_repository.add_user("Ben Fossett", "xxxxxxxx", "nobody@gmail.com", False)
    house1 = api.house_repository.add_house(user1, "Jack's House")
    # house2 = api.house_repository.add_house(user2, "Ben's House")
    room1 = api.room_repository.add_room(house1, "Kitchen")
    room2 = api.room_repository.add_room(house1, "Bathroom")
    room3 = api.room_repository.add_room(house1, "Living Room")
    faulty_device = api.device_repository.add_device(house1, room1, "Faulty thermostat", "thermostat", 1,
                                                     {"url": "http://dummy-sensor:5000/faulty_thermostat"},
                                                     vendor="OWN")
    adapter1 = api.device_repository.add_device(house1, None, "Test Adapter", "light_switch", 1,
                                                {"username": 'bc15050@mybristol.ac.uk',
                                                 "password": 'test1234',
                                                 "device_id": '46865'}, 'energenie')
    motion_sensor = api.device_repository.add_device(house1, room3, "Motion Sensor", "motion_sensor", 1,
                                                     {"url": "http://dummy-sensor:5000/motion_sensor"},
                                                     vendor="OWN")
    good_thermostat = api.device_repository.add_device(house1, None, "Working thermostat", "thermostat", 1, {
        "url": "http://dummy-sensor:5000/thermostat/3"
    }, vendor="OWN")
    # device2 = api.device_repository.add_device(house1, None, "Living Room Motion Sensor", "motion_sensor", 1)
    # device3 = api.device_repository.add_device(house1, None, "Kitchen Light Switch", "light_switch", 1)
    # device_ids1 = [device1, device2, device3]
    # devicegroup1 = api.devicegroup_repository.add_device_group(device_ids1, "Group 1")


@api.cli.command()
def fill_hardcoded_db():
    click.echo("Filling the database with dummy data")
    init_hardcoded_data()
    click.echo("Done.")
