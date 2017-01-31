from flask import render_template
import data_interface
from main import app

@app.route('/admin/faulty_devices', methods=['GET'])
def admin_faulty_devices():
    faulty_devices = data_interface.get_faulty_devices()
    devices = []
    for d in faulty_devices:
        house = data_interface.get_house_info(d['house_id'])
        user = data_interface.get_user_info(house['user_id'])
        devices.append({"device": d, "user": user})
    return render_template("admin/faulty_devices.html", devices=devices)



@app.route('/admin')
def admin():
    users = data_interface.get_all_users()
    print(users)
    return render_template("admin/admin.html", users=users)


@app.route('/admin_map')
def admin_map():
    house1 = {'lat': 51.529249, 'lng': -0.117973}
    house2 = {'lat': 53.472605, 'lng': -2.227532}
    house3 = {'lat': 10.000, 'lng': 120.000}
    house_location = [house1, house2, house3]
    return render_template("admin/admin_maps.html", house_location=house_location)
