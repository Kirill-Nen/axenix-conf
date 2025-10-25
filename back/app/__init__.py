from flask import Flask, Response
from flask.json import provider
from flask_jwt_extended import JWTManager
import os

from .db.session import init_models
from .api.users import blueprint as api_users

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(32)
app.config["JWT_SECRET_KEY"] = os.urandom(32)
app.config['JSON_SORT_KEYS'] = False

jwt = JWTManager(app)

app.register_blueprint(api_users)

provider.DefaultJSONProvider.sort_keys = False
provider.DefaultJSONProvider.ensure_ascii = False

#обход cors
@app.after_request
def after_request(response: Response) -> Response:
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response