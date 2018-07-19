from datetime import datetime
from flask import request, jsonify, url_for
from app import app, db
from app.api.errors import bad_request
from app.models import Sensor, Reading

@app.route('/api/sensors/<int:sensor_id>/readings', methods=['POST'])
def create_reading(sensor_id):
    data = request.get_json() or {}
    if 'data' not in data:
        return bad_request('must include data field')
    # Check if a sensor for the given sensor_id exists
    sensor = Sensor.query.get_or_404(sensor_id)
    reading = Reading(sensor=sensor, timestamp=datetime.utcnow())
    reading.from_dict(data)
    db.session.add(reading)
    sensor.last_updated = reading.timestamp
    db.session.add(sensor)
    db.session.commit()
    response = jsonify(reading.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('get_reading', reading_id=reading.id,
        sensor_id=sensor.id)
    return response

@app.route('/api/sensors/<int:sensor_id>/readings/<int:reading_id>', methods=['GET'])
def get_reading(sensor_id, reading_id):
    data = Reading.query.get_or_404(reading_id).to_dict()
    return jsonify(data)

@app.route('/api/sensors/<int:sensor_id>/readings', methods=['GET'])
def get_readings(sensor_id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 25, type=int), 100)
    sensor = Sensor.query.get_or_404(sensor_id)
    data = Sensor.to_collection_dict(sensor.readings, page, per_page,
        'get_readings', sensor_id=sensor_id)
    return jsonify(data)
