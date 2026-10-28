from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_orm_db(app):
    user = app.config["DB_USER"]
    password = app.config["DB_PASSWORD"]
    host = app.config["DB_HOST"]
    port = int(app.config["DB_PORT"])
    database = app.config["DB_NAME"]

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
        "?charset=utf8mb4"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # SQLAlchemy 自带的连接池配置
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_size": 10,       # 常驻连接池大小
        "max_overflow": 0,     # 不额外创建连接，总连接数最多为 10
        "pool_timeout": 30,    # 获取连接最多等待 30 秒
        "pool_recycle": 1800,  # 连接最长复用时间，避免 MySQL 断开闲置连接
        "pool_pre_ping": True  # 使用前检查连接是否有效
    }

    # db.init_app(app)