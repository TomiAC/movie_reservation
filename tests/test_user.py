from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

#Checks if a user can be registered
def test_register_user():
    response = client.post("/auth/register", json={"name": "test_name", "password": "test_pass", "email": "test@example.com"})
    assert response.status_code == 200

#Checks if a user can't be registered becase the email is already registered
def test_register_user_duplicate():
    client.post("/auth/register", json={"name": "test_name", "password": "test_pass", "email": "test@example.com"})
    response = client.post("/auth/register", json={"name": "test_name", "password": "test_pass", "email": "test@example.com"})
    print(response.status_code)
    assert response.status_code == 400

def test_login_user():
    client.post("/auth/register", json={"name": "test_name", "password": "test_pass", "email": "test@example.com"})
    response = client.post("/auth/token", data={"username": "test@example.com", "password": "test_pass"})
    assert response.status_code == 200

def test_login_user_incorrect_password():
    client.post("/auth/register", json={"name": "test_name", "password": "test_pass", "email": "test@example.com"})
    response = client.post("/auth/token", data={"username": "test@example.com", "password": "wrong_pass"})
    assert response.status_code == 400

def test_login_user_incorrect_email():
    response = client.post("/auth/token", data={"username": "wrong@example", "password": "test_pass"})
    assert response.status_code == 400

def test_refresh_token():
    response = client.post("/auth/token", data={"username": "test@example.com", "password": "test_pass"})
    refresh_token = response.json()["refresh_token"]
    response = client.post("/auth/refresh", params={"refresh_token": refresh_token})
    assert response.status_code == 200

def test_invalid_refresh_token():
    response = client.post("/auth/refresh", params={"refresh_token": "invalid_token"})
    assert response.status_code == 401

def test_change_password():
    response_login = client.post("/auth/token", data={"username": "test@example.com", "password": "test_pass"})
    response = client.put("/auth/password", json={"old_password": "test_pass", "new_password": "new_pass"}, headers={"Authorization": "Bearer " + response_login.json()["access_token"]})
    assert response.status_code == 200

def test_change_password_incorrect_password():
    response_login = client.post("/auth/token", data={"username": "test@example.com", "password": "new_pass"})
    response = client.put("/auth/password", json={"old_password": "wrong_pass", "new_password": "new_pass"}, headers={"Authorization": "Bearer " + response_login.json()["access_token"]})
    assert response.status_code == 400

def test_delete_user():
    response_login = client.post("/auth/token", data={"username": "test@example.com", "password": "new_pass"})
    response = client.delete("/auth/user", headers={"Authorization": "Bearer " + response_login.json()["access_token"]})
    assert response.status_code == 200