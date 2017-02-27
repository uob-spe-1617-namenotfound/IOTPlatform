from pymongo import MongoClient
from test.model_user import UserTests
from test.model_house import HouseTests
from test.model_room import RoomTests
from test.model_device import DeviceTests
import unittest

import os
print(os.environ)
mongo = MongoClient(os.environ['MONGO_HOST'], int(os.environ['MONGO_PORT']))
db = mongo.testdb

def main():
    mongo.drop_database('testdb')
    UserTests.collection = db.user_test
    HouseTests.collection = db.house_test
    RoomTests.collection = db.room_test
    DeviceTests.collection = db.device_test
    unittest.main()

if __name__ == "__main__":
    main()
