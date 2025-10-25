from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..db.repositories.users import UserRepository
from ..db.models.users import User

blueprint = Blueprint(
    name='users',
    import_name=__name__,
    url_prefix='/api/users'
)


@blueprint.route('/register', methods=['POST'])
def create_user():
    data = request.form
    if data:
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        if username and password and email:
            if not UserRepository.validate_exists(username, email):
                return jsonify({
                    'success': False,
                    'message': 'user already exists'
                }), 401
            
            user = UserRepository.add(username, password, email)
            if user:
                return jsonify({
                    'success': True,
                    'data': data,
                    'message': 'successfully register // axenix <3',
                    'token': user.create_auth_token()
                }), 201
        
        return jsonify({
            'success': False,
            'message': 'error'
        }), 401
    

@blueprint.route('/login', methods=['POST'])
def login_user():
    data = request.form
    if data:
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user = UserRepository.get(User.username == username)
            if user and user.check_password(password):
                return jsonify({
                    'success': True,
                    'message': 'successfully login // axenix <3',
                    'token': user.create_auth_token()
                }), 200
        
        return jsonify({
            'success': False,
            'message': 'error'
        }), 401