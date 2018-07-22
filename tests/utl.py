SENSORS = [
    {'name': 'abacus',      'categories': ['noise', 'temperature']},
    {'name': 'bushranger',  'categories': ['temperature', 'humidity']},
    {'name': 'camrose',     'categories': ['humidity', 'noise']}
]
CATEGORIES = [
    {'name': 'temperature', 'units': 'C'},
    {'name': 'humidity',    'units': 'RH'},
    {'name': 'noise',       'units': 'dB'}
]

def add_categories_to_db(self):
    for category in CATEGORIES:
        res = self.client.post('/api/categories',
            json={
                'name': category['name'],
                'units': category['units']
        })
        self.assertEqual(res.status_code, 201, res.get_json())

def add_sensors_to_db(self):
    for sensor in SENSORS:
        res = self.client.post('/api/sensors',
            json={
                'name': sensor['name'],
                'categories': sensor['categories']
        })
        self.assertEqual(res.status_code, 201, res.get_json())
