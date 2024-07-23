from django.conf import settings
from jwcrypto.common import json_decode
from jwcrypto.jwk import JWK
from jwcrypto.jwt import JWT


def extract_jwt_data(encrypted_token: str) -> dict:
    signed_token = JWT(
        jwt=encrypted_token,
        key=JWK.from_password(settings.TOKEN_EXCHANGE_JWE_SECRET),
        expected_type="JWE",
    )

    token = JWT(
        jwt=signed_token.claims,
        key=JWK.from_password(settings.TOKEN_EXCHANGE_JWT_SECRET),
        expected_type="JWS",
        check_claims={
            "exp": None,
            "iss": settings.TOKEN_EXCHANGE_JWT_ISSUER,
        },
    )

    return json_decode(token.claims)


def extract_sync_data(jwt_data: dict) -> dict:
    data = {
        keycloak_property: jwt_data.get(jwt_property)
        for jwt_property, keycloak_property in settings.TOKEN_EXCHANGE_JWT_SYNC_PROPERTIES.items()
    }

    organisationName = data.pop("organisationName")

    if organisationName:
        data["firstName"] = ""
        data["lastName"] = organisationName

    return data


def build_username(jwt_data: dict):
    return settings.TOKEN_EXCHANGE_USERNAME_PREFIX + str(
        jwt_data[settings.TOKEN_EXCHANGE_JWT_IDENTIFIER_PROPERTY]
    )
