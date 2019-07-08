from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def error_response(status_code, message=None):
    data = {"error": HTTP_STATUS_CODES.get(status_code, "Unknown error")}
    if message:
        data["message"] = message
    response = jsonify(data)
    response.status_code = status_code
    return response


def bad_request(message=None):
    return error_response(400, message)


def unauthorized(message=None):
    return error_response(401, message)


def not_found(message=None):
    return error_response(404, message)
