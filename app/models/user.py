from app import db
from app.models.junctions import user_sensor_junction
from app.models.mixins import ModelMixin

class User(db.Model, ModelMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    sensors = db.relationship(
        'Sensor', secondary=user_sensor_junction, lazy=True,
        backref=db.backref('users', lazy=True))

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def add_sensors(self, data):
        pass

    def remove_sensors(self, data):
        pass

    def from_dict(self, data):
        if 'name' in data:
            self.name = data['name']
        self.add_sensors(data)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
