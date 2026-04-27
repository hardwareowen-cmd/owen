from functools import wraps
from flask import abort
from flask_login import current_user


#allows for specific pages to be locked behind a user requiring a role
def role_required(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.role not in roles:
                return abort(403)

            return func(*args, **kwargs)
        return wrapper
    return decorator