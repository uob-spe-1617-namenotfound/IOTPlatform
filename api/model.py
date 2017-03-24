import logging
import time

import requests


def get_optional_attribute(attributes, key, default_value=None):
    return attributes[key] if key in attributes else default_value


class User(object):
    def __init__(self, attributes):
        self.user_id = None
        self.name = None
        self.password_hash = None
        self.email_address = None
        self.is_admin = None
        self.faulty = None
        self.set_attributes(attributes)

    def set_attributes(self, attributes):
        self.user_id = attributes['_id']
        self.name = attributes['name']
        self.email_address = attributes['email_address']
        self.password_hash = attributes['password_hash']
        self.is_admin = attributes['is_admin']
        self.faulty = get_optional_attribute(attributes, 'faulty', False)

    def get_user_attributes(self):
        return {'user_id': self.user_id, 'name': self.name, 'password_hash': self.password_hash,
                'faulty': self.faulty, 'email_address': self.email_address, 'is_admin': self.is_admin}

    def get_user_id(self):
        return self.user_id


class House(object):
    def __init__(self, attributes):
        self.house_id = None
        self.user_id = None
        self.name = None
        self.location = None
        self.set_attributes(attributes)

    def set_attributes(self, attributes):
        self.house_id = attributes['_id']
        self.user_id = attributes['user_id']
        self.name = attributes['name']
        self.location = get_optional_attribute(attributes, 'location', None)

    def get_house_attributes(self):
        return {'house_id': self.house_id, 'user_id': self.user_id, 'name': self.name, 'location': self.location}

    def get_house_id(self):
        return self.house_id


class Room(object):
    def __init__(self, attributes):
        self.room_id = None
        self.house_id = None
        self.name = None
        self.set_attributes(attributes)

    def set_attributes(self, attributes):
        self.room_id = attributes['_id']
        self.house_id = attributes['house_id']
        self.name = attributes['name']

    def get_room_attributes(self):
        return {'room_id': self.room_id, 'house_id': self.house_id, 'name': self.name}

    def get_room_id(self):
        return self.room_id


class Device(object):
    def __init__(self, attributes):
        self.device_id = None
        self.house_id = None
        self.room_id = None
        self.name = None
        self.device_type = None
        self.vendor = None
        self.configuration = None
        self.faulty = None
        self.target = {}
        self.status = {}
        self.set_attributes(attributes)

    def set_attributes(self, attributes):
        self.device_id = attributes['_id']
        self.house_id = attributes['house_id']
        self.room_id = attributes['room_id']
        self.name = attributes['name']
        self.device_type = attributes['device_type']
        self.faulty = get_optional_attribute(attributes, 'faulty', False)
        self.target = get_optional_attribute(attributes, 'target', {})
        self.status = get_optional_attribute(attributes, 'status', {})
        self.vendor = get_optional_attribute(attributes, 'vendor', None)
        self.configuration = get_optional_attribute(attributes, 'configuration', None)

    def get_device_attributes(self):
        return {'_id': str(self.device_id), 'device_id': str(self.device_id), 'house_id': self.house_id,
                'room_id': self.room_id, 'name': self.name, 'device_type': self.device_type,
                'faulty': self.faulty, 'target': self.target, 'status': self.status,
                'vendor': self.vendor, 'configuration': self.configuration}

    def get_device_id(self):
        return self.device_id

    def read_current_state(self):
        error = None
        data = None
        timestamp = str(time.time())
        if self.vendor == "OWN":
            if "url" in self.configuration:
                url = self.configuration['url']
                try:
                    r = requests.get(url)
                    r_data = r.json()
                    if "error" in r_data and r_data["error"] is not None:
                        error = r_data["error"]
                    else:
                        data = r_data['data']
                except Exception as ex:
                    error = "Cannot read data from configuration URL: {}".format(ex)
            else:
                error = "Can't read current state as no url is set in configuration"
        elif self.vendor == "energenie":
            if "username" in self.configuration and "password" in self.configuration and "device_id" in self.configuration:
                try:
                    username = self.configuration['username']
                    password = self.configuration['password']
                    dev_id = int(self.configuration['device_id'])
                    logging.debug(
                        "Retrieving mihome4u data. Auth = {}, json = {}".format((username, password), {"id": dev_id}))
                    r = requests.get("https://mihome4u.co.uk/api/v1/subdevices/show", auth=(username, password),
                                     json={"id": dev_id})
                    r_data = r.json()
                    logging.debug("Got: {}".format(r_data))
                    if r_data["status"] != "success":
                        error = "External error: {}".format(r_data['status'])
                    else:
                        data = {'power_state': r_data['data']['power_state'], 'voltage': r_data['data']['voltage']}
                except Exception as ex:
                    error = "Cannot read device data from URL: {}".format(ex)
            else:
                error = "Not all required information is set in the configuration"
            logging.debug("Read current data for the device: {}".format(data))
        else:
            error = "read_current_state not implemented for vendor {}".format(self.vendor)
        if error is not None:
            return {"error": error, "timestamp": timestamp}
        return {"data": data, "timestamp": timestamp}

    def is_faulty(self):
        if "error" in self.status['last_read'] and self.status['last_read']['error'] is not None:
            self.faulty = True
        return self.faulty

