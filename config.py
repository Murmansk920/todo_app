import os

class Config:
    """基础配置"""
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = os.environ.get("DB_PORT", "3306")
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
    DB_NAME = os.environ.get("DB_NAME", "library")

class DevelopmentConfig(Config):
    """开发环境"""
    DEBUG = True

class ProductionConfig(Config):
    """生产环境"""
    DEBUG = False

# 配置字典，按名字取用
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}