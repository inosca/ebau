import json
from datetime import date

import pytest
from caluma.caluma_form.factories import DocumentFactory
from caluma.caluma_workflow.factories import WorkItemFactory
from django.conf import settings
from django.urls import reverse
from rest_framework import status

from .test_master_data import add_answer, be_master_data_case  # noqa


@pytest.mark.freeze_time("2021-08-30")
@pytest.mark.parametrize("role__name", ["Municipality"])
def test_dms_placeholders(
    db,
    activation_factory,
    admin_client,
    application_settings,
    be_instance,
    be_master_data_case,  # noqa
    billing_v2_entry_factory,
    docx_decision_factory,
    group,
    instance_service,
    multilang,
    notice_factory,
    responsible_service_factory,
    service_factory,
    snapshot,
    tag_factory,
):
    application_settings["MASTER_DATA"] = settings.APPLICATIONS["kt_bern"][
        "MASTER_DATA"
    ]

    # publication
    document = DocumentFactory()

    add_answer(document, "publikation-anzeiger-von", "Bärnerblatt")
    add_answer(document, "publikation-text", "Text")
    add_answer(
        document,
        "publikation-1-publikation-anzeiger",
        date(2021, 8, 30),
        value_key="date",
    )
    add_answer(
        document,
        "publikation-2-publikation-anzeiger",
        date(2021, 8, 20),
        value_key="date",
    )
    add_answer(
        document,
        "publikation-amtsblatt",
        date(2021, 8, 10),
        value_key="date",
    )
    add_answer(
        document,
        "publikation-startdatum",
        date(2021, 9, 1),
        value_key="date",
    )
    add_answer(
        document,
        "publikation-ablaufdatum",
        date(2021, 9, 15),
        value_key="date",
    )

    WorkItemFactory(
        case=be_instance.case,
        task_id="fill-publication",
        document=document,
    )

    municipality = service_factory()
    be_master_data_case.document.answers.filter(question_id="gemeinde").update(
        value=str(municipality.pk)
    )
    be_master_data_case.document.dynamicoption_set.update(slug=str(municipality.pk))

    activation_factory.create_batch(
        2, service__service_group__name="district", circulation__instance=be_instance
    )
    activation_factory.create_batch(
        2,
        service__service_group__name="municipality",
        circulation__instance=be_instance,
    )
    activations = activation_factory.create_batch(
        2,
        service__service_group__name="service",
        circulation_state__name="DONE",
        circulation__instance=be_instance,
    )

    for activation in activations:
        notice_factory(activation=activation, notice_type_id=1)
        notice_factory(activation=activation, notice_type_id=20000)

    activations[0].service = group.service
    activations[0].save()

    tag_factory.create_batch(5, service=group.service, instance=be_instance)
    responsible_service_factory(instance=be_instance, service=group.service)
    docx_decision_factory(
        instance=be_instance,
        decision="positive",
        decision_type="GESAMT",
        decision_date=date(2021, 8, 30),
    )
    billing_v2_entry_factory.create_batch(2, instance=be_instance)
    billing_v2_entry_factory.create_batch(2, instance=be_instance, group=group)

    url = reverse("instance-dms-placeholders", args=[be_instance.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    snapshot.assert_match(
        json.loads(json.dumps(response.json()).replace(str(be_instance.pk), "9999"))
    )
