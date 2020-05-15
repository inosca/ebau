"""
The tests in this module cover the migration logic required to migrate
Kanton Uri's identity management from camac to keycloak.
"""
import pytest
from django.core.cache import cache
from jose.exceptions import ExpiredSignatureError, JOSEError
from rest_framework.exceptions import AuthenticationFailed

from camac.user.authentication import JSONWebTokenKeycloakAuthentication

from ..models import User

def test_authenticate_bootstrap_by_mail(
    rf,
    mocker,
    application_settings,
    user_factory
):
    token_value = {
        "sub": "existing-already",
        "email": "existing-guy@example.com",
        "family_name": "Existing",
        "given_name": "Guy",
    }

    # The user with the same email should be updated with keycloak information
    user_factory(email=token_value['email'])

    application_settings['OIDC_BOOTSTRAP_BY_EMAIL'] = True

    decode_token = mocker.patch("keycloak.KeycloakOpenID.decode_token")
    decode_token.return_value = token_value
    mocker.patch("keycloak.KeycloakOpenID.certs")

    userinfo = mocker.patch("keycloak.KeycloakOpenID.userinfo")
    userinfo.return_value = token_value

    request = rf.request(HTTP_AUTHORIZATION="Bearer some_token")
    _, token = JSONWebTokenKeycloakAuthentication().authenticate(request)

    user.refresh_from_db()

    assert user.username == token['sub']
    assert user.name == token['family_name']
    assert user.surname == token['given_name']
    assert user.groups.count() == 0
    assert decode_token.return_value == token


def test_migrate_portal_user(
    rf,
    mocker,
    settings,
    application_settings,
    instance_portal_factory,
    instance_factory,
    group_factory
):
    """When an existing applicant logs in for the first time via keycloak all their
    instances should be transfered from the portal user to their newly created
    camac user stub.
    """


    application_settings['URI_MIGRATE_PORTAL_USER'] = True

    applicant_group = group_factory()
    application_settings['APPLICANT_GROUP_ID'] = applicant_group.pk

    iweb_profile_id = "d12_1023"
    username = "somelongid"

    instance = instance_factory()
    instance_portal = instance_portal_factory(instance_id=instance.pk, portal_identifier=iweb_profile_id)

    # TODO(patrickw): Revisit this and add additionally required attributes once
    # we knew the attribute mapping of the iweb idp.
    token_value = {
        "sub": username,
        "preferred_username": iweb_profile_id,
        "email": "other-guy@example.com",
        "family_name": "Other",
        "given_name": "Guy",
    }

    decode_token = mocker.patch("keycloak.KeycloakOpenID.decode_token")
    decode_token.return_value = token_value
    mocker.patch("keycloak.KeycloakOpenID.certs")

    userinfo = mocker.patch("keycloak.KeycloakOpenID.userinfo")
    userinfo.return_value = token_value

    request = rf.request(HTTP_AUTHORIZATION="Bearer some_token")
    user, token = JSONWebTokenKeycloakAuthentication().authenticate(request)

    instance.refresh_from_db()
    instance_portal.refresh_from_db()

    # Ensure that the user is now owner of his submitted instances
    assert instance.user == user
    assert instance_portal.migrated == True

    # Ensure the user object attrubtes were updated
    assert user.username == token['sub']
    assert user.name == token['family_name']
    assert user.surname == token['given_name']

    # Ensure that the user was added to the applicant group
    groups = user.groups.all()
    assert len(groups)  == 1
    assert groups[0] == applicant_group
