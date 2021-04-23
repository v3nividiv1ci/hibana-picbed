import jwt
import time


def generate_token(username):
    # 失效时间：十分钟
    exp = int(time.time()) + 600
    # JSON数据
    # 生成token
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }
    payload = {"exp": exp, "username": username, "admin": True}
    token = jwt.encode(payload=payload, key=config.key, headers=headers, algorithm='HS256')
    return token