from datetime import datetime as dt

import redis

import config

r = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB, password=config.REDIS_PASSWORD)


class User:
    """
    User base object
    """

    def __init__(self, user):
        """
        Create an user object
        :param user: Telegram's user object
        """
        self.id = user.id
        self.rhash = 'user:' + str(user.id)

        #Redis database
        if r.hget(self.rhash, 'id') != user.id:
            r.hset(self.rhash, 'id', user.id)
        if r.hget(self.rhash, 'username') != user.username:
            r.hset(self.rhash, 'username', user.username)
        r.hset(self.rhash, 'last_update', dt.now())
        if not self.state():
            r.hset(self.rhash, 'state', 'home')
        r.hset(self.rhash, "active", True)

    def state(self, new_state=None):
        """
        Get current user state or set a new user state
        :param new_state: new state for the user
        :return: state
        """
        if not new_state:
            return r.hget(self.rhash, 'state')

        r.hset(self.rhash, 'state', new_state)
        return True

    def setRedis(self, key, value):
        """
        Set a redis value
        :param key: redis key
        :param value: redis value
        :return: value
        """
        return r.hset(self.rhash, key, value)

    def getRedis(self, key):
        """
        Get a redis value
        :param key: redis key
        :return: value
        """
        return r.hget(self.rhash, key)

    def delRedis(self, key):
        """
        Delete a redis value
        :param key: redis key
        :return: None
        """
        return r.hdel(self.rhash, key)

    def increaseStat(self, stat):
        """
        Increase a stat value
        :param stat: which stat increase
        :return: redis response
        """
        response = r.hincrby(self.rhash, stat)
        return response

    def isActive(self):
        return bool(r.hget(self.rhash, "active")) or False
