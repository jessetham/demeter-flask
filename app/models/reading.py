from datetime import datetime
from app import db
from app.models.category import Category
from app.models.sensor import Sensor
from app.models.mixins import ModelMixin

class Reading(db.Model, ModelMixin):
    __tablename__ = 'reading'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def add_category_to_reading(self, data):
        if 'category' in data:
            category = Category.query.filter_by(name=data['category']).first()
            if category:
                self.category = category

    def add_sensor_to_reading(self, data):
        if 'sensor' in data:
            sensor = Sensor.query.filter_by(name=data['sensor']).first()
            if sensor:
                self.sensor = sensor

    def from_dict(self, data):
        self.add_category_to_reading(data)
        self.add_sensor_to_reading(data)
        for field in ['data', 'timestamp']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        return {
            'id': self.id,
            'data': self.data,
            'sensor': self.sensor.to_dict(),
            'category': self.category.to_dict(),
            'timestamp': self.timestamp
        }
