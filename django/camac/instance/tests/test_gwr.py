import pytest
from django.urls import reverse
from rest_framework import status

from camac.conftest import sz_master_data_case  # noqa
from camac.instance.tests.test_master_data import sz_master_data_case_gwr  # noqa
from camac.instance.tests.test_master_data import sz_master_data_case_gwr_v2  # noqa
from camac.instance.tests.test_master_data import ur_master_data_case  # noqa
from camac.instance.tests.test_master_data import add_table_answer


@pytest.mark.freeze_time("2021-10-07")
def test_gwr_data_ur(
    admin_client,
    user,
    instance,
    use_caluma_form,
    ur_instance,
    caluma_forms_ur,
    caluma_admin_user,
    application_settings,
    settings,
    workflow_entry_factory,
    snapshot,
    ur_master_data_case,  # noqa
    ur_master_data_settings,
):
    settings.APPLICATION_NAME = "kt_uri"

    ur_instance.case.meta = {"dossier-number": "1201-21-003"}
    ur_instance.case.save()

    document = ur_instance.case.document

    # Completed date
    # Assert that workflow entry of last group (phase) is selected
    workflow_entry = next(
        filter(
            lambda entry: entry.workflow_item_id == 67,
            ur_instance.workflowentry_set.all(),
        ),
        None,
    )

    workflow_entry_factory(
        instance=ur_instance,
        workflow_date="2021-08-05 08:00:06+00",
        group=2,
        workflow_item=workflow_entry.workflow_item,
    )

    # Energy devices
    # Check logic for heating / warmwater devices and
    # primary / secondary devices
    table_answer = document.answers.filter(question_id="haustechnik-tabelle").first()
    add_table_answer(
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


def test_instance_gwr_data_sz_gwr(
    admin_client,
    user,
    sz_instance,
    application_settings,
    settings,
    snapshot,
    sz_master_data_case_gwr,  # noqa
    sz_master_data_settings,
):
    settings.APPLICATION_NAME = "kt_schwyz"

    url = reverse("instance-gwr-data", args=[sz_instance.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    snapshot.assert_match(response.json())


def test_instance_gwr_data_sz_gwr_v2(
    admin_client,
    user,
    sz_instance,
    application_settings,
    settings,
    snapshot,
    sz_master_data_case_gwr_v2,  # noqa
    sz_master_data_settings,
):
    settings.APPLICATION_NAME = "kt_schwyz"

    url = reverse("instance-gwr-data", args=[sz_instance.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    snapshot.assert_match(response.json())
