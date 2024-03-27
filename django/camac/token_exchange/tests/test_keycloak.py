import jwt
import pytest

from camac.token_exchange.keycloak import KeycloakClient


@pytest.mark.vcr()
def test_keycloak_client(snapshot):
    client = KeycloakClient()

    username = "egov:123"
    user_data = {"firstName": "Test", "name": "User", "email": "email@example.com"}

    # first call should create a new user
    assert not client.update_or_create_user(username, user_data)
    assert client.get_user(username) == snapshot

    # second call should update the existing user
    user_data.update({"firstName": "John", "name": "Doe"})

    assert client.update_or_create_user(username, user_data)
    assert client.get_user(username) == snapshot

    token = client.token_exchange(username)
    assert token == snapshot

    decoded_token = jwt.decode(
        token["access_token"], options={"verify_signature": False}
    )
    assert decoded_token == snapshot
