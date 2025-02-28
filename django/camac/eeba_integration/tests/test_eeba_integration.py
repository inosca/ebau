import pytest
from django.urls import reverse
from pytest_lazy_fixtures import lf
from rest_framework import status


@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
@pytest.mark.parametrize(
    "canton_name,master_data_case,shared_secret,expected_status",
    [
        (
            "kt_gr",
            lf("gr_master_data_case"),
            "shared_secret",
            status.HTTP_200_OK,
        ),
        (
            "kt_gr",
            lf("gr_master_data_case"),
            "",
            status.HTTP_403_FORBIDDEN,
        ),
        (
            "kt_so",
            lf("so_master_data_case"),
            "shared_secret",
            status.HTTP_403_FORBIDDEN,
        ),
    ],
)
def test_eeba_export(
    admin_client,
    instance,
    canton_name,
    master_data_case,
    shared_secret,
    expected_status,
    set_application_gr,
    settings,
    application_settings,
    snapshot,
):
    settings.APPLICATION_NAME = canton_name
    settings.EEBA_SHARED_SECRET = "shared_secret"

    headers = {"X-EBAU-EEBA-SECRET": shared_secret}
    url = reverse("instance-eeba-export", args=[instance.pk])

    response = admin_client.get(url, headers=headers)

    assert response.status_code == expected_status

    json_response = response.json()

    # Check instance pk separately as it will vary from test to test and can't be tested via snapshot
    if instance_pk := json_response.get("ebauId"):
        assert instance_pk == master_data_case.instance.pk
        json_response["ebauId"] = "INSTANCE_ID"

    snapshot.assert_match(json_response)
