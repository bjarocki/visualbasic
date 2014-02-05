import redis

class Storage(object):
    def __init__(self):
        try:
            self.redis_host = 'localhost'
            self.redis_port = 6379
            self.redis_db = 0
            self.redis_key_prefix = 'visualbasic::'
            self.redis_keys_list_name = '_keys_list_'

            self.r = self.__initial_connection()

        except Exception as e:
            print(e)

    def __initial_connection(self):
        "Setup initial connection to redis backend"
        return redis.StrictRedis(host=self.redis_host, port=self.redis_port, db=self.redis_db)

    def __register_key(self, key):
        "Add key to the list"
        try:
            self.r.sadd(self.__name_to_redis_key(self.redis_keys_list_name), key)
            return True
        except:
            return False

    def __name_to_redis_key(self, name):
        return self.redis_key_prefix + name

    def push(self, name, value):
        "Push value to the list"
        try:
            if self.__register_key(name) and self.r.lpush(self.__name_to_redis_key(name), value):
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def get(self, name, limit=-1):
        "Get a list of elements stored at 'name'"
        try:
            return self.r.lrange(self.__name_to_redis_key(name), 0, limit)
        except:
            return []

    def get_keys(self):
        "Get a list of all keys"
        try:
            return self.r.smembers(self.__name_to_redis_key(self.redis_keys_list_name))
        except:
            return []
