from flask import jsonify

API_ROUTE = "/api/0.1/"


# Errors

def error_response(code, message):
    response = jsonify({'error': message})
    response.status_code = code
    return response
