from flask import request, jsonify, url_for
from app import db
from app.api import bp
from app.api.errors import bad_request
from app.models import Sensor, User

@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'name' not in data:
        return bad_request('must include name field')
    if 'password' not in data:
        return bad_request('must include password field')
    if 'sensors' not in data:
        return bad_request('must include sensors field')
    if not Sensor.are_valid_sensors(data['sensors']):
        return bad_request('invalid sensor(s) in included sensors')
    if User.query.filter_by(name=data['name']).first():
        return bad_request('please use a different name')
    user = User()
    user.from_dict(data)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', user_id=user.id)
    return response

@bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    data = User.query.get_or_404(user_id).to_dict()
    return jsonify(data)

@bp.route('/users', methods=['GET'])
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 25)
    data = User.to_collection_dict(User.query, page, per_page,
        'api.get_users')
    return jsonify(data)

@bp.route('/users/<int:user_id>/sensors', methods=['GET'])
def get_user_sensors(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        'items': [sensor.to_dict() for sensor in user.sensors],
        '_meta': {
            'total_items': len(user.sensors)
        }
    })

@bp.route('/users/<int:user_id>/sensors/add', methods=['PATCH'])
def add_user_sensors(user_id):
    data = request.get_json() or {}
    if 'sensors' not in data:
        return bad_request('must include sensors field')
    if not Sensor.are_valid_sensors(data['sensors']):
        return bad_request('invalid sensor(s) in included sensors')
    user = User.query.get_or_404(user_id)
    user.add_sensors(data['sensors'])
    db.session.add(user)
    db.session.commit()
    response = jsonify()
    response.status_code = 204
    response.headers['Location'] = url_for('api.get_user_sensors', user_id=user.id)
    return response

@bp.route('/users/<int:user_id>/sensors/remove', methods=['PATCH'])
def remove_user_sensors(user_id):
    data = request.get_json() or {}
    if 'sensors' not in data:
        return bad_request('must include sensors field')
    if not Sensor.are_valid_sensors(data['sensors']):
        return bad_request('invalid sensor(s) in included sensors')
    user = User.query.get_or_404(user_id)
    user.remove_sensors(data['sensors'])
    db.session.add(user)
    db.session.commit()
    response = jsonify()
    response.status_code = 204
    response.headers['Location'] = url_for('api.get_user_sensors', user_id=user.id)
    return response
