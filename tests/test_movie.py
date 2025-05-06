def test_register_movie(client, admin_token):
    response = client.post(
        "/movie/",
        json={"name": "Test Movie", "description": "Test Description", "poster": "https://example.com/poster.jpg", "duration": 120, "genre": "Action"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200

def test_get_movie(client, created_movie, admin_token):
    response = client.get(f"/movie/{created_movie}", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200

def test_delete_movie(client, created_movie, admin_token):
    response = client.delete(f"/movie/{created_movie}", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200

def test_update_movie_name(client, created_movie, admin_token):
    response = client.put(f"/movie/{created_movie}", json={"name": "Updated Movie"}, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200

def test_update_movie_description(client, created_movie, admin_token):
    response = client.put(f"/movie/{created_movie}", json={"description": "Updated Description"}, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200

def test_update_movie_poster(client, created_movie, admin_token):
    response = client.put(f"/movie/{created_movie}", json={"poster": "https://example.com/updated_poster.jpg"}, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200

def test_update_movie_duration(client, created_movie, admin_token):
    response = client.put(f"/movie/{created_movie}", json={"duration": 150}, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200

def test_update_movie_genre(client, created_movie, admin_token):
    response = client.put(f"/movie/{created_movie}", json={"genre": "Comedy"}, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200