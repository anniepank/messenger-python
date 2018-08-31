import redis
import json

SESSION_PREFIX = 'session:'

class SessionStore:
    def __init__(self):
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)

    def set_session(self, key, value):
        value = json.dumps(value)
        self.redis.set(SESSION_PREFIX + key, value)
        self.redis.expire(SESSION_PREFIX + key, 3600 * 2)

    def get_session(self, key):
        session = self.redis.get(SESSION_PREFIX + key)
        if not session:
            session = {}
            self.set_session(key, session)
        else:
            session = json.loads(session)
        return session
