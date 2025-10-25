from flask import Flask, request, jsonify
from flask.json import provider
from flask_cors import CORS
import os

from .db.session import init_models
from .api.users import blueprint as api_users

app = Flask(__name__)

# Разрешаем запросы с фронта
CORS(app, origins=["http://localhost:8000"], supports_credentials=True, methods=['POST', 'OPTIONS'])

app.config['SECRET_KEY'] = os.urandom(32)
app.config['JSON_SORT_KEYS'] = False

app.register_blueprint(api_users)

provider.DefaultJSONProvider.sort_keys = False
provider.DefaultJSONProvider.ensure_ascii = False

@app.before_request
def before_request():
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        headers = response.headers

        headers['Access-Control-Allow-Origin'] = 'http://localhost:8000'
        headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        headers['Access-Control-Allow-Credentials'] = 'true'

        return response

@app.route('/')
def index():
    return jsonify({'ok': 'ok'})