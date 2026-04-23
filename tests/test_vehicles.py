def test_create_vehicle_success(client, auth_headers):
    response = client.post("/vehicles", json={
        "plate": "QTQ4200",
        "type": "cavalo",
        "company_cnpj": "00000123456789"
    }, headers=auth_headers)
    assert response.status_code == 201

def test_create_duplicate_vehicle(client, auth_headers):
    client.post("/vehicles", json={
        "plate": "QTQ4200",
        "type": "cavalo",
        "company_cnpj": "00000123456789"
    }, headers=auth_headers)

    response = client.post("vehicles", json={
        "plate": "QTQ4200",
        "type": "cavalo",
        "company_cnpj": "00000123456789"
    }, headers=auth_headers)

    assert response.status_code == 409

def test_get_vehicles(client, auth_headers):
    client.post("/vehicles", json={
        "plate": "QTQ4200",
        "type": "cavalo",
        "company_cnpj": "0000123456789"
    }, headers=auth_headers)

    client.post("/vehicles", json={
        "plate": "PRU6816",
        "type": "cavalo",
        "company_cnpj": "0000123456789"
    }, headers=auth_headers)

    response = client.get("/vehicles", headers=auth_headers)

    assert response.status_code == 200