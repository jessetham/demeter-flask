from datetime import datetime
from app import db
from app.models.mixins import ModelMixin

class Reading(db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def from_dict(self, data):
        for field in ['data']:
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
