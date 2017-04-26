import logging
import os
import unittest

from pymongo import MongoClient

import repositories
from test.model_admin import AdminTests
from test.model_device import DeviceTests
from test.model_house import HouseTests
from test.model_room import RoomTests
from test.model_device import DeviceTests
from test.model_trigger import TriggerTests
from test.model_theme import ThemeTests
from test.model_usr_mgmt import MgmtTests
from test.model_token import TokenTests
from test.model_user import UserTests

mongo = MongoClient(os.environ['MONGO_HOST'], int(os.environ['MONGO_PORT']))

logging.basicConfig(level=logging.DEBUG)


def main():
    mongo.drop_database('testdb')
    db = mongo.testdb
    repository_collection = repositories.RepositoryCollection(db)
    UserTests.repository_collection = repository_collection
    HouseTests.repository_collection = repository_collection
    RoomTests.repository_collection = repository_collection
    DeviceTests.repository_collection = repository_collection
    TriggerTests.repository_collection = repository_collection
    ThemeTests.repository_collection = repository_collection
    TokenTests.repository_collection = repository_collection
    AdminTests.repository_collection = repository_collection
    MgmtTests.repository_collection = repository_collection
    unittest.main()


if __name__ == "__main__":
    main()
