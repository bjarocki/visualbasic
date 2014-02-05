import redis

class Storage(object):
    def __init__(self):
        try:
            self.r = self.__initial_connection()

        except Exception as e:
            print(e)

    def __initial_connection(self):
        "Setup initial connection to redis backend"
        return redis.StrictRedis(host='127.0.0.1', port=6379, db=0)


    def push(self, name, value):
        "Push value to the list"
        try:
            if self.r.lpush(name, value):
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def get(self, name, limit=-1):
        "Get a list of elements stored at 'name'"
        try:
            return self.r.lrange(name, 0, limit)
        except:
            return []

    def get_keys(self):
        "Get a list of all keys"
        try:
            return self.r.keys('*')
        except:
            return []
