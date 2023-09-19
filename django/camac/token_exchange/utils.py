from django.conf import settings
from jose import jwe, jwt
from jose.constants import ALGORITHMS


def extract_jwt_data(encrypted_token: str) -> dict:
    signed_token = jwe.decrypt(encrypted_token, settings.TOKEN_EXCHANGE_JWE_SECRET)

    return jwt.decode(
        signed_token,
        settings.TOKEN_EXCHANGE_JWT_SECRET,
        algorithms=[ALGORITHMS.HS256],
        issuer=settings.TOKEN_EXCHANGE_JWT_ISSUER,
        options={
            "verify_exp": True,
            "verify_iss": True,
            "require_exp": True,
            "require_iss": True,
        },
    )


def extract_sync_data(jwt_data: dict) -> dict:
    return {
        keycloak_property: jwt_data[jwt_property]
        for jwt_property, keycloak_property in settings.TOKEN_EXCHANGE_JWT_SYNC_PROPERTIES.items()
    }


def build_username(jwt_data: dict):
    return settings.TOKEN_EXCHANGE_USERNAME_TEMPLATE.format(
        identifier=jwt_data[settings.TOKEN_EXCHANGE_JWT_IDENTIFIER_PROPERTY]
    )
