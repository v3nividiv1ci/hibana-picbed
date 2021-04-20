import time
import os
import mysql_opr.pool as pool
from flask import Flask
from flask import render_template
import base64


def pic_save(user_name, img, root):
    # 以时间戳命名，精确到0.001秒
    img_name = str(round(time.time() * 1000))
    img.save(os.path.join(root, img_name + ".jpg"))
    # f"{root}/{img_name}"
    conn, cursor = pool.create_conn()
    sql = "insert into pic_route values (NULL, %s, %s)"
    cursor.execute(sql, (user_name, img_name))
    conn.commit()
    pool.close_conn(conn, cursor)
    return img_name


def pic_get(username, img_name, root):
    conn, cursor = pool.create_conn()
    sql = "select * from pic_route where pic_id = %s"
    img_name = img_name.split(".", 1)[0]
    if not cursor.execute(sql, img_name):
        conn.commit()
        pool.close_conn(conn, cursor)
        return 10003
    _, user_db, img_db = cursor.fetchone()
    if user_db != username:
        conn.commit()
        pool.close_conn(conn, cursor)
        return 10004
    img_stream = ''
    # 以图片流的形式返回给前端
    with open(root + img_name + '.jpg', 'rb') as img_f:
        img_stream = img_f.read()
        # 到底用不用base64我还在考虑w
        # img_stream = base64.b64encode(img_stream)
    return img_stream



