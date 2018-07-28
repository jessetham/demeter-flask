from random import randint
from app import db
from app.models import Category

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

def add_categories_to_db(self):
    for category in CATEGORIES:
        c = Category()
        c.from_dict(category)
        db.session.add(c)
        db.session.commit()
        category['id'] = c.id

def add_sensors_to_db(self):
    for sensor in SENSORS:
        res = self.client.post('/api/sensors', json=sensor)
        self.assertEqual(res.status_code, 201, res.get_json())
        sensor['id'] = res.get_json()['id']

def add_readings_to_db(self):
    for sensor in SENSORS:
        for category in sensor['categories']:
            reading = {
                'data': randint(READING_LOWER_LIMIT, READING_UPPER_LIMIT),
                'category': category
            }
            res = self.client.post('/api/sensors/{}/readings'.format(sensor['id']),
                json=reading
            )
            self.assertEqual(res.status_code, 201, res.get_json())
            reading['id'] = res.get_json()['id']
            reading['sensor'] = res.get_json()['sensor']['id']
            reading['category'] = res.get_json()['category']['id']
            READINGS.append(reading)
