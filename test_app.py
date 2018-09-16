
# pytest automatically injects fixtures
# that are defined in conftest.py
# in this case, client is injected
def test_index(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json["result"]["content"] == "hello world!"


def test_mirror(client):
    res = client.get("/mirror/Tim")
    assert res.status_code == 200
    assert res.json["result"]["name"] == "Tim"


def test_get_users(client):
    res = client.get("/users")
    assert res.status_code == 200

    res_users = res.json["result"]["users"]
    assert len(res_users) == 4
    assert res_users[0]["name"] == "Aria"


def tests_get_users_with_team(client):
    res = client.get("/users?team=LWB")
    assert res.status_code == 200

    res_users = res.json["result"]["users"]
    assert len(res_users) == 2
    assert res_users[1]["name"] == "Tim"


def test_get_user_id(client):
    res = client.get("/users/1")
    assert res.status_code == 200

    res_user = res.json["result"]["user"]
    assert res_user["name"] == "Aria"
    assert res_user["age"] == 19

def test_create_user(client):
    res = client.post("/users", json = {"name": "Neeraj", "age": 17, "team": "TBD"})
    assert res.status_code == 201

    res_user = client.get("/users/5").json["result"]["user"]
    assert res_user["name"] == "Neeraj"
    assert res_user["age"] == 17
    assert res_user["team"] == "TBD"
    assert res_user["id"] is not None

def test_update_user(client):
    res = client.put("/users/5", json={"name": "Shreyas", "age": 18})
    assert res.status_code == 200

    res_user = client.get("/users/5").json["result"]["user"]
    assert res_user["name"] == "Shreyas"
    assert res_user["age"] == 18
    assert res_user["team"] == "TBD"
    assert res_user["id"] is not None

def test_delete_user(client):
    res = client.delete("/users/5")
    assert res.status_code == 200

    res2 = client.get("/users/5")
    assert res2.status_code == 404