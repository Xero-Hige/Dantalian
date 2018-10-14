from flask import Flask, request
from flask.json import jsonify
from flask_cors import CORS

# from rest_classify import rest_classify
# from rest_serving import rest_serving
from logger import print_info
from rest_session import rest_session
from rest_shared import API_ROUTE

# from rest_videos import rest_videos


app = Flask(__name__)
app.register_blueprint(rest_session)
# app.register_blueprint(rest_serving)
# app.register_blueprint(rest_videos)
# app.register_blueprint(rest_classify)

CORS(app)


@app.route(API_ROUTE + "status", methods=["GET"])
def status_code():
    return jsonify({"Status": "Ok"})


# FIXME: DO NOT PUSH THIS ON MASTER
@app.route(API_ROUTE + 'shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:  # pragma: no cover
        raise RuntimeError('Not running with the Werkzeug Server')  # pragma: no cover
    func()
    print_info(__name__, "Server Shutting down")
    return 'Server shutting down...'


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')

# FIXME: REMOVE
