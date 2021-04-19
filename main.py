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
                return dict(success=True, message="200")
            else:
                return dict(success=False, message="username used", error_code=1)

    @app.route("/login")
    def login():
        if request.method == "GET":
            username = request.json.get("username")
            password = request.json.get("password")
            if log_in.login(username, password) == 0:
                return dict(success=False, message="user unregeisterd", error_code=2)
            elif log_in.login(username, password) == 1:
                return dict(success=False, message="wrong password", error_code=3)
            else:
                token = authentication.generate_token(username, password)
                return dict(succees=True, message="200", token="token")
