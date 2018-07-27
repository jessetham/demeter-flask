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

def add_categories_to_db(self):
    for category in CATEGORIES:
        res = self.client.post('/api/categories', json=category)
        self.assertEqual(res.status_code, 201, res.get_json())
        category['id'] = res.get_json()['id']

def add_sensors_to_db(self):
    for sensor in SENSORS:
        res = self.client.post('/api/sensors', json=sensor)
        self.assertEqual(res.status_code, 201, res.get_json())
        sensor['id'] = res.get_json()['id']
