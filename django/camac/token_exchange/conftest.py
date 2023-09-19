import pytest
from faker import Faker
from jose import jwe, jwt
from jose.constants import ALGORITHMS
from rest_framework.test import APIClient

from camac.conftest import reload_urlconf

fake = Faker()


def encode_token(data, jwt_secret, jwe_secret):
    return jwe.encrypt(
        jwt.encode(data, jwt_secret, algorithm=ALGORITHMS.HS256),
        jwe_secret,
        algorithm=ALGORITHMS.DIR,
        encryption=ALGORITHMS.A256CBC_HS512,
    ).decode("utf-8")


@pytest.fixture(autouse=True)
def enable(settings):
    settings.ENABLE_TOKEN_EXCHANGE = True
    settings.KEYCLOAK_URL = "http://ebau-keycloak.local/auth"
    settings.KEYCLOAK_OIDC_TOKEN_URL = (
        "http://ebau-keycloak.local/auth/realms/ebau/protocol/openid-connect/token"
    )

    reload_urlconf("camac.urls")
    reload_urlconf("camac.token_exchange.urls")


@pytest.fixture
def jwt_client():
    return APIClient()


@pytest.fixture
def jwt_token_data(settings):
    return {
        "profileId": 1,
        "firstName": "John",
        "name": "Doe",
        "email": "john.doe@acme.com",
        "exp": fake.future_datetime(),
        "iss": settings.TOKEN_EXCHANGE_JWT_ISSUER,
    }


@pytest.fixture
def jwt_token(jwt_token_data, settings):
    return encode_token(
        jwt_token_data,
        settings.TOKEN_EXCHANGE_JWT_SECRET,
        settings.TOKEN_EXCHANGE_JWE_SECRET,
    )


@pytest.fixture
def invalid_exp_jwt_token(jwt_token_data, settings):
    return encode_token(
        {**jwt_token_data, "exp": fake.past_datetime()},
        settings.TOKEN_EXCHANGE_JWT_SECRET,
        settings.TOKEN_EXCHANGE_JWE_SECRET,
    )


@pytest.fixture
def invalid_iss_jwt_token(jwt_token_data, settings):
    return encode_token(
        {**jwt_token_data, "iss": "https://invalid.issuer.com"},
        settings.TOKEN_EXCHANGE_JWT_SECRET,
        settings.TOKEN_EXCHANGE_JWE_SECRET,
    )


@pytest.fixture
def invalid_signature_jwt_token(jwt_token_data, settings):
    return encode_token(
        jwt_token_data,
        "some-incorrect-secret",
        settings.TOKEN_EXCHANGE_JWE_SECRET,
    )


@pytest.fixture
def failed_decryption_jwt_token(jwt_token_data, settings):
    return encode_token(
        jwt_token_data,
        settings.TOKEN_EXCHANGE_JWT_SECRET,
        "abcdefghijklmnopqrstuvwabcdefghijklmnopqrstuvwabcdefghijklmnopqr",
    )
