def test_get_infractions_by_plate_success(client, auth_headers, registered_vehicle):
    response = client.get("/infractions/ABC1234", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["success"] 
    assert isinstance(response.json()["data"], list)

def test_get_infractions_by_plate_not_found(client, auth_headers):
    response = client.get("/infractions/ABC1234", headers=auth_headers)
    assert response.status_code == 404

def test_get_queries_by_user_id_success(client, auth_headers):
    response = client.get("/infractions/queries/1", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["success"] 
    assert isinstance(response.json()["data"], list)

def test_get_queries_by_user_id_not_found(client, auth_headers):
    response = client.get("/infractions/queries/2", headers=auth_headers)
    assert response.status_code == 404

def test_get_infractions_by_query_id_not_found(client, auth_headers):
    response = client.get("/infractions/queries/999/infractions", headers=auth_headers)
    assert response.status_code == 404