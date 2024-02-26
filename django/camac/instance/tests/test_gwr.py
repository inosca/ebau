import pytest
from django.urls import reverse
from pytest_lazyfixture import lazy_fixture
from rest_framework import status

from camac.instance.tests.test_master_data import (
    gr_master_data_case,  # noqa
    sz_master_data_case_gwr,  # noqa
    sz_master_data_case_gwr_v2,  # noqa
)


@pytest.mark.parametrize(
    "canton_name,canton_short_name,instance_for,master_data_case",
    [
        (
            "kt_so",
            "so",
            lazy_fixture("so_instance"),
            lazy_fixture("so_master_data_case"),
        ),
        (
            "kt_uri",
            "ur",
            lazy_fixture("ur_instance"),
            lazy_fixture("ur_master_data_case"),
        ),
        (
            "kt_gr",
            "gr",
            lazy_fixture("gr_instance"),
            lazy_fixture("gr_master_data_case"),
        ),
        (
            "kt_schwyz",
            "sz",
            lazy_fixture("sz_instance"),
            lazy_fixture("sz_master_data_case_gwr"),
        ),
        (
            "kt_schwyz",
            "sz",
            lazy_fixture("sz_instance"),
            lazy_fixture("sz_master_data_case_gwr_v2"),
        ),
    ],
)
@pytest.mark.freeze_time("2021-10-07")
def test_gwr_data(
    admin_client,
    user,
    instance,
    instance_for,
    canton_name,
    canton_short_name,
    use_caluma_form,
    caluma_admin_user,
    application_settings,
    master_data_case,
    settings,
    workflow_entry_factory,
    snapshot,
    utils,
):
    settings.APPLICATION_NAME = canton_name
    settings.APPLICATION["SHORT_NAME"] = canton_short_name

    if canton_name in ["kt_uri", "kt_so"]:
        instance_for.case.meta = {"dossier-number": "1201-21-003"}
        instance_for.case.save()

        document = instance_for.case.document

        # Completed date
        # Assert that workflow entry of last group (phase) is selected
        workflow_entry = next(
            filter(
                lambda entry: entry.workflow_item_id == 67,
                instance_for.workflowentry_set.all(),
            ),
            None,
        )

        workflow_entry_factory(
            instance=instance_for,
            workflow_date="2021-08-05 08:00:06+00",
            group=2,
            workflow_item=workflow_entry.workflow_item,
        )

        # Energy devices
        # Check logic for heating / warmwater devices and
        # primary / secondary devices
        table_answer = document.answers.filter(
            question_id="haustechnik-tabelle"
        ).first()
        utils.add_table_answer(
            document,
            "haustechnik-tabelle",
            [
                {
                    "gehoert-zu-gebaeudenummer": "Villa",
                    "anlagetyp": "anlagetyp-warmwasser",
                    "heizsystem-art": "-zusatzheizung",
                    "hauptheizungsanlage": "hauptheizungsanlage-gas",
                }
            ],
            table_answer,
        )

    url = reverse("instance-gwr-data", args=[instance.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    snapshot.assert_match(response.json())
