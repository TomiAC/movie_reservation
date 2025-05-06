import pytest

@pytest.fixture
def created_reservation(client, created_showtime, user_user_token):
    response_seats = client.get(f"/showtime/{created_showtime}", headers={"Authorization": f"Bearer {user_user_token}"})
    response = client.post(
        "/reservation/",
        json={"showtime_id": created_showtime, "amount": 2, "seats_list": [response_seats.json()["available_seats"][0]["id"], response_seats.json()["available_seats"][1]["id"]]},
        headers={"Authorization": f"Bearer {user_user_token}"}
    )
    assert response.status_code == 200
    return response.json()["id"]

def test_register_reservation(client, created_showtime, user_user_token):
    response_seats = client.get(f"/showtime/{created_showtime}", headers={"Authorization": f"Bearer {user_user_token}"})
    response = client.post(
        "/reservation/",
        json={"showtime_id": created_showtime, "amount": 2, "seats_list": [response_seats.json()["available_seats"][0]["id"], response_seats.json()["available_seats"][1]["id"]]},
        headers={"Authorization": f"Bearer {user_user_token}"}
    )
    assert response.status_code == 200

def test_invalid_seat_amout_register_reservation(client, created_showtime, user_user_token):
    response_seats = client.get(f"/showtime/{created_showtime}", headers={"Authorization": f"Bearer {user_user_token}"})
    response = client.post(
        "/reservation/",
        json={"showtime_id": created_showtime, "amount": 3, "seats_list": [response_seats.json()["available_seats"][0]["id"], response_seats.json()["available_seats"][1]["id"]]},
        headers={"Authorization": f"Bearer {user_user_token}"}
    )
    assert response.status_code == 400

def test_already_active_reservation(client, created_showtime, user_user_token):
    response_seats = client.get(f"/showtime/{created_showtime}", headers={"Authorization": f"Bearer {user_user_token}"})
    client.post(
        "/reservation/",
        json={"showtime_id": created_showtime, "amount": 2, "seats_list": [response_seats.json()["available_seats"][0]["id"], response_seats.json()["available_seats"][1]["id"]]},
        headers={"Authorization": f"Bearer {user_user_token}"}
    )
    response = client.post(
        "/reservation/",
        json={"showtime_id": created_showtime, "amount": 2, "seats_list": [response_seats.json()["available_seats"][4]["id"], response_seats.json()["available_seats"][5]["id"]]},
        headers={"Authorization": f"Bearer {user_user_token}"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "User already has an active reservation on this showtime"

def test_invalid_showtime_reservation(client, created_showtime, user_user_token):
    response_seats = client.get(f"/showtime/{created_showtime}", headers={"Authorization": f"Bearer {user_user_token}"})
    response = client.post(
        "/reservation/",
        json={"showtime_id": "invalid_showtime", "amount": 2, "seats_list": [response_seats.json()["available_seats"][0]["id"], response_seats.json()["available_seats"][1]["id"]]},
        headers={"Authorization": f"Bearer {user_user_token}"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid showtime id"

def test_invalid_seat_code_reservation(client, created_showtime, user_user_token):
    response = client.post(
        "/reservation/",
        json={"showtime_id": created_showtime, "amount": 2, "seats_list": ["IV", "IV1"]},
        headers={"Authorization": f"Bearer {user_user_token}"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid seat code"

def test_already_reserved_seat_reservation(client, created_showtime, admin_token, user_user_token):
    response_seats = client.get(f"/showtime/{created_showtime}", headers={"Authorization": f"Bearer {user_user_token}"})
    reponse_admin = client.post(
        "/reservation/",
        json={"showtime_id": created_showtime, "amount": 2, "seats_list": [response_seats.json()["available_seats"][0]["id"], response_seats.json()["available_seats"][1]["id"]]},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    print(reponse_admin.json())
    response = client.post(
        "/reservation/",
        json={"showtime_id": created_showtime, "amount": 2, "seats_list": [response_seats.json()["available_seats"][0]["id"], response_seats.json()["available_seats"][1]["id"]]},
        headers={"Authorization": f"Bearer {user_user_token}"}
    )
    print(response.json())
    assert response.status_code == 400
    assert response.json()["detail"] == "One or more seats are already reserved"

def test_get_history_showtimes(client, user_user_token):
    response = client.get("/reservation/user/history", headers={"Authorization": f"Bearer {user_user_token}"})
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_reservation(client, created_reservation, user_user_token):
    response = client.get(f"/reservation/{created_reservation}", headers={"Authorization": f"Bearer {user_user_token}"})
    assert response.status_code == 200
    assert response.json()["id"] == created_reservation

def test_get_invalid_reservation(client, user_user_token):
    response = client.get(f"/reservation/invalid_reservation", headers={"Authorization": f"Bearer {user_user_token}"})
    assert response.status_code == 400

def test_get_invalid_user_reservation(client, admin_token):
    response = client.get(f"/reservation/invalid_reservation", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 400

def test_delete_reservation(client, created_reservation, user_user_token):
    response = client.delete(f"/reservation/{created_reservation}", headers={"Authorization": f"Bearer {user_user_token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Reservation deleted"

def test_delete_invalid_reservation(client, user_user_token):
    response = client.delete(f"/reservation/invalid_reservation", headers={"Authorization": f"Bearer {user_user_token}"})
    assert response.status_code == 400