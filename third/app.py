from flask import *

import redis
import mysql_opr
app = Flask(__name__)
pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)


# 为第三方新建一个数据库/表，存入token
@app.route("/client/token", methods=["POST"])
def client_token():
    if request.method == "POST":
        # emmm这个token是包含在json里吧应该
        token = request.json.get("token")
        username = request.json.get("username")
        mysql_opr.insert_token(username, token)
        return dict(success=True, code="200")

# 第三方平台的路由
    # 由图床重定向 -> 第三方，带有code，要发往图床
    # 好像这个地方携带的redirect_uri应该是这个路由自己，因为之前往redis里面存的就是这个路由
    # 我觉得第三方平台应该是默认知道图床的uri的，所以直接用？
    @app.route("/client/code_token", methods=["GET"])
    def code_token():
        if request.method == "GET":
            code = request.args.get("code")
            redirect_uri = request.args.get("redirect_uri")
            username = request.args.get("user_name")
            scope = request.args.get("scope")
            exp_t = request.args.get("exp_t")
            uri = 'http://127.0.0.1:5000/OAuth/token?grant_type=authorization_code&code=%s&redirect_uri=%s&user_name=%s&scope=%s&exp_t=%s'\
                  % (code, redirect_uri, username, scope, exp_t)
            return redirect(uri)


if __name__ == '__main__':
    app.run()
