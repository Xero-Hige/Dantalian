from flask import Blueprint, jsonify, request

from model.model import *
from rest_shared import API_ROUTE, error_response
from sqlalchemy.sql.expression import func
from random import choice


MIN_TAGS = 5
MIN_TRESHOLD = 0.7

rest_classify = Blueprint('rest_classify', __name__, template_folder='templates')


@rest_classify.route(API_ROUTE + 'classify', methods=['GET'])
def get_images():
    token = request.headers.get("api_key")
    origin = request.environ.get("HTTP_ORIGIN")

    if not token:
        return error_response(400, "Missing api-key")

    if not Users.exists(origin):
        return error_response(401, "Unregistered")
    if not Users.is_valid_token(origin, token):
        return error_response(401, "Key is not valid!")

    response = {}

    classified = Gif.query.filter(Gif.has(classified=True)).order_by(func.rand()).limit(2)
    unclassified = Gif.query.filter(Gif.has(classified=False)).order_by(func.rand()).limit(2)

    text = choice(classified)
    text = Tag.query.filter(Tag.gif.has(id=text.id)).first()
    text = text.tagtext.text

    response["images"] = [gif.id for gif in classified] + [gif.id for gif in unclassified]
    response["text"] = text

    return jsonify(response)


@rest_classify.route(API_ROUTE + 'classify', methods=['POST'])
def classify_images():
    token = request.headers.get("api_key")
    origin = request.environ.get("HTTP_ORIGIN")

    if not token:
        return error_response(400, "Missing api-key")

    if not Users.exists(origin):
        return error_response(401, "Unregistered")
    if not Users.is_valid_token(origin, token):
        return error_response(401, "Key is not valid!")

    images = request.json.get("images")
    text = request.json.get("text")
    tags = request.json.get("tags")

    if not images:
        return error_response(400, "Bad request")

    def max_tag(tags):
        _d = {}
        for tag in tags:
            if tag not in _d:
                _d[tag] = 0
            _d[tag] += 1
        v = sorted([(v, k) for k, v in _d.items()])[-1]
        return v[1], v[0]

    def valid_tags(tags, text, images):
        tagtext = TagText.query.filter(TagText.text == text).one()
        for image, tag in zip(images, tags):
            gif = Gif.query.get(image)
            if gif.classified:
                if gif.classification != tag:
                    return False
        return True

    def update_classification(text, images, tags, user_id):
        tagtext = TagText.query.filter(TagText.text == text).one()
        for image, tag in zip(images, tags):
            gif = Gif.query.get(image)
            if not gif.classified:
                Tag.create(tagtext.id, gif.id, user_id, tag)
            if len(gif.tags) >= MIN_TAGS:
                max_tag, score = max_tag(gif.tags)
                if score >= MIN_TRESHOLD:
                    gif.mark_tagged(max_tag)

    user = Users.query.filter(Users.username == origin).one()
    if valid_tags(tags, text, images):
        update_classification(text, images, tags, user.id)
        return jsonify({"Success": True})
    return jsonify({"Success": False})
