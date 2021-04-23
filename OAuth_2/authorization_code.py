import jwt
import time
import random
import config
import mysql_opr.pool as pool


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


def generate_client_token(username, scope, exp):
    # 失效时间
    # JSON数据
    # 生成token
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }
    payload = {"exp": exp, "username": username, "scope": scope, "admin": True}
    token = jwt.encode(payload=payload, key=config.key, headers=headers, algorithm='HS256')
    return token


def insert_token(username, token):
    conn, cursor = pool.create_conn()
    sql = "insert into client_token values (NULL, %s, %s)"
    cursor.execute(sql, username, token)
    conn.commit()
    pool.close_conn(conn, cursor)