import os

from threading import Thread
from flask import request, g
from functools import wraps

from flask_backend.cache.redis_connector import RedisStore
from flask_backend.cache.cache_constants import REQUEST_LIMIT_KEY

_redis_store = RedisStore()


def asynchronous(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


def validate_file(allowed_extensions=None):
    """
    **User Example 1**

        @validate_file()
        def upload_user_photo(user_id):
            pass

        1. Makes sure 'files' is part of the request

    **User Example 2**

        @validate_file(allowed_extensions=['.png', '.jpg'])
        def upload_user_photo(user_id):
            pass

        1. Makes sure 'files' is part of the request
        2. Makes sure the file extension is allowed

    :param allowed_extensions:
    :return:
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'file' not in request.files:
                raise Exception(u'Missing file part in the request. '
                                u'Tip: Try including "-F file=@image.png".')

            file = request.files['file']

            if file.filename == '':
                raise Exception(u'No file selected.')

            # check to see if the file extension is allowed
            if allowed_extensions:
                file_ext = os.path.splitext(file.filename)[1]
                if file_ext not in allowed_extensions:
                    raise Exception(u'Only files with {0} exts are allowed.'
                                    .format(allowed_extensions))

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def limit(requests=100, window=60, by="ip", group=None):
    """
    **User Example**

        @limit(requests=100, window=60, by="ip", group=None)
        def authenticate_user():
            pass

        1. Makes sure that only 100 requests are allowed in 60 secs
           for authenticate_user() endpoint by the same ip address

    :param requests: max number of requests allowed
    :param window: duration in secs for the max allowed requests
    :param by: request originator
    :param group: request endpoint
    :return:
    """

    if not callable(by):
        by = {'ip': lambda: request.remote_addr}[by]

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            local_group = group or request.endpoint
            key = REQUEST_LIMIT_KEY.format(endpoint=local_group, ip=by())

            try:
                remaining = requests - int(_redis_store.get(key))
            except (ValueError, TypeError):
                remaining = requests
                _redis_store.set(key, 0, timeout_in_sec=None)

            ttl = _redis_store.ttl(key)
            if not ttl:
                _redis_store.expire(key, window)

            if remaining > 0:
                _redis_store.incr(key, 1)
            else:
                raise Exception(u'Too many requests.')

            return f(*args, **kwargs)
        return decorated_function
    return decorator
