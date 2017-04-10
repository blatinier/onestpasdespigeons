from flask import Blueprint, jsonify, request


auth_bp = Blueprint('api/auth', __name__)


@auth_bp.route('/is_token_valid', methods=['POST'])
def token_valid():
    print('IS TOKEN VALID')
    return {}


@auth_bp.route('/create_user', methods=['POST'])
def create_user():
    email = request.form.get('email')
    password = request.form.get('password')
    password_confirm = request.form.get('password_confirm')
    if password == password_confirm:
        password_hash = User.hash_password(password)
        user = User(email=email, password=password_hash)
        user.save()
        return jsonify({'token': user.get_new_token()})
    return {}


@auth_bp.route('/get_token', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.log_in(email, password)
    return jsonify({'token': user.get_new_token()})
