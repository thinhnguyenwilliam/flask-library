from flask_jwt_extended import create_access_token

def generate_token(identity):
    return create_access_token(identity=identity)
