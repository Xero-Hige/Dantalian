from flask import Blueprint, jsonify, request, send_file

from model.model import *
from rest_shared import API_ROUTE, error_response

rest_videos = Blueprint('rest_videos', __name__, template_folder='templates')


@rest_videos.route(API_ROUTE + 'video/random', methods=['GET'])
def get_random_video():
	token = request.headers.get("api_key")
    origin = request.environ.get("HTTP_ORIGIN")

    if not token:
        return error_response(400, "Missing api-key")
    if not Users.exists(origin):
        return error_response(401, "Unregistered")
    if not Users.is_valid_token(origin, token):
        return error_response(401, "Key is not valid!")

    video = Video.random()

    return jsonify({
        'video_id': video.id,
        'video_category': video.category,
        'video_name': video.name
    })


@rest_videos.route(API_ROUTE + 'video/<int:video_id>', methods=['GET'])
def get_video(video_id):
	token = request.headers.get("api_key")
    origin = request.environ.get("HTTP_ORIGIN")

    if not token:
        return error_response(400, "Missing api-key")
    if not Users.exists(origin):
        return error_response(401, "Unregistered")
    if not Users.is_valid_token(origin, token):
        return error_response(401, "Key is not valid!")

    video = Video.get_or_none(video_id)
    if video is None:
        return error_response(401, "Video id is not valid")
    return send_file(video.filename)