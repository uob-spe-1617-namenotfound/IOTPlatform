from flask import Flask, jsonify

from data_model import model

api = Flask("SPE-IoT-API")
api.config.from_pyfile('data_model/config.cfg')

user_repository = model.UserRepository()
user1 = model.User("user_id_1", "Floris Kint", "xxxxxxxx", "nobody@gmail.com", False)
user_repository.add_user(user1)


@api.route('/user/<string:user_id>')
def get_user_info(user_id):
    user = user_repository.get_user_by_id(user_id)
    return jsonify({"user": user.get_user_attributes(), "error": None})


def main():
    api.run(debug=True, host=api.config['HOSTNAME'], port=int(api.config['PORT']))


if __name__ == "__main__":
    main()