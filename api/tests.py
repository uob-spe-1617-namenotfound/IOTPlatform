from pymongo import MongoClient
from test.model_user import UserTests
from test.model_house import HouseTests
from test.model_room import RoomTests
from test.model_device import DeviceTests
from test.model_usr_mgmt import MgmtTests
from test.model_token import TokenTests
from test.model_admin import AdminTests

import repositories
import unittest

import os
print(os.environ)
mongo = MongoClient(os.environ['MONGO_HOST'], int(os.environ['MONGO_PORT']))
db = mongo.testdb


def main():
    mongo.drop_database('testdb')
    repository_collection = repositories.RepositoryCollection(db)
    UserTests.collection = db.user_test
    UserTests.repositories = repository_collection
    HouseTests.collection = db.house_test
    HouseTests.repositories = repository_collection
    RoomTests.collection = db.room_test
    RoomTests.repositories = repository_collection
    DeviceTests.collection = db.device_test
    DeviceTests.repositories = repository_collection
    MgmtTests.collection = db.user_test
    MgmtTests.repositories = repository_collection
    TokenTests.collection = db.token_test
    TokenTests.repositories = repository_collection
    AdminTests.collection = db.device_test
    AdminTests.repositories = repository_collection
    unittest.main()

if __name__ == "__main__":
    main()
