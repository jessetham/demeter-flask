import os
import base64
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models.junctions import user_sensor_junction
from app.models.mixins import ModelMixin, PaginatedAPIMixin
from app.models.sensor import Sensor

class User(db.Model, ModelMixin, PaginatedAPIMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    sensors = db.relationship(
        'Sensor', secondary=user_sensor_junction, lazy=True,
        backref=db.backref('users', lazy=True))
    password_hash = db.Column(db.String(128))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def add_sensors(self, sensors):
        for sensor_s in sensors:
            # If the sensor exists in the database, append it to the object
            sensor_o = Sensor.query.filter_by(name=sensor_s).first()
            if sensor_o and sensor_o not in self.sensors:
                self.sensors.append(sensor_o)

    def remove_sensors(self, sensors):
        for sensor_s in sensors:
            # If the category exists in the database, remove it from the object
            sensor_o = Sensor.query.filter_by(name=sensor_s).first()
            if sensor_o and sensor_o in self.sensors:
                self.sensors.remove(sensor_o)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and \
            self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if not user or user.token_expiration < datetime.utcnow():
            return None
        return user

    def from_dict(self, data):
        self.name = data['name']
        self.set_password(data['password'])
        self.add_sensors(data['sensors'])

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'password_hash': self.password_hash,
            'sensors': [sensor.to_dict() for sensor in self.sensors]
        }
