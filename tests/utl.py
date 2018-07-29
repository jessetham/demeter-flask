from random import randint
from app import db
from app.models import Category, Reading, Sensor

# Global list used for test cases. DON'T mutate them here or anywhere else
SENSORS = [
    {'name': 'abacus',      'categories': ['noise', 'temperature']},
    {'name': 'bushranger',  'categories': ['temperature', 'humidity']},
    {'name': 'camrose',     'categories': ['humidity', 'noise']},
    {'name': 'demascus',    'categories': ['brightness', 'energy']},
    {'name': 'evergreen',   'categories': ['humidity', 'temperature', 'noise', 'brightness']},
]
CATEGORIES = [
    {'name': 'temperature', 'units': 'C'},
    {'name': 'humidity',    'units': 'RH'},
    {'name': 'noise',       'units': 'dB'},
    {'name': 'brightness',  'units': 'lx'},
    {'name': 'energy',      'units': 'J'},
]
READINGS = []
READING_UPPER_LIMIT = 100
READING_LOWER_LIMIT = 0

def add_categories_to_db():
    for category in CATEGORIES:
        c = Category()
        c.from_dict(category)
        db.session.add(c)
        db.session.commit()
        category['id'] = c.id

def add_sensors_to_db():
    for sensor in SENSORS:
        s = Sensor()
        s.from_dict(sensor)
        db.session.add(s)
        db.session.commit()
        sensor['id'] = s.id

def add_readings_to_db():
    for sensor in SENSORS:
        for category in sensor['categories']:
            reading = {
                'data': randint(READING_LOWER_LIMIT, READING_UPPER_LIMIT),
                'category': category,
                'sensor': sensor['name']
            }
            r = Reading()
            r.from_dict(reading)
            db.session.add(r)
            db.session.commit()
            reading['id'] = r.id
            READINGS.append(reading)
