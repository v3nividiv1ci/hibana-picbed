import io
import redis
from flask import Flask, send_file, redirect
from flask import request

import mysql_opr.create_tbl as create
import pic_bed.login.authentication as authentication
import pic_bed.login.login as log_in
import pic_bed.pic_load.pic_load as pic_load
import OAuth_2.redis_opr as redis_opr
import OAuth_2.authorization_code as authz_code

def create_app(test_config=None):
    # 创建app
    app = Flask(__name__)
    create.recreate_user_account()
    create.recreate_pic_route()
    root = "/Users/wangye/pyproject/hibana-picbed/pics/"
    # uri_1 = "跳转到的登陆界面"
    # uri_2 = "跳转到的授权界面"
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
    '''
    args:
    {
        response_type：# 表示授权类型，必选项，此处的值固定为"code"
        client_id：# 表示客户端的ID，必选项
        redirect_uri：
        {
            redirect_uri: http://127.0.0.1:5000/OAuth2/authenticate,
            redirect_uri_0: http://127.0.0.1:5000//OAuth2/authorize,
            redirect_uri_1: http://127.0.0.1:5000/OAuth2/login
        }
        # scope这里还没有
        # scope：# 表示申请的权限范围，可选项
        # {
        #     images:read,
        #     images:write
        # }
        state：# 表示客户端的当前状态，可以指定任意值，认证服务器会原封不动地返回这个值。
    }
    '''
    @app.route("/OAuth2/authenticate", methods=["GET"])
    def oauth_authenticate():
        if request.method == "GET":
            token = request.json.get("token")
            uri_0 = request.args.get("redirect_uri").get("redirect_uri_0")
            uri_1 = request.args.get("redirect_uri").get("redirect_uri_1")
            uri_a = request.args.get("redirect_uri").get("redirect_uri")
            # 如果有token
            if token:
                payload, msg = authentication.validate_token(token)
                # token没问题
                if not msg:
                    username = payload["username"]
                    uri = uri_0 + "?grant_type=authorization_code&user_name=%s" % username
                    return redirect(uri)
            # 没有token/token有问题
            else:
                uri = uri_1 + "?grant_type=authorization_code&redirect_uri=%s" % uri_a
                return redirect(uri)

    # uri_1对应登陆
    @app.route("/OAuth2/login", methods=["GET"])
    def oauth_login():
        if request.method == "GET":
            username = request.json.get("username")
            password = request.json.get("password")
            uri = request.args.get("redirect_uri")
            if log_in.login(username, password) == 10001:
                return dict(success=False, code="400", msg="user unregeisterd")
            elif log_in.login(username, password) == 10002:
                return dict(success=False, code="400", msg="wrong password")
            else:
                token = authentication.generate_token(username)
                # 孩子真的不知道怎么同时return redirect又return token了呜呜，那这里重定向就交给前端做叭（逃
                # 总之就是返回authenticate那个路由再来一遍
                return dict(succees=True, code="200", token=token, uri=uri)

    # uri_2对应的接口
    '''
    params:
    {
        # redirect时传过来的username
        username: 
        # 用户在授权界面填入的信息
        scope:{
            read: 0/1,
            write: 0/1,
            },
        exp_t: xxx,（前端提示最长三个月，前端进行换算成以秒为单位）
        redirect_uri: http://127.0.0.1:5000/client/code_token,
    }
    # https://api.typeform.com/oauth/authorize?
    # client_id={your_client_id}
    # &redirect_uri=https://results-example.herokuapp.com/callback
    # &scope={scope1}+{scope2}+{scope3}
    '''
    @app.route("/OAuth2/authorize", methods=["GET"])
    def authorize():
        if request.method == "GET":
            # token = request.json.get("token")
            # browse = request.json.get("browse")
            # download = request.json.get("download")
            # delete = request.json.get("delete")
            username = request.args.get("username")
            scope = request.args.get("scope")
            exp_t = request.args.get("exp_t")
            redirect_uri = request.args.get("redirect_uri")
            code = redis_opr.generate_save_code(pool, redirect_uri)
            uri = redirect_uri + '?grant_type=authorization_code&code=%s&redirect_uri=%s&user_name=%s&scope=%s&exp_t=%s'\
                  % (code, redirect_uri, username, scope, exp_t)
            return redirect(uri)
    '''
    params:
    {
        code: 
        redirect_uri: 
        user_name: 
        scope: 
        exp_t:
    }
    '''

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

    @app.route("/OAuth/token", methods=["GET"])
    def code_token():
        if request.method == "GET":
            code = request.args.get("code")
            redirect_uri = request.args.get("redirect_uri")
            username = request.args.get("user_name")
            scope = request.args.get("scope")
            exp_t = request.args.get("exp_t")
            if redis_opr.verify_code_uri(pool, code, redirect_uri):
                token = authz_code.generate_client_token(username, scope, exp_t)
                return dict(success=True, token=token, username=username)

    # 为第三方新建一个数据库/表，存入token
    @app.route("/client/token", methods=["POST"])
    def client_token():
        if request.method == "POST":
            # emmm这个token是包含在json里吧应该
            token = request.json.get("token")
            username = request.json.get("username")
            authz_code.insert_token(username, token)
            return dict(success=True, code="200")

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)