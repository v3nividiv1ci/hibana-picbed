import redis


def insert_token(pool, username, token):
    r = redis.Redis(connection_pool=pool)
    r.set(username, token, ex=24*3600)
