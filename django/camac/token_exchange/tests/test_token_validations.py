import pytest
from faker import Faker
from jwcrypto.common import (
    JWException,
    json_decode,
)
from jwcrypto.jwk import JWK
from jwcrypto.jwt import JWT

from camac.token_exchange.utils import extract_jwt_data

fake = Faker()


@pytest.mark.parametrize(
    "reason,exception,message",
    [
        ("not_encrypted", TypeError, "Expected JWE, got JWS"),
        ("jwe_secret", JWException, "InvalidSignature"),
        ("jwe_alg", JWException, "Invalid JWE alg header"),
        ("jwe_enc", JWException, "Invalid JWE enc header"),
        ("jwe_cty", JWException, "Invalid JWE cty header"),
        ("jwe_typ", JWException, "Invalid JWE typ header"),
        ("jwt_secret", JWException, "InvalidJWSSignature"),
        ("jwt_alg", JWException, "Invalid JWT alg header"),
        ("jwt_typ", JWException, "Invalid JWT typ header"),
        ("jwt_nbf", JWException, "Valid from"),
        ("jwt_exp", JWException, "Expired at"),
        ("jwt_iat", JWException, "Issued at is in the future (iat)"),
        (
            "jwt_valitity_period",
            JWException,
            "Validity period (exp - nbf) of token is longer than 60 seconds",
        ),
        ("jwt_iss", JWException, "Invalid 'iss' value"),
    ],
)
def test_token_validations(  # noqa: C901
    exception,
    jwt_token_data,
    message,
    mocker,
    reason,
    settings,
):
    token_data = {**jwt_token_data}

    jwt_key = JWK.from_password(settings.TOKEN_EXCHANGE_JWT_SECRET)
    jwt_headers = {"alg": "HS256", "typ": "JWT"}

    jwe_key = JWK.from_password(settings.TOKEN_EXCHANGE_JWE_SECRET)
    jwe_headers = {"alg": "dir", "enc": "A256CBC-HS512", "cty": "JWT", "typ": "JWT"}

    if reason == "jwe_secret":
        jwe_key = JWK.from_password(
            "abcdefghijklmnopqrstuvwabcdefghijklmnopqrstuvwabcdefghijklmnopqr"
        )
    elif reason == "jwe_alg":
        jwe_key = JWK.generate(kty="RSA", size=2048)

        public_key = JWK()
        public_key.import_key(**json_decode(jwe_key.export_public()))

        jwe_headers.update({"alg": "RSA-OAEP-256", "kid": public_key.thumbprint()})
    elif reason == "jwe_enc":
        jwe_secret = "abcdefghijklmnopqrstuvwabcdefghi"
        jwe_key = JWK.from_password(jwe_secret)
        settings.TOKEN_EXCHANGE_JWE_SECRET = jwe_secret
        jwe_headers["enc"] = "A256GCM"
    elif reason == "jwe_cty":
        jwe_headers["cty"] = "NOT JWT"
    elif reason == "jwe_typ":
        jwe_headers["typ"] = "NOT JWT"
    elif reason == "jwt_secret":
        jwt_key = JWK.from_password("wrong-secret")
    elif reason == "jwt_alg":
        jwt_headers["alg"] = "HS384"
    elif reason == "jwt_typ":
        jwt_headers["typ"] = "NOT JWT"
    elif reason == "jwt_nbf":
        token_data["nbf"] = fake.future_datetime().timestamp()
    elif reason == "jwt_exp":
        token_data["exp"] = fake.past_datetime().timestamp()
    elif reason == "jwt_iat":
        token_data["iat"] = fake.future_datetime().timestamp()
    elif reason == "jwt_valitity_period":
        token_data["exp"] = (
            token_data["nbf"] + settings.TOKEN_EXCHANGE_MAX_VALIDITY_PERIOD + 1
        )
    elif reason == "jwt_iss":
        token_data["iss"] = "http://some-other-issuer.com"

    signed_token = JWT(header=jwt_headers, claims=token_data)
    signed_token.make_signed_token(jwt_key)

    encrypted_token = JWT(header=jwe_headers, claims=signed_token.serialize())
    encrypted_token.make_encrypted_token(jwe_key)

    if reason == "not_encrypted":
        # Bypass JWE header validation as this would already raise an exception
        # about wrong headers because we can't create a valid signed token that
        # would pass those validations.
        mocker.patch("camac.token_exchange.utils.verify_jwe_headers")
        token = signed_token.serialize()
    else:
        token = encrypted_token.serialize()

    with pytest.raises(exception) as e:
        extract_jwt_data(token)

    assert message in str(e.value)
