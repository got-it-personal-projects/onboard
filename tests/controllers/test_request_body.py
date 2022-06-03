def test_send_invalid_request_body(client):
    response = client.post("/users", data="invalid")

    assert response.status_code == 400
