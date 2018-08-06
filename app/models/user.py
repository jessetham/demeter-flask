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

    def from_dict(self, data):
        self.name = data['name']
        self.add_sensors(data['sensors'])

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'sensors': [sensor.to_dict() for sensor in self.sensors]
        }
