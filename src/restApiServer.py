from flask import Flask
from flask_cors import CORS

from rest_serving import rest_serving
from rest_session import rest_session
from rest_videos import rest_videos
from rest_classify import rest_classify


app = Flask(__name__)
app.register_blueprint(rest_session)
app.register_blueprint(rest_serving)
app.register_blueprint(rest_videos)
app.register_blueprint(rest_classify)


CORS(app)


@app.route("/status", methods=["GET"])
def status_code():
    return "Ok"


if __name__ == '__main__':
    app.run(debug=True,
            host='0.0.0.0',
            port=8000,
            threaded=True)
