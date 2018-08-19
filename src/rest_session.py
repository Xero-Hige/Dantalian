from flask import Blueprint, jsonify, request

from handler_user import UserHandler
from rest_shared import API_ROUTE, error_response

rest_session = Blueprint('rest_session', __name__, template_folder='templates')


@rest_session.route(API_ROUTE + 'users', methods=['POST'])
def create_user_post():
    if not request.json or 'username' not in request.json:
        return error_response(400, "Missing username")

    new_user = request.json['username']

    with UserHandler() as handler:
        api_key = handler.add_user(new_user)
        if api_key:
            return jsonify({
                'status': "Created",
                'api_key': api_key
            })
        else:
            return error_response(400, "Already in use")

    return error_response(500, "Internal server error.")


@rest_session.route(API_ROUTE + 'users', methods=['DELETE'])
def delete_user_post():
    if not request.json or 'username' not in request.json:
        return error_response(400, "Missing username")

    del_user = request.json['username']

    with UserHandler() as handler:
        handler.delete_user(del_user)

    return jsonify({'status': "Deleted"})
