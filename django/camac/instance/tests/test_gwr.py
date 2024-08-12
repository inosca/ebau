import pytest
from django.urls import reverse
from pytest_lazy_fixtures import lf
from rest_framework import status

from camac.instance.tests.test_master_data import (
    gr_master_data_case,  # noqa
    so_master_data_case,  # noqa
    sz_master_data_case_gwr,  # noqa
    sz_master_data_case_gwr_v2,  # noqa
    ur_master_data_case_gwr,  # noqa
)


@pytest.mark.parametrize(
    "canton_name,master_data_case",
    [
        (
            "kt_uri",
            lf("ur_master_data_case_gwr"),
        ),
        (
            "kt_gr",
            lf("gr_master_data_case"),
        ),
        (
            "kt_schwyz",
            lf("sz_master_data_case_gwr"),
        ),
        (
            "kt_schwyz",
            lf("sz_master_data_case_gwr_v2"),
        ),
        (
            "kt_so",
            lf("so_master_data_case"),
        ),
    ],
)
@pytest.mark.freeze_time("2021-10-07")
def test_gwr_data(
    admin_client,
    canton_name,
    master_data_case,
    settings,
    application_settings,
    snapshot,
):
    settings.APPLICATION_NAME = canton_name
    application_settings["SHORT_NAME"] = settings.APPLICATIONS[canton_name][
        "SHORT_NAME"
    ]

    url = reverse("instance-gwr-data", args=[master_data_case.instance.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    snapshot.assert_match(response.json())
