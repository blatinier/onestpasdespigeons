from flask import Blueprint


auth_bp = Blueprint('api/auth', __name__)

@auth_bp.route('/is_token_valid', methods=['POST'])
def token_valid():
    print('IS TOKEN VALID')
    return {}
