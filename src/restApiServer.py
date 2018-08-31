from flask import Flask
from flask_cors import CORS

from rest_serving import rest_serving
from rest_session import rest_session

app = Flask(__name__)
app.register_blueprint(rest_session)
app.register_blueprint(rest_serving)

CORS(app)

if __name__ == '__main__':
    app.run(debug=True,
            host='0.0.0.0',
            threaded=True)
