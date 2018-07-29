from app import db

# Junction table to relate sensors to categories
categories = db.Table('categories',
    db.Column('sensor_id', db.Integer, db.ForeignKey('sensor.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True))

# Junction table to relate users to sensors
sensors = db.Table('sensors',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('sensor_id', db.Integer, db.ForeignKey('sensor.id'), primary_key=True))
