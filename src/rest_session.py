from flask import Blueprint, jsonify, request

from model.model import *
from rest_shared import API_ROUTE, error_response

rest_session = Blueprint('rest_session', __name__, template_folder='templates')


@rest_session.route(API_ROUTE + 'users', methods=['POST'])
def create_user_post():
    """
    Endpoint to create a new user

    Receives:
    - username: intended username

    Returns:
    - response with api_key value
    """
    if not request.json or 'username' not in request.json:
        return error_response(400, "Missing username")

    new_user = request.get_json()['username']

    api_key = Users.create(new_user)
    if not api_key:
        return error_response(400, "Already in use")
    return jsonify({
        'status': "Created",
        'api_key': api_key
    })


@rest_session.route(API_ROUTE + 'users', methods=['DELETE'])
def delete_user_post():
    """
    Endpoint to delete existing users

    Receives:
    - username: username to be deleted

    Returns:
    - response with status
    """
    if not request.json or 'username' not in request.json:
        return error_response(400, "Missing username")

    del_user = request.json['username']
    Users.delete_user(del_user)

    return jsonify({'status': "Deleted"})


@rest_session.route(API_ROUTE + 'users/trust', methods=['POST'])
def trust_user_post():
    """
    Endpoint to acknowledge a user as trusted

    Receives:
    - username: username to acknowledge as trusted
    - api_key: the user's api_key
    - secret_phrase: secret phrase issued by the system's admin

    Returns:
    - response with result value
    """
    if not request.json or 'username' not in request.json:
        return error_response(400, "Missing username")

    if 'secret_phrase' not in request.json:
        return error_response(400, 'Missing secret phrase')

    if 'api_key' not in request.json:
        return error_response(400, 'Missing api_key')

    result = Users.acknowledge_trusted(request.json["username"],
                                       request.json["api_key"],
                                       request.json["secret_phrase"])

    return jsonify({'result': result})
