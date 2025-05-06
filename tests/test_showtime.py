def test_register_showtime(client, created_movie, created_auditorium, admin_token):
    response = client.post(
        "/showtime/",
        json={"movie_id": created_movie, "auditorium_id": created_auditorium, "start_time": "2025-05-20 12:00", "avaible_tickets": 0, "status": "active"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.json()["movie_id"] == created_movie
    assert response.json()["auditorium_id"] == created_auditorium
    assert response.json()["start_time"] == "2025-05-20 12:00"
    assert response.status_code == 200

def test_get_showtime(client, created_showtime, created_auditorium, admin_token):
    response = client.get(f"/showtime/{created_showtime}", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json()["showtime_searched"]["auditorium_id"] == created_auditorium

def test_get_invalid_showtime(client, admin_token):
    response = client.get(f"/showtime/invalid_showtime", headers={"Authorization": f"Bearer {admin_token}"})
    print(response.json())
    assert response.status_code == 404

def test_get_showtimes(client, admin_token):
    response = client.get("/showtime/", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_showtime_availability(client, created_showtime, admin_token):
    response = client.get(f"/showtime/availability/{created_showtime}", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json() == 100

def test_get_movie_showtimes(client, created_movie, created_auditorium, admin_token):
    response_movie = client.post(
        "/showtime/",
        json={"movie_id": created_movie, "auditorium_id": created_auditorium, "start_time": "2025-06-20 12:00", "avaible_tickets": 0, "status": "active"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    data_movie = response_movie.json()
    response = client.get(f"/showtime/movie/{data_movie['movie_id']}", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1

def test_get_movie_showtime_history(client, created_movie, created_auditorium, admin_token):
    response_movie = client.post(
        "/showtime/",
        json={"movie_id": created_movie, "auditorium_id": created_auditorium, "start_time": "2025-06-20 12:00", "avaible_tickets": 0, "status": "active"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    client.post(
        "/showtime/",
        json={"movie_id": created_movie, "auditorium_id": created_auditorium, "start_time": "2024-06-20 12:00", "avaible_tickets": 0, "status": "active"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    data_movie = response_movie.json()
    response = client.get(f"/showtime/movie/history/{data_movie['movie_id']}", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2

def test_update_start_time_showtime(client, created_showtime, admin_token):
    response = client.put(f"/showtime/{created_showtime}", json={"start_time": "2025-06-20 12:00"}, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json()["start_time"] == "2025-06-20 12:00"

def test_update_invalid_start_time_showtime(client, created_showtime, admin_token):
    response = client.put(f"/showtime/{created_showtime}", json={"start_time": "2025-03-20 12:00"}, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid start time"

def test_update_avaible_tickets_showtime(client, created_showtime, admin_token):
    response = client.put(f"/showtime/{created_showtime}", json={"avaible_tickets": 90}, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json()["avaible_tickets"] == 90

def test_update_invalid_avaible_tickets_showtime(client, created_showtime, admin_token):
    response = client.put(f"/showtime/{created_showtime}", json={"avaible_tickets": -1}, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid avaible tickets"

def test_update_not_enough_seats_showtime(client, created_movie, created_small_auditorium, admin_token):
    response = client.post(
        "/showtime/",
        json={"movie_id": created_movie, "auditorium_id": created_small_auditorium, "start_time": "2024-06-20 12:00", "avaible_tickets": 0, "status": "active"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    reponse_update_showtime = client.put(f"/showtime/{response.json()['id']}", json={"avaible_tickets": 101}, headers={"Authorization": f"Bearer {admin_token}"})
    assert reponse_update_showtime.status_code == 400
    assert reponse_update_showtime.json()["detail"] == "Not enough seats"

def test_delete_showtime(client, created_showtime, admin_token):
    response = client.delete(f"/showtime/{created_showtime}", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200

def test_delete_invalid_showtime(client, admin_token):
    response = client.delete(f"/showtime/invalid_showtime", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 404