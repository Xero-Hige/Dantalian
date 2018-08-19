from flask import Blueprint, jsonify, request

from handler_user import UserHandler
from rest_shared import API_ROUTE, error_response

rest_classify = Blueprint('rest_classify', __name__, template_folder='templates')
API_ROUTE += "classify"


@rest_classify.route(API_ROUTE, methods=['GET'])
def get_images():
    token = request.headers.get("api_key")
    origin = request.environ.get("HTTP_ORIGIN")

    if not token:
        return error_response(400, "Missing api-key")

    with UserHandler() as handler:
        if not handler.user_exists(origin):
            return error_response(404, "Unregistered")
        if not handler.is_valid_token(origin, token):
            return error_response(404, "Not registered or not valid key")

    response = {}

    response["tag"] = "people pooping"
    classified_images = ["101", "201", "403", "008"]
    unclassified_images = ["700", "005", "951", "213"]
    response["images"] = classified_images + unclassified_images

    return jsonify(response)


@rest_classify.route(API_ROUTE, methods=['POST'])
def classify_images():
    token = request.headers.get("api_key")
    origin = request.environ.get("HTTP_ORIGIN")

    if not token:
        return error_response(400, "Missing api-key")

    with UserHandler() as handler:
        if not handler.user_exists(origin):
            return error_response(404, "Unregistered")
        if not handler.is_valid_token(origin, token):
            return error_response(404, "Not registered or not valid key")

    images = request.json.get("images")
    tag = request.json.get("tag")

    if not images:
        return error_response(400, "Bad request")

    def valid_tags(tag, images):
        return True

    if valid_tags(tag, images):
        return jsonify({"Success": True})
    return jsonify({"Success": False})
