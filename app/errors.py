from flask import jsonify, g


def register_error_handlers(app):
    """在工厂里调用，统一注册错误处理"""

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "资源不存在", "code": 404}), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({"error": "请求方法不允许", "code": 405}), 405

    @app.errorhandler(409)
    def conflict(error):
        return jsonify({"error":"用户已存在", "code": 409}), 409

    # @app.errorhandler(Exception)
    # def internal_error(error):
    #     if g and g.current_user_id:
    #         app.logger.error(f"服务器错误: {error}-curent_user_id={g.current_user_id}")  # 记录日志
    #     else:
    #         app.logger.error(f"服务器错误: {error}")
    #     return jsonify({"error": "服务器内部错误", "code": 500}), 500