# TODO: Fix set_attribute method names.
class Thermostat(Device):
    def __init__(self, attributes):
        Device.__init__(self, attributes)
        self.temperature_scale = None
        self.target['target_temperature'] = None
        self.status['last_temperature'] = None
        self.status['power_state'] = None
        if self.vendor == 'netatmo':
            self.target['locked_max_temp'] = None
            self.target['locked_min_temp'] = None

    def set_attributes(self, attributes):
        attributes['device_type'] = "thermostat"
        Device.set_attributes(self, attributes=attributes)
        self.temperature_scale = get_optional_attribute(attributes, 'temperature_scale')
        self.target['target_temperature'] = get_optional_attribute(attributes, 'target_temperature')
        self.status['last_temperature'] = get_optional_attribute(attributes, 'last_temperature')
        self.status['power_state'] = get_optional_attribute(attributes, 'power_state')
        if self.vendor == 'netatmo':
            self.target['locked_max_temp'] = get_optional_attribute(attributes, 'locked_max_temperature')
            self.target['locked_min_temp'] = get_optional_attribute(attributes, 'locked_min_temperature')

    def get_device_attributes(self):
        attributes = Device.get_device_attributes(self)
        attributes.update({
            'target': self.target, 'status': self.status, 'temperature_scale': self.temperature_scale
        })
        return attributes

    def configure_target_temperature(self, temperature):
        error = None
        data = None
        timestamp = str(time.time())
        if self.vendor == "OWN":
            if "url" in self.configuration:
                url = self.configuration['url'] + "/write"
                try:
                    r = requests.post(url, json={"target_temperature": temperature})
                    r_data = r.json()
                    if "error" in r_data and r_data["error"] is not None:
                        error = r_data["error"]
                except Exception as ex:
                    error = "Cannot configure target temperature from configuration URL: {}".format(ex)
            else:
                error = "Can't configure target temperature as no url is set in configuration"
        elif self.vendor == "energenie":
            if "username" in self.configuration and "password" in self.configuration and "device_id" in self.configuration:
                try:
                    username = self.configuration['username']
                    password = self.configuration['password']
                    dev_id = int(self.configuration['device_id'])
                    logging.debug(
                        "Configuring target temp for mihome4u data. Auth = {}, json = {}".format((username, password), {"id": dev_id}))
                    r = requests.get("https://mihome4u.co.uk/api/v1/subdevices/set_target_temperature", auth=(username, password),
                                     json={"id": dev_id, "target_temperature": temperature}, params={"id": dev_id, "temperature": temperature})
                    r_data = r.json()
                    logging.debug("Got: {}".format(r_data))
                    if r_data["status"] != "success":
                        error = "External error: {}".format(r_data['status'])
                    else:
                        data = {'target_temperature': r_data['data']['target_temperature'], 'voltage': r_data['data']['voltage']}
                except Exception as ex:
                    error = "Cannot read device data from URL: {}".format(ex)
            else:
                error = "Not all required information is set in the configuration"
            logging.debug("Read current data for the device: {}".format(data))
        else:
            error = "configure_target_temperature not implemented for vendor {}".format(self.vendor)
        if error is not None:
            return {"error": error, "timestamp": timestamp}


