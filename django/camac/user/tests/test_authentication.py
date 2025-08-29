import json

import pytest
from django.db import connection
from django.test.utils import CaptureQueriesContext
from jwcrypto.common import JWException
from jwcrypto.jwt import JWTExpired
from mozilla_django_oidc.contrib.drf import OIDCAuthentication
from rest_framework import exceptions, status
from rest_framework.exceptions import AuthenticationFailed

from camac.applicants.models import Applicant
from camac.user.authentication import JSONWebTokenKeycloakAuthentication


def test_authenticate_no_headers(rf):
    request = rf.request()
    assert JSONWebTokenKeycloakAuthentication().authenticate(request) is None


def test_authenticate_disabled_user(rf, admin_user, mocker, clear_cache, settings):
    token_dict = {
        "sub": admin_user.username,
        "email": admin_user.email,
        "family_name": admin_user.surname,
        "given_name": admin_user.name,
        settings.OIDC_USERNAME_CLAIM: admin_user.username,
    }
    decode_token = mocker.patch("keycloak.KeycloakOpenID.decode_token")
    decode_token.return_value = token_dict
    mocker.patch("keycloak.KeycloakOpenID.certs")

    mocker.patch("keycloak.KeycloakOpenID.userinfo", return_value=token_dict)

    admin_user.disabled = True
    admin_user.save()

    request = rf.request(HTTP_AUTHORIZATION="Bearer some_token")
    with pytest.raises(AuthenticationFailed):
        JSONWebTokenKeycloakAuthentication().authenticate(request)


@pytest.mark.parametrize("demo_mode", [True, False])
@pytest.mark.parametrize(
    "token_value,username",
    [
        (
            {
                "sub": "new-here",
                "email": "new-guy@example.com",
                "family_name": "New",
                "given_name": "Guy",
            },
            "new-here",
        ),
        (
            {
                "sub": "service-account-gemeinde",
                "email": "new-guy@example.com",
                "clientId": "testClient",
            },
            "service-account-gemeinde",
        ),
    ],
)
def test_authenticate_new_user(
    rf,
    admin_user,
    mocker,
    demo_mode,
    settings,
    application_settings,
    token_value,
    username,
    applicant_factory,
    clear_cache,
):
    token_value[settings.OIDC_USERNAME_CLAIM] = token_value["sub"]

    applicant_factory(email=token_value["email"], invitee=None)

    if demo_mode:
        admin_group = admin_user.groups.first()
        inexistent_group = 2138242342
        settings.DEMO_MODE = True
        application_settings["DEMO_MODE_GROUPS"] = [admin_group.pk, inexistent_group]

    decode_token = mocker.patch("keycloak.KeycloakOpenID.decode_token")
    decode_token.return_value = token_value
    mocker.patch("keycloak.KeycloakOpenID.certs")

    userinfo = mocker.patch("keycloak.KeycloakOpenID.userinfo")
    userinfo.return_value = token_value

    request = rf.request(HTTP_AUTHORIZATION="Bearer some_token")
    user, token = JSONWebTokenKeycloakAuthentication().authenticate(request)

    if demo_mode:
        assert user.groups.count() == 1
        assert user.groups.first() == admin_group
    else:
        assert user.groups.count() == 0
    assert decode_token.return_value == token


@pytest.mark.parametrize(
    "token_value, expected",
    [
        (
            {
                "sub": "service-account-gemeinde",
                "email": "new-guy@example.com",
                "clientId": "testClient",
            },
            "new-guy@example.com",
        ),
        (
            {
                "sub": "service-account-gemeinde",
                "clientId": "testClient",
            },
            "service-account-gemeinde@placeholder.org",
        ),
    ],
)
def test_authenticate_email_fallback(
    rf,
    admin_user,
    mocker,
    token_value,
    applicant_factory,
    clear_cache,
    expected,
    settings,
):
    token_value[settings.OIDC_USERNAME_CLAIM] = token_value["sub"]

    decode_token = mocker.patch("keycloak.KeycloakOpenID.decode_token")
    decode_token.return_value = token_value
    mocker.patch("keycloak.KeycloakOpenID.certs")

    userinfo = mocker.patch("keycloak.KeycloakOpenID.userinfo")
    userinfo.return_value = token_value

    request = rf.request(HTTP_AUTHORIZATION="Bearer some_token")
    user, token = JSONWebTokenKeycloakAuthentication().authenticate(request)

    assert user.email == expected


def test_authenticate_ok(rf, admin_user, mocker, clear_cache, settings):
    token_value = {
        "sub": admin_user.username,
        "email": admin_user.email,
        "family_name": admin_user.surname,
        "given_name": admin_user.name,
        settings.OIDC_USERNAME_CLAIM: admin_user.username,
    }
    decode_token = mocker.patch("keycloak.KeycloakOpenID.decode_token")
    decode_token.return_value = token_value
    mocker.patch("keycloak.KeycloakOpenID.certs")

    userinfo = mocker.patch("keycloak.KeycloakOpenID.userinfo")
    userinfo.return_value = token_value

    request = rf.request(HTTP_AUTHORIZATION="Bearer some_token")
    user, token = JSONWebTokenKeycloakAuthentication().authenticate(request)

    assert user == admin_user
    assert decode_token.return_value == token


