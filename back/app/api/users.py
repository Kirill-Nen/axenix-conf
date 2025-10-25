from flask import Blueprint, request, jsonify
from flask_cors import CORS

from ..db.repositories.users import UserRepository
from ..db.models.users import User

from ..auth import decode_access_token

blueprint = Blueprint(
    name='users',
    import_name=__name__,
    url_prefix='/api/users'
)


@blueprint.route('/register', methods=['POST', 'OPTIONS'])
def create_user():
    data = request.get_json()
    if data and 'username' in data and 'password' in data and 'email' in data:
        username, password, email = data['username'], data['password'], data['email']
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
    

@blueprint.route('/login', methods=['POST', 'OPTIONS'])
def login_user():
    data = request.get_json()
    if data:
        username, password = data['username'], data['password']
        user = UserRepository.get(User.username == username)
        if user and user.check_password(password):
            return jsonify({
                'success': True,
                'message': 'successfully login // axenix <3',
                'token': user.create_auth_token()
            }), 200
        
    return jsonify({
        'success': False,
        'message': 'invalid login data'
    })
    

@blueprint.route('/validate_token', methods=['POST', 'OPTIONS'])
def validate_token():
    data = request.get_json()
    if data:
        token = data['auth_token']
        decoded_data = decode_access_token(token)
        if decoded_data and 'id' in decoded_data:
            user = UserRepository.get(User.id == decoded_data['id'])
            if user:
                return jsonify({
                    'success': True,
                    'data': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email
                    }
                })
    return jsonify({
        'success': False,
        'message': 'validate error'
    }), 401