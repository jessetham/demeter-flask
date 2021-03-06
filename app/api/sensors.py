from flask import request, jsonify, url_for
from app import db
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request
from app.models import Sensor, Category


@bp.route("/sensors", methods=["POST"])
@token_auth.login_required
def create_sensor():
    data = request.get_json() or {}
    if "name" not in data:
        return bad_request("must include name field")
    if "categories" not in data:
        return bad_request("must include categories field")
    if not Category.are_valid_categories(data["categories"]):
        return bad_request("invalid categor(y)/(ies) in included categories")
    if Sensor.query.filter_by(name=data["name"]).first():
        return bad_request("please use a different name")
    sensor = Sensor()
    sensor.from_dict(data)
    db.session.add(sensor)
    db.session.commit()
    response = jsonify(sensor.to_dict())
    response.status_code = 201
    response.headers["Location"] = url_for("api.get_sensor", sensor_id=sensor.id)
    return response


@bp.route("/sensors/<int:sensor_id>", methods=["GET"])
@token_auth.login_required
def get_sensor(sensor_id):
    data = Sensor.query.get_or_404(sensor_id).to_dict()
    return jsonify(data)


@bp.route("/sensors", methods=["GET"])
@token_auth.login_required
def get_sensors():
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 10, type=int), 25)
    data = Sensor.to_collection_dict(Sensor.query, page, per_page, "api.get_sensors")
    return jsonify(data)


@bp.route("/sensors/<int:sensor_id>/categories", methods=["GET"])
@token_auth.login_required
def get_sensor_categories(sensor_id):
    sensor = Sensor.query.get_or_404(sensor_id)
    return jsonify(
        {
            "items": [category.to_dict() for category in sensor.categories],
            "_meta": {"total_items": len(sensor.categories)},
        }
    )


@bp.route("/sensors/<int:sensor_id>/categories/add", methods=["PATCH"])
@token_auth.login_required
def add_sensor_categories(sensor_id):
    data = request.get_json() or {}
    if "categories" not in data:
        return bad_request("must include categories field")
    if not Category.are_valid_categories(data["categories"]):
        return bad_request("invalid categor(y)/(ies) in included categories")
    sensor = Sensor.query.get_or_404(sensor_id)
    sensor.add_categories(data["categories"])
    db.session.add(sensor)
    db.session.commit()
    response = jsonify()
    response.status_code = 204
    response.headers["Location"] = url_for(
        "api.get_sensor_categories", sensor_id=sensor.id
    )
    return response


@bp.route("/sensors/<int:sensor_id>/categories/remove", methods=["PATCH"])
@token_auth.login_required
def remove_sensor_categories(sensor_id):
    data = request.get_json() or {}
    if "categories" not in data:
        return bad_request("must include categories field")
    if not Category.are_valid_categories(data["categories"]):
        return bad_request("invalid categor(y)/(ies) in included categories")
    sensor = Sensor.query.get_or_404(sensor_id)
    sensor.remove_categories(data["categories"])
    db.session.add(sensor)
    db.session.commit()
    response = jsonify()
    response.status_code = 204
    response.headers["Location"] = url_for(
        "api.get_sensor_categories", sensor_id=sensor.id
    )
    return response
