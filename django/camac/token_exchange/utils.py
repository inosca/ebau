from json import JSONDecodeError

from django.conf import settings
from django.utils import timezone
from jwcrypto.common import JWException, base64url_decode, json_decode
from jwcrypto.jwk import JWK
from jwcrypto.jwt import JWT


def extract_headers(raw_token: str) -> dict:
    try:
        return json_decode(base64url_decode(raw_token.split(".")[0]))
    except (IndexError, ValueError, JSONDecodeError):  # pragma: no cover
        raise JWException("Could not parse headers")


def verify_jwe_headers(headers: dict) -> None:
    if headers.get("alg") != "dir":
        raise JWException("Invalid JWE alg header")
    elif headers.get("enc") not in ["A256CBC-HS512", "A128CBC-HS256"]:
        raise JWException("Invalid JWE enc header")
    elif headers.get("cty") != "JWT":
        raise JWException("Invalid JWE cty header")
    elif headers.get("typ") != "JWT":
        raise JWException("Invalid JWE typ header")


def verify_jwt_headers(headers: dict) -> None:
    if headers.get("alg") != "HS256":
        raise JWException("Invalid JWT alg header")
    elif headers.get("typ") != "JWT":
        raise JWException("Invalid JWT typ header")


def verify_jwt_claims(claims: dict) -> None:
    max_validity_period = settings.TOKEN_EXCHANGE_MAX_VALIDITY_PERIOD

    if claims["iat"] > timezone.now().timestamp():
        raise JWException("Issued at is in the future (iat)")
    elif max_validity_period and claims["exp"] - claims["nbf"] > max_validity_period:
        raise JWException(
            f"Validity period (exp - nbf) of token is longer than {max_validity_period} seconds"
        )


def extract_jwt_data(encrypted_token: str) -> dict:
    verify_jwe_headers(extract_headers(encrypted_token))

    signed_token = JWT(
        jwt=encrypted_token,
        key=JWK.from_password(settings.TOKEN_EXCHANGE_JWE_SECRET),
        expected_type="JWE",
    )

    verify_jwt_headers(extract_headers(signed_token.claims))

    token = JWT(
        jwt=signed_token.claims,
        key=JWK.from_password(settings.TOKEN_EXCHANGE_JWT_SECRET),
        expected_type="JWS",
        check_claims={
            "exp": None,
            "nbf": None,
            "iat": None,
            "iss": settings.TOKEN_EXCHANGE_JWT_ISSUER,
        },
    )

    verify_jwt_claims(json_decode(token.claims))

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

    data["attributes"] = {"lot": data.pop("lot")}

    return data


def build_username(jwt_data: dict):
    return settings.TOKEN_EXCHANGE_USERNAME_PREFIX + str(
        jwt_data[settings.TOKEN_EXCHANGE_JWT_IDENTIFIER_PROPERTY]
    )