@pytest.mark.parametrize("is_id_token", [True, False])
@pytest.mark.parametrize(
    "authentication_header,authenticated,error",
    [
        ("", False, False),
        ("Bearer", False, True),
        ("Bearer Too many params", False, True),
        ("Basic Auth", False, True),
        ("Bearer Token", True, False),
    ],
)
@pytest.mark.parametrize("user__username", ["1"])
def test_django_admin_oidc_authentication(
    db,
    user,
    rf,
    authentication_header,
    authenticated,
    error,
    is_id_token,
    requests_mock,
    settings,
    clear_cache,
):
    userinfo = {"sub": "1", "preferred_username": "1"}
    requests_mock.get(settings.OIDC_OP_USER_ENDPOINT, text=json.dumps(userinfo))

    if not is_id_token:
        userinfo = {"client_id": "test_client", "sub": "1"}
        requests_mock.get(
            settings.OIDC_OP_USER_ENDPOINT, status_code=status.HTTP_401_UNAUTHORIZED
        )
        requests_mock.post(
            settings.OIDC_OP_INTROSPECT_ENDPOINT, text=json.dumps(userinfo)
        )

    request = rf.get("/openid", HTTP_AUTHORIZATION=authentication_header)
    try:
        result = OIDCAuthentication().authenticate(request)
    except exceptions.AuthenticationFailed:
        assert error
    else:
        if result:
            user, auth = result
            assert user.is_authenticated


@pytest.mark.parametrize("side_effect", [JWTExpired(), JWException()])
def test_authenticate_side_effect(rf, mocker, side_effect, clear_cache):
    decode_token = mocker.patch("keycloak.KeycloakOpenID.decode_token")
    decode_token.side_effect = side_effect
    mocker.patch("keycloak.KeycloakOpenID.certs")

    request = rf.request(HTTP_AUTHORIZATION="Bearer some_token")
    with pytest.raises(AuthenticationFailed):
        JSONWebTokenKeycloakAuthentication().authenticate(request)


@pytest.mark.parametrize("authorization", ["Bearer", "Bearer token token"])
def test_get_jwt_value_invalid_authorization(db, rf, authorization):
    request = rf.request(HTTP_AUTHORIZATION=authorization)
    with pytest.raises(AuthenticationFailed):
        JSONWebTokenKeycloakAuthentication().get_jwt_value(request)


def test_authenticate_header(db, rf, settings):
    request = rf.request()
    header = JSONWebTokenKeycloakAuthentication().authenticate_header(request)
    assert settings.KEYCLOAK_REALM in header


def test_authenticate_applicants(
    rf, admin_user, mocker, applicant_factory, instance_factory, clear_cache, settings
):
    new_email = "test@test.ch"
    new_username = "N12345678"

    admin_user.username = new_username
    admin_user.save()

    instance1 = instance_factory()
    instance2 = instance_factory()
    instance3 = instance_factory()

    existing_applicant = applicant_factory(instance=instance1, invitee=admin_user)
    pending_obsolete_applicant = applicant_factory(
        instance=instance1, email=new_email, invitee=None
    )
    pending_email_applicant = applicant_factory(
        instance=instance2, email=new_email, invitee=None
    )
    pending_username_applicant = applicant_factory(
        instance=instance3, username=new_username, invitee=None
    )

    token_value = {
        "sub": admin_user.username,
        "email": new_email,
        "family_name": admin_user.surname,
        "given_name": admin_user.name,
        settings.OIDC_USERNAME_CLAIM: admin_user.username,
    }
    decode_token = mocker.patch("keycloak.KeycloakOpenID.decode_token")
    decode_token.return_value = token_value
    mocker.patch("keycloak.KeycloakOpenID.certs")

    userinfo = mocker.patch("keycloak.KeycloakOpenID.userinfo")
    userinfo.return_value = token_value

    request = rf.request(HTTP_AUTHORIZATION="Bearer some_token")

    JSONWebTokenKeycloakAuthentication().authenticate(request)

    existing_applicant.refresh_from_db()
    pending_email_applicant.refresh_from_db()
    pending_username_applicant.refresh_from_db()

    assert existing_applicant.invitee == admin_user
    assert pending_email_applicant.invitee == admin_user
    assert pending_username_applicant.invitee == admin_user

    with pytest.raises(Applicant.DoesNotExist):
        pending_obsolete_applicant.refresh_from_db()


