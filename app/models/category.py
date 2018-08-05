from app import db
from app.models.mixins import ModelMixin, PaginatedAPIMixin

class Category(db.Model, ModelMixin, PaginatedAPIMixin):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    units = db.Column(db.String(16), unique=True)
    readings = db.relationship('Reading', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<Category {}>'.format(self.name)

    @staticmethod
    def are_valid_categories(categories):
        if not categories:
            return False
        valid_categories = set([category.name for category in Category.get_all()])
        for category in categories:
            if category not in valid_categories:
                return False
        return True

    def from_dict(self, data):
        for field in ['name', 'units']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'units': self.units
        }
