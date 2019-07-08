from app import db
from app.models.category import Category
from app.models.sensor import Sensor
from app.models.mixins import ModelMixin


class Reading(db.Model, ModelMixin):
    __tablename__ = "reading"
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey("sensor.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))

    def add_category(self, category_s):
        category_o = Category.query.filter_by(name=category_s).first()
        if category_o:
            self.category = category_o

    def add_sensor(self, sensor_s):
        sensor_o = Sensor.query.filter_by(name=sensor_s).first()
        if sensor_o:
            self.sensor = sensor_o

    def from_dict(self, data):
        self.add_category(data["category"])
        self.add_sensor(data["sensor"])
        for field in ["data", "timestamp"]:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        return {
            "id": self.id,
            "data": self.data,
            "sensor": self.sensor.to_dict(),
            "category": self.category.to_dict(),
            "timestamp": self.timestamp,
        }
