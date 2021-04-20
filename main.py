import io
import os
import time
from flask import Flask, send_file
from flask import request
import pic_bed.login.login as log_in
import pic_bed.login.authentication as authentication
import mysql_opr.create_tbl as create
import pic_bed.pic_load.pic_load as pic_load


def create_app(test_config=None):
    # 创建app
    app = Flask(__name__)
    create.recreate_user_account()
    create.recreate_pic_route()
    root = "/Users/wangye/pyproject/hibana-picbed/pics/"

    @app.route("/register", methods=["POST"])
    def register():
        if request.method == "POST":
            username = request.json.get("username")
            password = request.json.get("password")
            if log_in.register(username, password):
                return dict(success=True, code="200")
            else:
                return dict(success=False, msg="username used")

    @app.route("/login", methods=["GET"])
    def login():
        if request.method == "GET":
            username = request.json.get("username")
            password = request.json.get("password")
            if log_in.login(username, password) == 10001:
                return dict(success=False, code="400", msg="user unregeisterd")
            elif log_in.login(username, password) == 10002:
                return dict(success=False, code="400", msg="wrong password")
            else:
                token = authentication.generate_token(username)
                return dict(succees=True, code="200", token=token)

    @app.route("/upload", methods=["POST"])
    def pic_upload():
        if request.method == "POST":
            token = request.form.get("token")
            payload, msg = authentication.validate_token(token)
            # 对token进行合法性校验
            if msg:
                return dict(success=False, code="500", msg=msg)
            username = payload["username"]
            img = request.files.get("img")
            img_name = pic_load.pic_save(username, img, root) + ".jpg"
            if img_name:
                return dict(success=True, code="200", pname=img_name)

    @app.route("/download", methods=["GET"])
    def pic_download():
        if request.method == "GET":
            token = request.json.get("token")
            payload, msg = authentication.validate_token(token)
            # 对token进行合法性校验
            if msg:
                return dict(success=False, code="500", msg=msg)
            username = payload["username"]
            '''
            img_name : 11451141919810.jpg
            '''
            img_name = request.args.get("img_name")
            img_stream = pic_load.pic_get(username, img_name, root)
            if img_stream == 10003:
                return dict(success=False, code="500", msg="pic not found")
            elif img_stream == 10004:
                return dict(success=False, code="500", msg="username unmatch")
            else:
                return send_file(
                    io.BytesIO(img_stream),
                    mimetype='image/jpeg',
                    as_attachment=True,
                    attachment_filename='%s' % img_name)

    @app.route("/delete", methods=["POST"])
    def pic_delete():
        if request.method == "POST":
            token = request.json.get("token")
            payload, msg = authentication.validate_token(token)
            # 对token进行合法性校验
            if msg:
                return dict(success=False, code="500", msg=msg)
            username = payload["username"]
            pass

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)