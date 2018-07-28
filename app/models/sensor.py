from app import db
from app.models.category import Category
from app.models.junctions import categories as categories_junction
from app.models.mixins import ModelMixin, PaginatedAPIMixin

class Sensor(db.Model, ModelMixin, PaginatedAPIMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    last_updated = db.Column(db.DateTime, index=True)
    readings = db.relationship('Reading', backref='sensor', lazy='dynamic')
    categories = db.relationship('Category', secondary=categories_junction, lazy='subquery',
        backref=db.backref('sensors', lazy=True))

    def __repr__(self):
        return '<Sensor {}>'.format(self.name)

    def add_categories(self, data):
        if 'categories' in data:
            for category_s in data['categories']:
                # If the category exists in the database, append it to the object
                category_o = Category.query.filter_by(name=category_s).first()
                if category_o and category_o not in self.categories:
                    self.categories.append(category_o)

    def remove_categories(self, data):
        if 'categories' in data:
            for category_s in data['categories']:
                # If the category exists in the database, remove it from the object
                category_o = Category.query.filter_by(name=category_s).first()
                if category_o and category_o in self.categories:
                    self.categories.remove(category_o)

    def add_name(self, data):
        if 'name' in data:
            self.name = data['name']

    def from_dict(self, data):
        self.add_name(data)
        self.add_categories(data)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'lastUpdated': self.last_updated,
            'categories': [category.to_dict() for category in self.categories]
        }
