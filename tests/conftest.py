import pytest
from app import create_app
from app.orm_db import db

@pytest.fixture()
def app():
    app = create_app(test_config={
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with app.app_context():
        db.create_all()        # 准备：建一张全新的空表
        yield app
        db.session.remove()
        db.drop_all()        # 清理：测试结束，表销毁

@pytest.fixture()
def client(app):
    return app.test_client()   # 模拟浏览器，不发真网络请求

@pytest.fixture()
def auth_headers(client):
    """注册 + 登录一条龙，返回带 Token 的请求头"""
    client.post("/api/register", json={"username": "tester", "password": "123456"})
    resp = client.post("/api/login", json={"username": "tester", "password": "123456"})
    token = resp.get_json()["token"]
    return {"Authorization": f"Bearer {token}"}