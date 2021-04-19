import mysql_opr.pool as pool
import config
import jwt


def register(username, password):
    conn, cursor = pool.create_conn()
    sql = "select * from user_account where username = %s"
    # 用户名已存在，已注册
    if cursor.execute(sql, username):
        conn.commit()
        pool.close_conn(conn, cursor)
        return False
    sql = "insert into user_account values(null, %s, %s)"
    cursor.execute(sql, (username, password))
    conn.commit()
    pool.close_conn(conn, cursor)
    return True


def login(username, password):
    conn, cursor = pool.create_conn()
    sql = "select * from user_account where username = %s"
    # 如果没有找到该用户名对应的用户信息
    if not cursor.execute(sql, username):
        conn.commit()
        pool.close_conn(conn, cursor)
        return 0
    password_db = cursor.fetchone()[2]
    conn.commit()
    pool.close_conn(conn, cursor)
    # 输入密码错误
    if password_db != password:
        return 1
    # 成功登陆
    return 2