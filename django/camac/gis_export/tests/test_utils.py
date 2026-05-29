import json

import pytest
from django.conf import settings

from camac.gis_export.models import AGGISExport, InstanceProxyAG, SOGISExport
from camac.gis_export.domain_logic import export_agis, export_so
from camac.instance.serializers import SUBMIT_DATE_FORMAT
from camac.permissions.api import PermissionManager
from camac.tests.form_utils import FormUtils


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


@pytest.mark.django_db
def test_so_gis_export(
    so_instance,
    role,
    service_factory,
    instance_acl_factory,
    instance_state_t_factory,
    access_level_factory,
    form_utils: FormUtils,
):
    service = service_factory(slug="arp-leitbehoerde")
    role.name = "service-lead"
    role.save()

    lead_authority = access_level_factory(pk="lead-authority")
    instance_acl_factory(
        instance=so_instance, service=service, access_level=lead_authority
    )

    so_instance.instance_state = instance_state_t_factory(
        instance_state__name="subm",
        name="Submitted",
    ).instance_state
    so_instance.case.meta.update({"dossier-number": "SO-2026-1", "is-bab": True})
    so_instance.case.save()
    so_instance.save()

    form_utils.add_answer(so_instance.case.document, "gemeindenummer-bfs", "2601")
    form_utils.add_table_answer(
        so_instance.case.document,
        "bauherrin",
        [
            {
                "vorname": "Max",
                "nachname": "Muster",
                "strasse": "Teststrasse",
                "strasse-nummer": "12",
                "plz": 4500,
                "ort": "Solothurn",
            }
        ],
    )
    form_utils.add_table_answer(
        so_instance.case.document,
        "parzellen",
        [
            {
                "parzellennummer": "123456",
                "e-grid": "CH123456",
                "lagekoordinaten-ost": 2690970.9,
                "lagekoordinaten-nord": 1192891.9,
            },
            {
                "parzellennummer": "789012",
                "e-grid": "CH789012",
                "lagekoordinaten-ost": 2690970.9,
                "lagekoordinaten-nord": 1192891.9,
            },
        ],
    )

    assert SOGISExport.objects.count() == 0

    export_so()

    assert SOGISExport.objects.count() == 1

    exported = SOGISExport.objects.first()
    assert exported.instance_id == so_instance.pk
    assert exported.identifikator == "SO-2026-1"
    assert exported.bfsnr == 2601
    assert exported.status == "Pruefung.formell"
    assert exported.ausserhalb_bauzone is True
    assert exported.gesuchssteller == {
        "natuerliche_person": {"name": "Muster", "vorname": "Max"},
        "juristische_person": {"name": None},
        "adresse": {
            "strassenname": "Teststrasse",
            "hausnummer": "12",
            "plz": "4500",
            "ortschaft": "Solothurn",
        },
    }
    assert exported.geometrie_punkt == {"ost": "2690970.9", "nord": "1192891.9"}
    assert exported.ebau_link == f"{settings.INTERNAL_BASE_URL}/cases/{so_instance.pk}"
    assert sorted(exported.grundstuecke, key=lambda plot: plot["nummer"]) == [
        {"nummer": "123456", "egrid": "CH123456"},
        {"nummer": "789012", "egrid": "CH789012"},
    ]
    assert exported.hash


@pytest.mark.django_db
def test_export_so_detects_changes(
    so_instance,
    role,
    service_factory,
    instance_acl_factory,
    instance_state_t_factory,
    access_level_factory,
    form_utils: FormUtils,
):
    service = service_factory(slug="arp-leitbehoerde")
    role.name = "service-lead"
    role.save()

    lead_authority = access_level_factory(pk="lead-authority")
    instance_acl_factory(
        instance=so_instance, service=service, access_level=lead_authority
    )

    so_instance.instance_state = instance_state_t_factory(
        instance_state__name="subm",
        name="Submitted",
    ).instance_state
    so_instance.case.meta.update({"dossier-number": "SO-2026-1"})
    so_instance.case.save()
    so_instance.save()

    form_utils.add_answer(so_instance.case.document, "gemeindenummer-bfs", "2601")

    # Create: a brand new instance is exported.
    export_so()
    assert SOGISExport.objects.count() == 1
    export = SOGISExport.objects.get()
    original_hash = export.hash
    original_modified_at = export.modified_at

    # No change: nothing is updated, hash and modified_at stay stable (this is
    # what makes the deterministic hash and the diff pass worthwhile).
    export_so()
    assert SOGISExport.objects.count() == 1
    export.refresh_from_db()
    assert export.hash == original_hash
    assert export.modified_at == original_modified_at

    # Change a hashed field: the export row is detected and updated.
    so_instance.case.document.answers.filter(question_id="gemeindenummer-bfs").delete()
    form_utils.add_answer(so_instance.case.document, "gemeindenummer-bfs", "2602")

    export_so()
    assert SOGISExport.objects.count() == 1
    export.refresh_from_db()
    assert export.hash != original_hash
    assert export.bfsnr == 2602
