import redis
import random


# 生成并保存authz_code
def generate_save_code(pool, uri):
    code = random.randint(1, 1000)
    r = redis.Redis(connection_pool=pool)
    r.set(uri, code, ex=600)
    return code


def verify_code_uri(pool, code, uri):
    r = redis.Redis(connection_pool=pool)
    if r.get(uri) == code:
        return True
    return False
