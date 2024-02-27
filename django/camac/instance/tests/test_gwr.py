import pytest
from django.urls import reverse
from pytest_lazyfixture import lazy_fixture
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
            lazy_fixture("ur_master_data_case_gwr"),
        ),
        (
            "kt_gr",
            lazy_fixture("gr_master_data_case"),
        ),
        (
            "kt_schwyz",
            lazy_fixture("sz_master_data_case_gwr"),
        ),
        (
            "kt_schwyz",
            lazy_fixture("sz_master_data_case_gwr_v2"),
        ),
        (
            "kt_so",
            lazy_fixture("so_master_data_case"),
        ),
    ],
)
@pytest.mark.freeze_time("2021-10-07")
def test_gwr_data(
    admin_client,
    canton_name,
    master_data_case,
    settings,
    snapshot,
):
    settings.APPLICATION_NAME = canton_name
    settings.APPLICATION["SHORT_NAME"] = settings.APPLICATIONS[canton_name][
        "SHORT_NAME"
    ]

    url = reverse("instance-gwr-data", args=[master_data_case.instance.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    snapshot.assert_match(response.json())
