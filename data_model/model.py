from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

import api

api.config['MONGO_DBNAME'] = 'iotdb'
api.config['MONGO_URI'] = 'mongodb://localhost:27017/iotdb'

mongo = PyMongo(api)

class User(object):
    def _init_(self, name, password_hash, email_address, is_admin):
        self.user_id = None
        self.name = name
        self.password_hash = password_hash
        self.email_address = email_address
        self.is_admin = is_admin

    def get_user_attributes(self):
        return {'user_id': self.user_id, 'name': self.name, 'password_hash': self.password_hash,
                'email_address': self.email_address, 'is_admin': self.is_admin}

    def set_user_id(self, user_id):
        setattr(self, user_id, user_id)

class UserRepository:
    def _init_(self):
        self.users = mongo.db.users

    def add_user(self, user):
        new_user = User.get_user_attributes(user)
        name = new_user['name']
        password_hash = new_user['password_hash']
        email_address = new_user['email_address']
        is_admin = new_user['is_admin']
        user_id = self.users.insert_one({'name': name, 'password_hash': password_hash,
                                        'email_address': email_address, 'is_admin': is_admin})
        User.set_user_id(user, 'user_id', user_id)

    def remove_user(self, user_id):
        self.users.delete_one({'_id': user_id})

    def get_user_by_id(self, user_id):
        user = self.users.find_one_or_404({'_id': user_id})
        return user

class House(User):
    def _init_(self, name):
        self.user_id = None
        self.house_id = None
        self.name = name

    def get_house_attributes(self):
        return {'user_id': self.user_id, 'house_id': self.house_id, 'name': self.name}

    def set_house_id(self, house_id):
        setattr(self, 'house_id', house_id)

    def set_user(self, user_id):
        setattr(self, 'user_id', user_id)

class HouseRepository:
    def _init_(self):
        self.houses = mongo.db.houses

    def add_house(self, house):
        new_house = House.get_house_attributes(house)
        name = new_house['name']
        house_id = self.houses.insert_one({'name': name})
        House.set_house_id(house, 'house_id', house_id)

    def remove_house(self, house_id):
        self.houses.delete_one({'_id': house_id})

    def get_house_by_id(self, house_id):
        house = self.houses.find_one_or_404({'_id': house_id})
        return house

    def add_house_to_user(self, user, house):
        target_house = House.get_house_attributes(house)
        target_user = User.get_user_attributes(user)
        house_id = target_house['house_id']
        user_id = target_user['user_id']
        House.set_user(house, user_id)
        self.houses.update({'_id': house_id}, {"$set": {'user_id': user_id}}, upsert = False)

    def get_houses_for_user(self, user_id):
        return self.houses.find({'user_id': user_id})

class HouseGroup(object):
    def _init_(self, house__group_id, name):
        self.house_group_id = None
        self.house_ids = []
        self.name = name

    def get_house_group_attributes(self):
        return {'house_group_id': self.house_group_id, 'house_ids': self.house_ids, 'name': self.name}

    def set_house_group_id(self, house_group_id):
        setattr(self, 'house_group_id', house_group_id)

    def add_house_to_group(self, house_id):
        self.house_ids.append(house_id)

class HouseGroupRepository:
    def _init_(self):
        self.house_groups = mongo.db.housegroups

    def add_house_group(self, house_group):
        new_house_group = HouseGroup.get_house_group_attributes(house_group)
        house_ids = new_house_group['house_ids']
        name = new_house_group['name']
        house_group_id = self.house_groups.insert_one({'house_ids': house_ids, 'name': name})
        HouseGroup.set_house_group_id(house_group, house_group_id)


    def add_house_to_group(self, house_group, house):
        target_house = House.get_house_attributes(house)
        target_house_group = HouseGroup.get_house_group_attributes(house_group)
        house_id = target_house['house_id']
        house_group_id = target_house_group['house_group_id']
        self.house_groups.update({'_id': house_group_id}, {"$push": {'house_ids': house_id}}, upsert = False)

    def remove_house_group(self, house_group_id):
        self.house_groups.delete_one({'_id': house_group_id})