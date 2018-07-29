from app import db

# Junction table to relate sensors to categories
sensor_category_junction = db.Table('sensor_category_junction',
    db.Column('sensor_id', db.Integer, db.ForeignKey('sensor.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True))

# Junction table to relate users to sensors
user_sensor_junction = db.Table('user_sensor_junction',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('sensor_id', db.Integer, db.ForeignKey('sensor.id'), primary_key=True))
