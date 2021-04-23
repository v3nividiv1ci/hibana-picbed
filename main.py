import io

from flask import Flask, send_file, redirect
from flask import request

import mysql_opr.create_tbl as create
import pic_bed.login.authentication as authentication
import pic_bed.login.login as log_in
import pic_bed.pic_load.pic_load as pic_load


def create_app(test_config=None):
    # 创建app
    app = Flask(__name__)
    create.recreate_user_account()
    create.recreate_pic_route()
    root = "/Users/wangye/pyproject/hibana-picbed/pics/"
    # uri_1 = "跳转到的登陆界面"
    # uri_2 = "跳转到的授权界面"

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
            img_name = pic_load.save_pic(username, img, root) + ".jpg"
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
            img_stream = pic_load.rd_pic(username, img_name, root, True)
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

    @app.route("/delete", methods=["DELETE"])
    def pic_delete():
        if request.method == "DELETE":
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
            img_stream = pic_load.rd_pic(username, img_name, root, False)
            if img_stream == 10003:
                return dict(success=False, code="500", msg="pic not found")
            elif img_stream == 10004:
                return dict(success=False, code="500", msg="username unmatch")
            else:
                return dict(success=True, code="200", msg="pic deleted")

# ------------------------以下是OAuth2.0相关部分-------------------------- #

    # 判断用户是否已经登陆，如果没登陆跳转到uri_1即登陆界面，如果已经登陆了跳转到uri_2即授权界面
    # 如果登陆了是否
    '''
    args:
    {
        "redirect_uri_0": " http://127.0.0.1:5000//OAuth2/authorize",
        "redirect_uri_1": " http://127.0.0.1:5000/OAuth2/login"
    }
    '''
    @app.route("/OAuth2/authenticate", methods=["GET"])
    def log():
        if request.method == "GET":
            token = request.json.get("token")
            uri_0 = request.args.get("redirect_uri_0")
            uri_1 = request.args.get("redirect_uri_1")
            # 这个地方，如何判断用户是否登陆，问题很大
            # 我觉得还可以，因为这个token和最后的token包含的字段区别很大
            if not token:
                return redirect(uri_1)
            _, msg = authentication.validate_token(token)
            if msg:
                return redirect(uri_1)
            else:
                uri = uri_0 + "?="
                return redirect(uri_0)

    # uri_1对应的接口，返回
    @app.route("/OAuth2/login", methods=["GET"])
    def login():
        if request.method == "GET":
            username = request.json.get("username")
            password = request.json.get("password")
            if log_in.login(username, password) == 10001:
                return dict(success=False, code="400", msg="user unregeisterd")
            elif log_in.login(username, password) == 10002:
                return dict(success=False, code="400", msg="wrong password")
            else:
                # 之后把验证机制改成cookie/session
                token = authentication.generate_token(username)
                return dict(succees=True, code="200", token=token, redirect_uri=uri_0)

    # uri_2对应的接口
    '''
    params: 
    {   
        "token": xxx.xxx.xxx,
        "browse": 0/1,
        "download": 0/1,
        "delete": 0/1
        "exp_t": xxx（前端提示最长三个月，前端进行换算成以秒为单位）
    }
    
    '''
    @app.route("/OAuth2/authorize", methods=["GET"])
    def authorize():
        if request.method == "GET":
            token = request.json.get("token")
            browse = request.json.get("browse")
            download = request.json.get("download")
            delete = request.json.get("delete")

    @app.route("/token", methods=["GET"])
    def code_token():
        if request.method == "GET":
            pass
            return dict(success=True, token=token)



    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)