def test_register_auditorium(client, admin_token):
    response = client.post("/auditorium/", json={"number": "1", "seats": 100, "rows": 10, "columns": 10}, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200

def test_get_auditorium(client, created_auditorium, admin_token):
    response = client.post(f"/auditorium/{created_auditorium}", json={"number": "1", "seats": 100, "rows": 10, "columns": 10}, headers={"Authorization": f"Bearer {admin_token}"})
    response = client.get("/auditorium/")
    print(response.json()[0]["number"])
    assert response.status_code == 200

def test_get_auditoriums(client):
    response = client.get("/auditorium/")
    assert response.status_code == 200

def test_delete_auditorium(client, created_auditorium, admin_token):
    response = client.delete(f"/auditorium/{created_auditorium}", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200