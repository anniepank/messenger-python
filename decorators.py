from functools import wraps
from flask import request, make_response
from session_store import SessionStore
import uuid
import time

SESSION_COOKIE = 'session'


def session_lifecycle(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        session_key = request.cookies.get(SESSION_COOKIE)

        if not session_key:
            session_key = str(uuid.uuid4())

        session_store = SessionStore()
        session = session_store.get_session(session_key)
        request.session = session

        response = f(*args, **kwargs)

        response.set_cookie(SESSION_COOKIE, session_key)
        session_store.set_session(session_key, session)

        print(session)

        return response
    return wrap


def logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username' in request.session:
            return f(*args, **kwargs)
        return make_response('', 403)
    return wrap
