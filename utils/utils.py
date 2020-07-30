import jwt

from flask import request, g, abort, current_app
from functools import wraps


def login_decorator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = request.headers.get('Authorization')
        if access_token is not None:
            try:
                payload = jwt.decode(access_token, current_app.config['JWT_SECRET_KEY'], 'HS256')
            except jwt.InvalidTokenError:
                 payload = None

            if payload is None:
                abort(401, description="INVALID_TOKEN")
            g.user_info = payload
        else:
            abort(401, description="INVALID_TOKEN")

        return f(*args, **kwargs)
    return decorated_function
