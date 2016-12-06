from flask import Flask, jsonify

from data_model import model

api = Flask("SPE-IoT-API")
api.config.from_pyfile('data_model/config.cfg')

user_repository = model.UserRepository()
user1 = model.User("user_id_1", "Jack Xia", "xxxxxxxx", "nobody@gmail.com", False)
user_repository.add_user(user1)
house = model.HouseRepository()
house1 = model.House("user_id_1","house_id_1","Jack")
room_repository = model.RoomRepository()
room1 = model.Room("house_id_1","Room_id_1", "Kitchen")
room_repository.add_room(room1)
room2 = model.Room("house_id_1","Room_id_2", "Bathroom")
room_repository.add_room(room2)
room3 = model.Room("house_id_1","Room_id_3", "Living Room")
room_repository.add_room(room3)
device_repository = model.DeviceRepository()
devicegroup = model.DeviceGroupRepository()

@api.route('/user/<string:user_id>')
def get_user_info(user_id):
    user = user_repository.get_user_by_id(user_id)
    return jsonify({"user": user.get_user_attributes(), "error": None})

@api.route('/user/<string:user_id>)/rooms')
def get_room_info(room_id):
    room = room_repository.get_room_by_id(room_id)
    return jsonify({"room":room.get_room_attributes(), "errors": None})

@api.route('')


def main():
    api.run(debug=True, host=api.config['HOSTNAME'], port=int(api.config['PORT']))


if __name__ == "__main__":
    main()

