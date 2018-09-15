from flask import Blueprint, send_file

from model.model import *
from rest_shared import API_ROUTE

rest_serving = Blueprint('rest_serving', __name__, template_folder='templates')


@rest_serving.route(API_ROUTE + "gif/<int:gif_id>", methods=['GET'])
def get_classified_image(gif_id):
    gif = Gif.get(gif_id)
    return send_file(gif.filename)
