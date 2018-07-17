from flask import request, jsonify
from flask_restful import Resource
from app import app, api, models

class Sensor(Resource):
    def get(self, sensor_id):
        data = models.Sensor.query.get_of_404(sensor_id).to_dict()
        return jsonify(data)

api.add_resource(Sensor, '/sensors/<int:sensor_id>')

class SensorList(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 25)
        data = models.Sensor.to_collection_dict(models.Sensor.query, page, per_page,
            'sensorlist')
        return jsonify(data)

api.add_resource(SensorList, '/sensors')