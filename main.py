import os

import redis
from flask import Flask
from flask import request
import pic_bed.login.login as log_in
import pic_bed.login.authentication as authentication


def create_app(test_config=None):
    # 创建app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)

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
            if log_in.login(username, password) == 0:
                return dict(success=False, code="4xx", msg="user unregeisterd")
            elif log_in.login(username, password) == 1:
                return dict(success=False, code="4xx", msg="wrong password")
            else:
                token = authentication.generate_token(username, password)
                return dict(succees=True, code="200", token="token")

    @app.route("/upload", methods=["POST"])
    def pic_upload():
        if request.method == "POST":
            token = request.args.get("token")
            payload, msg = authentication.validate_token(token)
            # 对token进行合法性校验
            if msg:
                return dict(success=False, code="500", msg=msg)
            username = payload["username"]

    @app.route("/download", methods=["GET"])
    def pic_upload():
        if request.method == "GET":
            token = request.args.get("token")
            payload, msg = authentication.validate_token(token)
            # 对token进行合法性校验
            if msg:
                return dict(success=False, code="500", msg=msg)
            username = payload["username"]

    @app.route("/delete", methods=["POST"])
    def pic_upload():
        if request.method == "POST":
            token = request.args.get("token")
            payload, msg = authentication.validate_token(token)
            # 对token进行合法性校验
            if msg:
                return dict(success=False, code="500", msg=msg)
            username = payload["username"]

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)