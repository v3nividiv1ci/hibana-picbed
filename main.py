import os

import redis
from flask import Flask
from flask import request


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



    @app.route("/login")
    def login():
        if request.method == "GET":
            pass
