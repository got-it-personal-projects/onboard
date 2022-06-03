import pytest


@pytest.mark.parametrize(
    "headers",
    [
        {},
        {"Authorization": ""},
        {"Authorization": "Bearer"},
        {"Authorization": "Bearer invalid"},
        {"Authorization": "Bearer invalid authorization"},
    ],
)
def test_send_invalid_request_headers(client, headers):
    response = client.get("/users/me", headers=headers)

    assert response.status_code == 401
