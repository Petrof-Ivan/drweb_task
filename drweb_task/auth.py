# auth.py
from flask import request, Response
from functools import wraps
from models import User

def check(auth):
    user = User.query.filter_by(username=auth.username).first()
    if user and user.password == auth.password:
        return True

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        authorization_header = request.headers.get('Authorization')
        if authorization_header and check(auth):
            return f(*args, **kwargs)
        else:
            resp = Response("Need authorization")
            resp.headers['WWW-Authenticate'] = 'Basic'
            return resp, 401
    return decorated