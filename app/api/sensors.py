from flask import request, jsonify
from app import app, models

@app.route('/api/sensors/<int:sensor_id>', methods=['GET'])
def get_sensor(sensor_id):
    data = models.Sensor.query.get_or_404(sensor_id).to_dict()
    return jsonify(data)

@app.route('/api/sensors', methods=['GET'])
def get_sensors():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 25)
    data = models.Sensor.to_collection_dict(models.Sensor.query, page, per_page,
        'get_sensors')
    return jsonify(data)