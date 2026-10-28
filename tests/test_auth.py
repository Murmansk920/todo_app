def test_register_success(client):
    # Arrange 已在 fixture 里做好（空库 + 模拟浏览器）
    resp = client.post("/api/register",
                        json={"username": "alice", "password": "123456"})
    assert resp.status_code == 201

def test_register_duplicate(client):
    body = {"username": "alice", "password": "123456"}
    client.post("/api/register", json=body)              # 第一次：成功
    resp = client.post("/api/register", json=body)        # 第二次：应 409
    assert resp.status_code == 409
    assert "已存在" in resp.get_json()["error"]    # 统一错误格式的好处

def test_register_missing_field(client):
    resp = client.post("/api/register", json={"username": "bob"})  # 缺密码
    assert resp.status_code == 400

def test_login_wrong_password(client):
    client.post("/api/register", json={"username": "carol", "password": "123456"})
    resp = client.post("/api/login", json={"username": "carol", "password": "wrong"})
    assert resp.status_code == 401

def test_protected_without_token(client):
    resp = client.get("/api/todos")          # 没带 Token
    assert resp.status_code == 401