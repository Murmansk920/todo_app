from flask import current_app
from flask import request, jsonify, g
from jwt import decode,ExpiredSignatureError, InvalidTokenError

def verify_token(token):
    """验证 Token，成功返回 payload 字典，失败返回 (错误信息, 状态码)"""
    try:
        payload = decode(
            token,
            current_app.config["SECRET_KEY"],
            algorithms=["HS256"]
        )
        return payload
    except ExpiredSignatureError:
        return {"error": "Token 已过期", "code": 401}, 401
    except InvalidTokenError:
        return {"error": "Token 无效", "code": 401}, 401

def auth_required():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "缺少认证信息", "code": 401}), 401

    # 2. 验证 Token
    result = verify_token(auth_header[7:])
    if isinstance(result, tuple):  # 验证失败，result 是 (错误, 状态码)
        return jsonify(result[0]), result[1]

    # 3. 把当前用户 id 挂到 g 上，供视图函数使用
    g.current_user_id = result["user_id"]