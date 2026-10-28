import logging

from flask import Flask

# from app.db import init_pool
from app.errors import register_error_handlers
from app.orm_db import init_orm_db, db
# from app.routes.auth import auth_bp
from app.routes.orm_auth import auth_bp
from app.routes.orm_todos import todo_bp
# from app.routes.todos import old_todo_bp
from config import config

def create_app(test_config,config_name="default"):

    """应用工厂：按需创建、配置 Flask 实例"""
    app = Flask(__name__,static_folder="../static",static_url_path="/")
    app.config.from_object(config[config_name])

    # 关键修改 1：优先加载测试配置
    if test_config:
        app.config.update(test_config)
    else:
        # 只有在非测试环境（没有传 test_config）时，才去初始化 MySQL 连接串
        # init_pool(app)
        init_orm_db(app)

    db.init_app(app)

    from flask_cors import CORS
    CORS(app)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(filename)s:%(lineno)d - %(message)s",
        filename="app.log"
    )

    # 注册蓝图（第 5 节内容）
    # app.register_blueprint(auth_bp, url_prefix="/api")
    # app.register_blueprint(old_todo_bp, url_prefix="/api")
    app.register_blueprint(todo_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api")
    register_error_handlers(app)

    return app