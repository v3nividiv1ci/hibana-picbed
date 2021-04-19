import jwt
import config
import time


def generate_token(username, password):
    # 失效时间
    exp = int(time.time()) + 86400 * 114
    # JSON数据
    # 生成token
    payload = {"exp": exp, "username": username, "password": password, "admin": True}
    token = jwt.encode(payload, config.key)
    return token


def authentication(token):
    exp, username, password = jwt.decode(token, config.key, algorithms=['HS256'])['exp', 'username', 'password']
    pass
#     验证token是否合法：从数据库里面调取
#     验证token是否过期
