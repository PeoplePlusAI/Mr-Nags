import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def get_redis_value(key):
    return redis_client.get(key)

def set_redis(key, value, expire=None):
    redis_client.set(key, value, ex=expire)

def delete_redis(key):
    redis_client.delete(key)