@pytest.mark.parametrize(
    "user__username,expect_invitee", [("test", False), ("egov:123", True)]
)
def test_update_applicants_token_exchange(
    db, applicant_factory, expect_invitee, settings, user, clear_cache
):
    settings.ENABLE_TOKEN_EXCHANGE = True

    pending_applicant = applicant_factory(email=user.email, invitee=None)

    JSONWebTokenKeycloakAuthentication()._update_applicants(user)

    pending_applicant.refresh_from_db()

    if expect_invitee:
        assert pending_applicant.invitee == user
    else:
        assert pending_applicant.invitee is None


def test_authenticate_token_exchange_company_name(rf, mocker, settings, clear_cache):
    settings.ENABLE_TOKEN_EXCHANGE = True

    token_data = {
        "sub": "egov:2",
        "email": "test@example.com",
        "family_name": "Acme Inc.",
        # Explicitly no `given_name` in here
        settings.OIDC_USERNAME_CLAIM: "egov:2",
    }

    decode_token = mocker.patch("keycloak.KeycloakOpenID.decode_token")
    decode_token.return_value = token_data
    mocker.patch("keycloak.KeycloakOpenID.certs")

    userinfo = mocker.patch("keycloak.KeycloakOpenID.userinfo")
    userinfo.return_value = token_data

    request = rf.request(HTTP_AUTHORIZATION="Bearer some_token")
    user, _ = JSONWebTokenKeycloakAuthentication().authenticate(request)

    assert user.get_full_name() == "Acme Inc."


@pytest.mark.parametrize(
    "oidc_sync_user_attributes",
    [["language", "email", "username", "name", "surname", "phone"]],
)
@pytest.mark.parametrize(
    "existing_values,new_values,expected_update,expected_insert",
    [
        # no changes, no update
        (
            {"username": "testuser", "email": "", "language": "en"},
            {"username": "testuser", "email": ""},
            False,
            False,
        ),
        # changed email, update record
        (
            {"username": "testuser", "email": "", "language": "en"},
            {"username": "testuser", "email": "test@example.com"},
            True,
            False,
        ),
        # new record, created
        (
            None,
            {"username": "testuser", "email": "test@example.com"},
            False,
            True,
        ),
        # change name with email fallback and update username
        (
            {
                "username": "testuser",
                "email": "test@example.com",
                "name": "Before",
            },
            {
                "username": "mismatch",
                "email": "test@example.com",
                "name": "After",
            },
            True,
            False,
        ),
    ],
)
def test_authenticate_only_update_user_if_changed(
    db,
    user_factory,
    existing_values,
    new_values,
    expected_insert,
    expected_update,
    oidc_sync_user_attributes,
    settings,
):
    settings.OIDC_BOOTSTRAP_BY_EMAIL_FALLBACK = True

    if existing_values:
        user_factory(**existing_values)

    with CaptureQueriesContext(connection) as ctx:
        obj, _ = JSONWebTokenKeycloakAuthentication()._update_or_create_user(
            defaults=new_values, accept_language_header="de"
        )

        for key in oidc_sync_user_attributes:
            if key in new_values:
                assert getattr(obj, key) == new_values[key], (
                    f"Expected {key} to be {new_values[key]}, got {getattr(obj, key)}"
                )
            elif existing_values and key in existing_values:
                assert getattr(obj, key) == existing_values.get(key, None), (
                    f"Expected {key} to be {existing_values.get(key, None)}, got {getattr(obj, key)}"
                )

        has_insert = any(
            'INSERT INTO "USER" ' in query["sql"] for query in ctx.captured_queries
        )
        has_update = any(
            'UPDATE "USER" ' in query["sql"] for query in ctx.captured_queries
        )

        assert has_insert == expected_insert
        assert has_update == expected_update


@pytest.mark.parametrize(
    "oidc_sync_user_attributes",
    [["language", "email", "username", "name", "surname", "phone"]],
)
@pytest.mark.parametrize(
    "values,use_fallback,expected_fallback",
    [
        # Sync by username, no fallback
        (
            {"username": "testuser", "email": "test@example.com", "name": "New name"},
            False,
            False,
        ),
        # Sync by username, fallback enabled but not used because user found by username
        (
            {
                "username": "nonexisting",
                "email": "test@example.com",
                "name": "New name",
            },
            True,
            True,
        ),
        # Sync by email, fallback enabled and used because user not found by username
        (
            {
                "username": "testuser",
                "email": "test@example.com",
                "name": "New name",
            },
            True,
            False,
        ),
    ],
)
def test_authenticate_user_email_fallback(
    db,
    user_factory,
    values,
    use_fallback,
    expected_fallback,
    oidc_sync_user_attributes,
    settings,
):
    settings.OIDC_BOOTSTRAP_BY_EMAIL_FALLBACK = use_fallback

    user1 = user_factory(username="testuser", name="Name")
    user2 = user_factory(username="testuser2", email="test@example.com", name="Name")

    obj, _ = JSONWebTokenKeycloakAuthentication()._update_or_create_user(
        defaults=values, accept_language_header="de"
    )

    assert obj.name == values["name"]
    assert obj.username == values["username"]
    assert obj.email == values["email"]
    assert obj.pk == (user1.pk if not expected_fallback else user2.pk)
