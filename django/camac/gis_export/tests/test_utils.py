import json

import pytest
from django.conf import settings

from camac.instance.serializers import SUBMIT_DATE_FORMAT
from camac.permissions.api import PermissionManager
from camac.tests.form_utils import FormUtils

from ..models import AGGISExport, InstanceProxyAG
from ..utils import export_agis


@pytest.mark.freeze_time("2025-08-5 11:49:15+02:00")
@pytest.mark.django_db
def test_agis_export(
    ag_instance,
    instance_with_case,
    role,
    service_factory,
    instance_acl_factory,
    instance_state_t_factory,
    caluma_workflow_factory,
    caluma_form_factory,
    caluma_dynamic_option_factory,
    snapshot,
    form_utils: FormUtils,
    freezer,
    admin_client,
    responsible_service_factory,
):
    # AfB service data and access
    afb_service = service_factory(slug="afb")
    role.name = "trusted-service-lead"
    role.save()
    instance_acl = instance_acl_factory(instance=ag_instance, service=afb_service)
    responsible_service_factory(
        instance=ag_instance,
        service=afb_service,
        responsible_user=admin_client.user,
    )

    # Instance data
    ag_instance.instance_state = instance_state_t_factory(
        name="Submitted"
    ).instance_state
    ag_instance.case.meta.update(
        {
            "submit-date": ag_instance.creation_date.strftime(SUBMIT_DATE_FORMAT),
            "dossier-number": "2025-08",
        }
    )
    ag_instance.case.save()
    ag_instance.save()

    # Form data
    document = ag_instance.case.document
    form_utils.add_answer(document, "beschreibung-bauvorhaben", "Test Vorhaben")
    municipality = service_factory(service_group__name="municipality")
    form_utils.add_answer(document, "gemeinde", str(municipality.pk))
    caluma_dynamic_option_factory(
        slug=str(municipality.pk),
        label="Test Municipality",
        question_id="gemeinde",
        document=document,
    )
    form_utils.add_table_answer(
        document,
        "parzelle",
        [{"parzellennummer": "1338", "e-grid-nr": "CH270677774577"}],
    )
    form_utils.add_answer(
        document,
        "gis-map",
        json.dumps({"markers": [{"x": 2641234.1234, "y": 1245670.121212}]}),
    )
    form_utils.add_table_answer(
        document,
        "personalien-gesuchstellerin",
        [
            {
                "name-gesuchstellerin": "Nachname",
                "vorname-gesuchstellerin": "Vorname",
                "juristische-person-gesuchstellerin": "juristische-person-gesuchstellerin-nein",
                "name-juristische-person-gesuchstellerin": None,
            }
        ],
    )

    assert AGGISExport.objects.count() == 0

    # Create missing export for instance
    export_agis()

    assert AGGISExport.objects.count() == 1
    exported = AGGISExport.objects.first()

    fields = InstanceProxyAG.fields.copy()
    fields.remove("instance_id")
    fields.remove("url")

    snapshot.assert_match(AGGISExport.objects.values(*fields))
    assert exported.instance_id == ag_instance.pk
    assert exported.url == f"{settings.INTERNAL_BASE_URL}/cases/{ag_instance.pk}"

    # No changes to export table
    export_agis()

    assert AGGISExport.objects.count() == 1
    exported = AGGISExport.objects.first()

    snapshot.assert_match(AGGISExport.objects.values(*fields))
    assert exported.instance_id == ag_instance.pk
    assert exported.url == f"{settings.INTERNAL_BASE_URL}/cases/{ag_instance.pk}"

    # Update existing export entry for instance
    ag_instance.instance_state = instance_state_t_factory(
        name="In circulation"
    ).instance_state
    ag_instance.save()

    document.answers.filter(question_id="personalien-gesuchstellerin").delete()
    form_utils.add_table_answer(
        document,
        "personalien-gesuchstellerin",
        [
            {
                "name-gesuchstellerin": "Nachname",
                "vorname-gesuchstellerin": "Vorname",
                "juristische-person-gesuchstellerin": "juristische-person-gesuchstellerin-ja",
                "name-juristische-person-gesuchstellerin": "Firma Test",
            }
        ],
    )

    export_agis()

    assert AGGISExport.objects.count() == 1
    exported = AGGISExport.objects.first()

    snapshot.assert_match(AGGISExport.objects.values(*fields))
    assert exported.instance_id == ag_instance.pk
    assert exported.url == f"{settings.INTERNAL_BASE_URL}/cases/{ag_instance.pk}"

    # Remove export entry for deleted instance
    manager = PermissionManager.for_anonymous()
    manager.revoke(instance_acl)

    export_agis()

    assert AGGISExport.objects.count() == 0
