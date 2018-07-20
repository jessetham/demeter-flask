from datetime import datetime
from flask import url_for
from app import db

categories = db.Table('categories',
    db.Column('sensor_id', db.Integer, db.ForeignKey('sensor.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True))

class ModelMixin:
    @classmethod
    def get_all(cls):
        return cls.query.all()

class PaginatedAPIMixin:
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        return {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                    **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                    **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                    **kwargs) if resources.has_prev else None
            }
        }

class Sensor(db.Model, ModelMixin, PaginatedAPIMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    last_updated = db.Column(db.DateTime, index=True)
    readings = db.relationship('Reading', backref='sensor', lazy='dynamic')
    categories = db.relationship('Category', secondary=categories, lazy='subquery',
        backref=db.backref('sensors', lazy=True))

    def __repr__(self):
        return '<Sensor {}>'.format(self.name)

    def from_dict(self, data):
        for field in ['name']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'lastUpdated': self.last_updated
        }

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
            'timestamp': self.timestamp
        }

class Category(db.Model, ModelMixin, PaginatedAPIMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    units = db.Column(db.String(16), unique=True)
    readings = db.relationship('Reading', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<Category {}>'.format(self.name)

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