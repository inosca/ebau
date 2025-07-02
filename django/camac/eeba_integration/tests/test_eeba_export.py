import pytest
from django.conf import settings
from django.urls import reverse
from pytest_lazy_fixtures import lf
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
@pytest.mark.parametrize(
    "canton_name,master_data_case,shared_secret,scope,expected_status",
    [
        (
            "kt_gr",
            lf("gr_master_data_case"),
            "shared_secret",
            "eeba-export",
            status.HTTP_200_OK,
        ),
        (
            "kt_gr",
            lf("gr_master_data_case"),
            "shared_secret",
            "",
            status.HTTP_403_FORBIDDEN,
        ),
        (
            "kt_gr",
            lf("gr_master_data_case"),
            "",
            "eeba-export",
            status.HTTP_403_FORBIDDEN,
        ),
        (
            "kt_so",
            lf("so_master_data_case"),
            "shared_secret",
            "eeba-export",
            status.HTTP_403_FORBIDDEN,
        ),
    ],
)
def test_eeba_export(
    db,
    instance,
    canton_name,
    master_data_case,
    shared_secret,
    scope,
    expected_status,
    set_application_gr,
    gr_eeba_integration_settings,
    snapshot,
):
    settings.APPLICATION_NAME = canton_name
    gr_eeba_integration_settings["EEBA_SHARED_SECRET"] = "shared_secret"

    client = APIClient()

    if scope:
        client.force_authenticate(user=instance.user, token={"scope": scope})
    else:
        client.force_authenticate(user=instance.user, token={})

    extra = {}
    if shared_secret:
        extra["HTTP_X_EBAU_EEBA_SECRET"] = shared_secret

    url = reverse("instance-eeba-export", args=[instance.pk])

    response = client.get(url, **extra)

    assert response.status_code == expected_status

    data = response.json()

    # Check instance pk separately as it will vary from test to test and can't be tested via snapshot
    if expected_status == status.HTTP_200_OK:
        assert data["ebauId"] == master_data_case.instance.pk
        data["ebauId"] = "INSTANCE_ID"

    snapshot.assert_match(data)
