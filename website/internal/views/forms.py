from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators


class AddNewRoomForm(FlaskForm):
    name = StringField("Room name", [validators.Length(min=1)])
    submit = SubmitField()
