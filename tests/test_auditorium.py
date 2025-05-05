from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

auditorium_id = ""

def test_register_auditorium(admin_token):
    response = client.post("/auditorium/", json={"number": "1", "seats": 100, "rows": 10, "columns": 10}, headers={"Authorization": f"Bearer {admin_token}"})
    print(response)
    auditorium_id = response.json()["id"]
    assert response.status_code == 200

def test_get_auditorium():
    response = client.get("/auditorium/" + auditorium_id)
    print(response.json()[0]["number"])
    assert response.status_code == 200

def test_get_auditoriums():
    response = client.get("/auditorium/")
    assert response.status_code == 200

def test_delete_auditorium(admin_token):
    print(auditorium_id)
    response = client.delete("/auditorium/" + auditorium_id, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200