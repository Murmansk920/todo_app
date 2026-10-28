def test_create_and_list(client, auth_headers):
    # Act：建两条任务
    for title in ["写周报", "买牛奶"]:
        resp = client.post("/api/todos", json={"title": title}, headers=auth_headers)
        assert resp.status_code == 200

    # Assert：列表里应有 2 条
    data = client.get("/api/todos", headers=auth_headers).get_json()
    assert data["total"] == 2

def test_pagination(client, auth_headers):
    for i in range(15):                       # 造 15 条数据
        client.post("/api/todos", json={"title": f"任务{i}"}, headers=auth_headers)
    data = client.get("/api/todos?page=2&size=10", headers=auth_headers).get_json()
    assert len(data["items"]) == 5          # 第 2 页剩 5 条
    assert data["pages"] == 2

def test_isolation_between_users(client):
    """用户 B 绝看不到用户 A 的任务——数据隔离的自动化守卫"""
    client.post("/api/register", json={"username": "user_a", "password": "123456"})
    client.post("/api/register", json={"username": "user_b", "password": "123456"})
    headers_a = {"Authorization": "Bearer " + client.post(
        "/api/login", json={"username": "user_a", "password": "123456"}).get_json()["token"]}
    headers_b = {"Authorization": "Bearer " + client.post(
        "/api/login", json={"username": "user_b", "password": "123456"}).get_json()["token"]}

    client.post("/api/todos", json={"title": "A 的秘密任务"}, headers=headers_a)
    data_b = client.get("/api/todos", headers=headers_b).get_json()
    assert data_b["total"] == 0              # B 的世界里一无所有