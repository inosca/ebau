import pytest
from django.conf import settings
from django.urls import reverse

from camac.gis_export.models import SOGISExport


@pytest.mark.django_db
def test_export_so_gis_view(
    admin_client,
    admin_user,
    so_instance,
    role,
    service_factory,
    instance_acl_factory,
    instance_state_t_factory,
    access_level_factory,
    form_utils,
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
                "nachname": "Muster",
                "vorname": "Max",
                "strasse": "Teststrasse",
                "strasse-nummer": "1",
                "plz": "4500",
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
            }
        ],
    )

    assert SOGISExport.objects.count() == 0

    admin_client.force_authenticate(
        user=admin_user, token={"azp": settings.GIS_EXPORT.keycloak_client}
    )

    response = admin_client.get(reverse("so-gis-export"))

    assert response.status_code == 200
    assert response["Content-Type"] == "application/xml"
    assert response["Content-Disposition"] == 'inline; filename="so_gis_export.xtf"'

    # exported_at is set by the after-stream hook, i.e. only once the body is
    # fully consumed below — not before.
    assert SOGISExport.objects.get().exported_at is None

    content = b"".join(response.streaming_content).decode()
    assert "<transfer />" not in content
    assert "<ili:transfer" in content
    assert "<ili:datasection>" in content
    assert (
        "<SO_DSBJD_eBauSO_Geschaefte_20250422:Identifikator>SO-2026-1</SO_DSBJD_eBauSO_Geschaefte_20250422:Identifikator>"
        in content
    )
    assert (
        "<SO_DSBJD_eBauSO_Geschaefte_20250422:BFSNr>2601</SO_DSBJD_eBauSO_Geschaefte_20250422:BFSNr>"
        in content
    )
    assert (
        "<SO_DSBJD_eBauSO_Geschaefte_20250422:Status>Pruefung.formell</SO_DSBJD_eBauSO_Geschaefte_20250422:Status>"
        in content
    )
    assert (
        "<SO_DSBJD_eBauSO_Geschaefte_20250422:ausserhalb_Bauzone>true</SO_DSBJD_eBauSO_Geschaefte_20250422:ausserhalb_Bauzone>"
        in content
    )

    assert SOGISExport.objects.count() == 1
    # After the full body streamed, the row is marked delivered.
    assert SOGISExport.objects.get().exported_at is not None


@pytest.mark.django_db
def test_export_sogis_view_returns_no_content(monkeypatch):
    from camac.gis_export.views import ExportSOGISView

    monkeypatch.setattr("camac.gis_export.views.export_so", lambda: None)
    monkeypatch.setattr("camac.gis_export.views.export_sogis_xml", lambda exports: None)

    response = ExportSOGISView().get(None)

    assert response.status_code == 204


def test_is_sogis_client_token_handles_missing_auth():
    from types import SimpleNamespace

    from camac.user.permissions import IsSogisClientToken

    request = SimpleNamespace(auth=None)

    assert IsSogisClientToken().has_permission(request, None) is False
