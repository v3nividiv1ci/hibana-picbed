import jwt
import config
import time


def generate_token(username):
    # 失效时间
    exp = int(time.time()) + 3600 * 11.45
    # JSON数据
    # 生成token
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }
    payload = {"exp": exp, "username": username, "admin": True}
    token = jwt.encode(payload=payload, key=config.key, headers=headers, algorithm='HS256')
    return token


def validate_token(token):
    # jwt校验，通过则返回解码信息
    # jwt比token方便的地方：不需要/少查询数据库
    payload = None
    msg = None
    # jwt有效、合法性校验
    try:
        # True：进行校验
        payload = jwt.decode(token, config.key, algorithms=['HS256'], options={"verify_exp": True})
    except jwt.exceptions.ExpiredSignatureError:
        msg = "token expired"
    except jwt.DecodeError:
        msg = "token authentication failed"
    except jwt.InvalidTokenError:
        msg = "invalid token"
    return payload, msg




