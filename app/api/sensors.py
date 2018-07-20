from flask import request, jsonify, url_for
from app import app, db
from app.api.errors import bad_request
from app.models import Sensor

@app.route('/api/sensors', methods=['POST'])
def create_sensor():
    data = request.get_json() or {}
    if 'name' not in data:
        return bad_request('must include name field')
    if 'categories' not in data:
        return bad_request('must include categories field')
    if Sensor.query.filter_by(name=data['name']).first():
        return bad_request('please use a different name')
    sensor = Sensor()
    sensor.from_dict(data)
    db.session.add(sensor)
    db.session.commit()
    response = jsonify(sensor.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('get_sensor', sensor_id=sensor.id)
    return response

@app.route('/api/sensors/<int:sensor_id>', methods=['GET'])
def get_sensor(sensor_id):
    data = Sensor.query.get_or_404(sensor_id).to_dict()
    return jsonify(data)

@app.route('/api/sensors', methods=['GET'])
def get_sensors():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 25)
    data = Sensor.to_collection_dict(Sensor.query, page, per_page,
        'get_sensors')
    return jsonify(data)