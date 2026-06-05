from flask_jwt_extended import create_access_token, get_jwt_identity
from flask import g

def refresh_jwt_token():
    identity = get_jwt_identity()
    if identity:
        new_token = create_access_token(identity=identity)
        g.new_access_token = new_token