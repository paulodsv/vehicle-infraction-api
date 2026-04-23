def test_register_success(client):
    response = client.post("/auth/register", json={
        "email": "test@email.com",
        "password": "123456"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "test@email.com"

def test_already_registered_email(client):
    response = client.post("auth/register", json={
        "email": "test@email.com",
        "password": "123456"
    })

    response = client.post("auth/register", json={
        "email": "test@email.com",
        "password": "123456"
    })

    assert response.status_code == 409

def test_user_login_success(client):
    response = client.post("auth/register", json={
        "email": "test@email.com",
        "password": "123456"
    })

    response = client.post("auth/login", json={
        "email": "test@email.com",
        "password": "123456"
    })
    
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_user_login_with_wrong_password(client):
    response = client.post("auth/register", json={
        "email": "test@email.com",
        "password": "123456"
    })

    response = client.post("auth/login", json={
        "email": "test@email.com",
        "password": "12345"
    })

    assert response.status_code == 401