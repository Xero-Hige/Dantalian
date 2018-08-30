from flask import Blueprint, send_from_directory

from handler_user import UserHandler
from rest_shared import API_ROUTE, error_response

rest_serving = Blueprint('rest_session', __name__, template_folder='templates')


@rest_serving.route(API_ROUTE + "classified/<filename>", methods=['GET'])
def get_classified_image(filename):
	token = request.headers.get("api_key")
    origin = request.environ.get("HTTP_ORIGIN")

    if not token:
        return error_response(400, "Missing api-key")

    with UserHandler() as handler:
        if not handler.user_exists(origin):
            return error_response(404, "Unregistered")
        if not handler.is_valid_token(origin, token):
            return error_response(404, "Not registered or not valid key")

    return send_from_directory('/images/classified', filename + ".gif")


@rest_serving.route(API_ROUTE + "unclassified/<filename>", methods=['GET'])
def get_unclassified_image(filename):
	token = request.headers.get("api_key")
    origin = request.environ.get("HTTP_ORIGIN")

    if not token:
        return error_response(400, "Missing api-key")

    with UserHandler() as handler:
        if not handler.user_exists(origin):
            return error_response(404, "Unregistered")
        if not handler.is_valid_token(origin, token):
            return error_response(404, "Not registered or not valid key")

    return send_from_directory('/images/unclassified', filename + ".gif")
