from flask import Blueprint, send_from_directory

from rest_shared import API_ROUTE

rest_serving = Blueprint('rest_serving', __name__, template_folder='templates')


@rest_serving.route(API_ROUTE + "classified/<int:filename>", methods=['GET'])
def get_classified_image(filename):
    return send_from_directory('/images/classified', str(filename) + ".gif")


@rest_serving.route(API_ROUTE + "unclassified/<int:filename>", methods=['GET'])
def get_unclassified_image(filename):
    return send_from_directory('/images/unclassified', str(filename) + ".gif")
