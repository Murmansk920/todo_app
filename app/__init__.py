import logging

from flask import Flask

from app.db import init_pool
from app.errors import register_error_handlers
from app.routes.auth import auth_bp
from app.routes.todos import todo_bp
from config import config

def create_app(config_name="default"):
    """应用工厂：按需创建、配置 Flask 实例"""
    app = Flask(__name__,static_folder="static",static_url_path="/")
    app.config.from_object(config[config_name])
    from flask_cors import CORS
    CORS(app)
    init_pool(app)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(filename)s:%(lineno)d - %(message)s",
        filename="app.log"
    )

    # 注册蓝图（第 5 节内容）
    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(todo_bp, url_prefix="/api")
    register_error_handlers(app)

    return app