class MotionSensor(Device):
    def __init__(self, attributes):
        Device.__init__(self, attributes)
        self.sensor_data = None
        self.status = {}

    def set_attributes(self, attributes):
        Device.set_attributes(self, attributes=attributes)
        self.sensor_data = get_optional_attribute(attributes, 'sensor_data')

    def get_device_attributes(self):
        attributes = Device.get_device_attributes(self)
        attributes.update({'sensor_data': self.sensor_data})
        return attributes

    # TODO: verify if this + OpenSensor get_data method are needed or if to just call read_current_state
    def get_sensor_data(self):
        error = None
        data = None
        timestamp = str(time.time())
        if self.vendor == "OWN":
            if "url" in self.configuration:
                url = self.configuration['url'] + "/write"
                try:
                    r = requests.post(url, json={"data": data})
                    r_data = r.json()
                    if "error" in r_data and r_data["error"] is not None:
                        error = r_data["error"]
                except Exception as ex:
                    error = "Cannot get sensor data from configuration URL: {}".format(ex)
            else:
                error = "Can't get sensor data as no url is set in configuration"
        # elif self.vendor == "energenie":
        #     if "username" in self.configuration and "password" in self.configuration and "device_id" in self.configuration:
        #         try:
        #             device_state = Device.read_current_state(self)
        #             if device_state['error'] is None:
        #                 first_data = device_state['data']
        #                 second_data = first_data['data']
        #                 sensor_data = second_data['historical_sensor_data']
        else:
            error = "get_sensor_data not implemented for vendor {}".format(self.vendor)
        if error is not None:
            return {"error": error, "timestamp": timestamp}
        return {"data": data, "timestamp": timestamp}


class LightSwitch(Device):
    def __init__(self, attributes):
        Device.__init__(self, attributes)
        self.status['power_state'] = None

    def set_attributes(self, attributes):
        Device.set_attributes(self, attributes=attributes)
        self.status['power_state'] = get_optional_attribute(attributes, 'power_state')

    def get_device_attributes(self):
        return Device.get_device_attributes(self)

    def configure_power_state(self, power_state):
        error = None
        if self.vendor == "energenie":
            if "username" in self.configuration and "password" in self.configuration and "device_id" in self.configuration:
                try:
                    username = self.configuration['username']
                    password = self.configuration['password']
                    dev_id = int(self.configuration['device_id'])
                    logging.debug(
                        "Setting power state mihome4u data. Auth = {}, json = {}".format((username, password),
                                                                                         {"id": dev_id}))
                    r = requests.get(
                        "https://mihome4u.co.uk/api/v1/subdevices/power_{}".format("on" if power_state == 1 else "off"),
                        auth=(username, password),
                        json={"id": dev_id})
                    r_data = r.json()
                    logging.debug("Got: {}".format(r_data))
                    if r_data["status"] != "success":
                        error = "External error: {}".format(r_data['status'])
                except Exception as ex:
                    error = "Cannot configure power state: {}".format(ex)
            else:
                error = "Not all required information is set in the configuration"
        else:
            error = "configure_power_state not implemented for vendor {}".format(self.vendor)
        return error


class OpenSensor(Device):
    def __init__(self, attributes):
        self.sensor_data = None
        Device.__init__(self, attributes)

    def set_attributes(self, attributes):
        Device.set_attributes(self, attributes=attributes)
        self.sensor_data = attributes["sensor_data"]

    def get_device_attributes(self):
        attributes = Device.get_device_attributes(self)
        attributes.update({'sensor_data': self.sensor_data})
        return attributes

    def get_sensor_data(self):
        error = None
        data = None
        timestamp = str(time.time())
        if self.vendor == "OWN":
            if "url" in self.configuration:
                url = self.configuration['url'] + "/write"
                try:
                    r = requests.post(url, json={"data": data})
                    r_data = r.json()
                    if "error" in r_data and r_data["error"] is not None:
                        error = r_data["error"]
                except Exception as ex:
                    error = "Cannot get sensor data from configuration URL: {}".format(ex)
            else:
                error = "Can't get sensor data as no url is set in configuration"
        else:
            error = "get_sensor_data not implemented for vendor {}".format(self.vendor)
        if error is not None:
            return {"error": error, "timestamp": timestamp}
        return {"data": data, "timestamp": timestamp}


class DeviceGroup(object):
    def __init__(self, device_group_id, device_ids, name):
        self.device_group_id = device_group_id
        self.device_ids = device_ids
        self.name = name

    def get_device_group_attributes(self):
        return {'device_group_id': self.device_group_id, 'device_ids': self.device_ids, 'name': self.name}


class Trigger:
    def __init__(self, trigger, action):
        self.trigger_id = None
        self.trigger_sensor_id = None
        self.trigger = trigger
        self.actor_id = None
        self.action = action

    def get_trigger_attributes(self):
        return {'trigger_id': self.trigger_id, 'trigger_sensor_id': self.trigger_sensor_id,
                'trigger': self.trigger, 'actor_id': self.actor_id, 'action': self.action}


class Token:
    def __init__(self, token_id, user_id, token):
        self.token_id = token_id
        self.user_id = user_id
        self.token = token

    def get_token_attributes(self):
        return {'token_id': self.token_id, 'user_id': self.user_id, 'key': self.token}
