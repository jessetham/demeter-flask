from app import db
from app.models.category import Category
from app.models.junctions import sensor_category_junction
from app.models.mixins import ModelMixin, PaginatedAPIMixin

class Sensor(db.Model, ModelMixin, PaginatedAPIMixin):
    __tablename__ = 'sensor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    last_updated = db.Column(db.DateTime, index=True)
    readings = db.relationship('Reading', backref='sensor', lazy='dynamic')
    categories = db.relationship(
        'Category', secondary=sensor_category_junction, lazy='subquery',
        backref=db.backref('sensors', lazy=True))

    def __repr__(self):
        return '<Sensor {}>'.format(self.name)

    @staticmethod
    def are_valid_sensors(sensors):
        if not sensors:
            return False
        valid_sensors = set([sensor.name for sensor in Sensor.get_all()])
        for sensor in sensors:
            if sensor not in valid_sensors:
                return False
        return True

    def add_categories(self, categories):
        for category_s in categories:
            # If the category exists in the database, append it to the object
            category_o = Category.query.filter_by(name=category_s).first()
            if category_o and category_o not in self.categories:
                self.categories.append(category_o)

    def remove_categories(self, categories):
        for category_s in categories:
            # If the category exists in the database, remove it from the object
            category_o = Category.query.filter_by(name=category_s).first()
            if category_o and category_o in self.categories:
                self.categories.remove(category_o)

    def from_dict(self, data):
        self.name = data['name']
        self.add_categories(data['categories'])

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'lastUpdated': self.last_updated,
            'categories': [category.to_dict() for category in self.categories]
        }
