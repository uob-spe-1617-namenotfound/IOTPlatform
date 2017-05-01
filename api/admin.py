import click

from main import api


@api.cli.command()
def clear_db():
    click.echo('Clearing the database')
    api.user_repository.clear_db()
    api.house_repository.clear_db()
    api.room_repository.clear_db()
    api.device_repository.clear_db()
    api.trigger_repository.clear_db()
    click.echo("Done.")


def init_hardcoded_data():
    admin_user = api.user_repository.register_new_user(email_address="dr@no.com",
                                                       password="jamaica",
                                                       name="Dr No",
                                                       is_admin=True)
    user_data = [
        ("James Bond", "james@bond.com"),
        ("M", "m@bond.com"),
        ("Miss Moneypenny", "money@bond.com"),
        ("Q", "q@bond.com"),
        ("Felix Leiter", "felix@bond.com"),
        ("Bill Tanner", "bill@bond.com"),
        ("Ernst Stavro Blofeld", "ernst@bond.com"),
        ("General Gogol", "gg@bond.com"),
        ("Sir Frederick Gray", "gray@bond.com"),
        ("Sylvia Trench", "sylvia@bond.com"),
        ("Sheriff J.W. Pepper", "pepper@bond.com")
    ]
    user_ids = []
    house_ids = []
    room_ids = []
    nb_own_light_swithces = 0
    nb_own_thermostats = 0
    nb_own_door_sensors = 0
    nb_own_motion_sensors = 0
    for data in user_data:
        # User
        user_id = api.user_repository.register_new_user(email_address=data[1],
                                                        password="007007",
                                                        name=data[0],
                                                        is_admin=False)
        user_ids.append(user_id)
        # House
        house_id = api.house_repository.add_house(user_id=user_id,
                                                  name="{}'s house".format(data[0]),
                                                  location=None)
        house_ids.append(house_id)
        # Rooms
        kitchen_id = api.room_repository.add_room(house_id=house_id,
                                                  name="{}'s Kitchen".format(data[0]))
        bathroom_id = api.room_repository.add_room(house_id=house_id,
                                                   name="{}'s Bathroom".format(data[0]))
        living_room_id = api.room_repository.add_room(house_id=house_id,
                                                      name="{}'s Living room".format(data[0]))
        room_ids.append([kitchen_id, bathroom_id, living_room_id])
        # Devices
        kitchen_faulty_thermostat_id = api.device_repository.add_device(
            house_id=house_id,
            room_id=kitchen_id,
            name="Faulty thermostat",
            device_type="thermostat",
            target={'target_temperature': 20},
            configuration={"url": "http://dummy-sensor:5000/faulty_thermostat"},
            vendor="OWN")
        nb_own_motion_sensors += 1
        kitchen_motion_sensor_id = api.device_repository.add_device(
            house_id=house_id,
            room_id=kitchen_id,
            name="Motion Sensor",
            device_type="motion_sensor",
            target={},
            configuration={"url": "http://dummy-sensor:5000/motion_sensor/{}".format(nb_own_motion_sensors)},
            vendor="OWN")
        kitchen_light_switch_id = api.device_repository.add_device(
            house_id=house_id,
            room_id=kitchen_id,
            name="Kitchen Light Switch",
            device_type="light_switch",
            target={'power_state': 0},
            configuration={
                "username": 'bc15050@mybristol.ac.uk',
                "password": 'test1234',
                "device_id": '46865'
            },
            vendor="energenie")
        nb_own_light_swithces += 1
        bathroom_light_switch_id = api.device_repository.add_device(
            house_id=house_id,
            room_id=bathroom_id,
            name="Bathroom light switch",
            device_type="light_switch",
            target={},
            configuration={
                "url": "http://dummy-sensor:5000/light_switch/{}".format(nb_own_light_swithces)
            },
            vendor='OWN')
        nb_own_thermostats += 1
        bathroom_thermostat_id = api.device_repository.add_device(
            house_id=house_id,
            room_id=bathroom_id,
            name="Working thermostat",
            device_type="thermostat",
            target={'target_temperature': 20},
            configuration={"url": "http://dummy-sensor:5000/thermostat/{}".format(nb_own_thermostats)},
            vendor="OWN")
        nb_own_motion_sensors += 1
        living_room_motion_sensor_id = api.device_repository.add_device(
            house_id=house_id,
            room_id=living_room_id,
            name="Living Room Motion Sensor",
            device_type="motion_sensor",
            target=None,
            configuration={"url": "http://dummy-sensor:5000/motion_sensor/{}".format(nb_own_motion_sensors)},
            vendor="OWN")

        # Themes
        api.theme_repository.add_theme(
            user_id=user_id,
            name="{}'s Holiday Theme".format(data[0]),
            settings=[{
                "device_id": bathroom_light_switch_id,
                "setting": {
                    "power_state": 0
                }
            }, {
                "device_id": kitchen_light_switch_id,
                "setting": {
                    "power_state": 0
                }
            }, {
                "device_id": bathroom_thermostat_id,
                "target_temperature": 12
            }],
            active=False)
        api.theme_repository.add_theme(
            user_id=user_id,
            name="{}'s Party Theme".format(data[0]),
            settings=[{
                "device_id": bathroom_thermostat_id,
                "setting": {
                    "target_temperature": 19
                }
            }],
            active=False
        )



@api.cli.command()
def fill_hardcoded_db():
    click.echo("Filling the database with dummy data")
    init_hardcoded_data()
    click.echo("Done.")
