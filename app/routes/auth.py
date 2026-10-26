import jwt
from datetime import datetime, timedelta, timezone
from flask import Blueprint, request, jsonify, current_app,abort
from werkzeug.security import check_password_hash, generate_password_hash

from app.service.todos import find_user, add_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def user_register():
    username = request.json.get("username")
    password = request.json.get("password")
    if username is None or password is None:
        return {"error": "username 和 password 是必填项"}, 400
    if len(find_user(username)) == 0:
        hashed = generate_password_hash(password)
        add_user(username, hashed)
        return {"id": username, "message": "创建成功"}, 201
    abort(409)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json or {}
    username = data.get("username")
    password = str(data.get("password",''))
    if not username or not password:
        return jsonify({"error": "缺少用户名或密码", "code": 400}), 400

    user = find_user(username)
    if len(user) == 0 or not check_password_hash(user[0]["password"], password):
        return jsonify({"error": "用户名或密码错误", "code": 401}), 401

    token = jwt.encode(
        {"user_id": str(user[0]["id"]),
         "exp": datetime.now(timezone.utc) + timedelta(hours=2)},
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )
    return jsonify({"token": token, "expires_in": 7200})