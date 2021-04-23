import time
import os
import mysql_opr.pool as pool
from flask import Flask
from flask import render_template
import base64
from threading import Thread


def delete_file(img_name, root):
    os.remove(os.path.join(root, img_name + ".jpg"))


def delete_path(img_name):
    conn, cursor = pool.create_conn()
    sql = "delete from pic_route where pic_id = %s"
    if cursor.execute(sql, str(img_name)):
        print("yes")
    else:
        print("no")
    conn.commit()
    pool.close_conn(conn, cursor)


class Delete:
    pass


def save_pic(user_name, img, root):
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


def rd_pic(username, img_name, root, r):
    conn, cursor = pool.create_conn()
    sql = "select * from pic_route where pic_id = %s"
    img_name = img_name.split(".", 1)[0]
    print(type(img_name))
    conn.commit()
    if not cursor.execute(sql, img_name):
        pool.close_conn(conn, cursor)
        return 10003
    _, user_db, img_db = cursor.fetchone()
    if user_db != username:
        pool.close_conn(conn, cursor)
        return 10004
    if r:
        img_stream = ''
        # 以图片流的形式返回给前端
        with open(root + img_name + '.jpg', 'rb') as img_f:
            img_stream = img_f.read()
            # 到底用不用base64我还在考虑w
            # img_stream = base64.b64encode(img_stream)
        return img_stream
    else:

        t1 = Thread(target=delete_file, args=(str(img_name), root))
        t2 = Thread(target=delete_path, args=(str(img_name),))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        return 0



