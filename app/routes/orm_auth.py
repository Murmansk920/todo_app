from datetime import datetime, timezone, timedelta

import jwt
from flask import Blueprint, request, abort, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash

from app.orm_db import db
from app.models import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def user_register():
    username = request.json.get("username")
    password = request.json.get("password")
    if username is None or password is None:
        return {"error": "username 和 password 是必填项"}, 400

    user = User.query.filter_by(username=username).first()
    if user:
        abort(409)
    hashed = generate_password_hash(password)
    db.session.add(User(username=username, password=hashed))
    db.session.commit()
    return {"id": username, "message": "创建成功"}, 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json or {}
    username = data.get("username")
    password = str(data.get("password",''))
    if not username or not password:
        return jsonify({"error": "缺少用户名或密码", "code": 400}), 400

    user = User.query.filter_by(username=username).first()
    if user is None or not check_password_hash(user.password, password):
        return jsonify({"error": "用户名或密码错误", "code": 401}), 401

    token = jwt.encode(
        {"user_id": user.id,
         "exp": datetime.now(timezone.utc) + timedelta(hours=2)},
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )
    return jsonify({"token": token, "expires_in": 7200})