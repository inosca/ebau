import re

import pytest
from django.urls import reverse

from camac.gis_export.models import SOGISExport
from camac.gis_export.so_schema import (
    INTERLIS,
    SO_DSBJD_eBauSO_Geschaefte_20250422 as so_schema,
)

MODEL_TAG = re.compile(r"<ns\d+:(\w+)")

# Point, line and polygon are a mutually exclusive choice: a Geschaeft carries
# exactly one of them.
GEOMETRY_VARIANTS = {"Geometrie_Punkt", "Geometrie_Linie", "Geometrie_Flaeche"}

DRAWN_POINT = {
    "markers": [{"x": 2607000.5, "y": 1228500.5}],
    "geometry": "POINT",
}
DRAWN_LINE = {
    "markers": [{"x": 2607000.5, "y": 1228500.5}, {"x": 2607100.5, "y": 1228600.5}],
    "geometry": "LINESTRING",
}
DRAWN_POLYGON = {
    "markers": [
        {"x": 2607000.5, "y": 1228500.5},
        {"x": 2607100.5, "y": 1228500.5},
        {"x": 2607100.5, "y": 1228600.5},
    ],
    "geometry": "POLYGON",
}


def _export(sogis_client):
    """Run the endpoint and return the streamed XTF."""
    response = sogis_client.get(reverse("so-gis-export"))

    assert response.status_code == 200
    assert response["Content-Type"] == "application/xml"
    assert response["Content-Disposition"] == 'inline; filename="so_gis_export.xtf"'

    xml = b"".join(response.streaming_content).decode()

    # PyXB validates against the generated schema while parsing.
    INTERLIS.CreateFromDocument(xml.encode("utf-8"))

    return xml


@pytest.mark.django_db
def test_export_two_minimal_instances(
    sogis_client, instance_factory, instance_with_case, setup_so_instance, snapshot
):
    """Only the attributes the .ili marks MANDATORY are answered."""
    for number in ("2601-2026-1", "2601-2026-2"):
        setup_so_instance(instance_with_case(instance_factory()), number)

    xml = _export(sogis_client)

    assert xml.count("<ns2:Geschaeft ") == 2
    assert SOGISExport.objects.count() == 2

    for absent in ("Bauprojekt", "Lokalisation", "Publikation", "Zirkulation"):
        assert f"<ns2:{absent}>" not in xml

    snapshot.assert_match(sorted(set(MODEL_TAG.findall(xml))))


@pytest.mark.django_db
def test_export_two_full_instances(
    sogis_client, instance_factory, instance_with_case, setup_so_instance, snapshot
):
    """Every attribute that has a Caluma source is answered."""
    # `gis-karte` is a Caluma source too, so a full dossier draws a geometry.
    for number in ("2601-2026-1", "2601-2026-2"):
        setup_so_instance(
            instance_with_case(instance_factory()),
            number,
            full=True,
            parcels=2,
            gis_karte=DRAWN_POLYGON,
        )

    xml = _export(sogis_client)
    emitted = set(MODEL_TAG.findall(xml))

    assert xml.count("<ns2:Geschaeft ") == 2
    # Two parcels per dossier, one wrapper element each.
    assert xml.count("<ns2:Grundstuecke>") == 4

    # A snapshot cannot see an attribute the regenerated bindings added but
    # nobody mapped, because the output simply stays the same. Compare
    # against the schema instead. The geometry variants are excluded: they are a
    # mutually exclusive choice covered by test_export_emits_only_the_drawn_geometry.
    declared = {name.localName() for name in so_schema.GeschaeftType._ElementMap}
    assert declared - GEOMETRY_VARIANTS - emitted == set()
    assert emitted & GEOMETRY_VARIANTS == {"Geometrie_Flaeche"}

    snapshot.assert_match(sorted(emitted))


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("gis_karte", "expected"),
    [
        (None, "Geometrie_Punkt"),  # no map answer: the plot-table fallback
        (DRAWN_POINT, "Geometrie_Punkt"),
        (DRAWN_LINE, "Geometrie_Linie"),
        (DRAWN_POLYGON, "Geometrie_Flaeche"),
    ],
)
def test_export_emits_only_the_drawn_geometry(
    sogis_client,
    instance_factory,
    instance_with_case,
    setup_so_instance,
    gis_karte,
    expected,
):
    """A dossier carries exactly one of point, line or polygon, never several."""
    setup_so_instance(
        instance_with_case(instance_factory()), "2601-2026-1", gis_karte=gis_karte
    )

    emitted = set(MODEL_TAG.findall(_export(sogis_client)))

    assert emitted & GEOMETRY_VARIANTS == {expected}


@pytest.mark.django_db
def test_export_reports_invalid_dossiers_but_delivers_the_valid_ones(
    sogis_client,
    instance_factory,
    instance_with_case,
    setup_so_instance,
    form_utils,
    caplog,
):
    """Each way a dossier is invalid is reported and kept pending; valid ones ship."""
    valid = instance_with_case(instance_factory())
    setup_so_instance(valid, "2601-2026-0")

    missing_applicant = instance_with_case(instance_factory())
    setup_so_instance(missing_applicant, "2601-2026-1")
    # Gesuchsteller is MANDATORY in the .ili - a schema rule only PyXB catches.
    missing_applicant.case.document.answers.filter(question_id="bauherrin").delete()

    no_geometry = instance_with_case(instance_factory())
    setup_so_instance(no_geometry, "2601-2026-2")
    # No parcels leaves no coordinates, violating the geometry constraint _validate
    # enforces before serialization.
    no_geometry.case.document.answers.filter(question_id="parzellen").delete()

    bad_bfsnr = instance_with_case(instance_factory())
    setup_so_instance(bad_bfsnr, "2601-2026-3")
    # BFSNr is a 0..9999 range the XSD enforces as a facet.
    document = bad_bfsnr.case.document
    document.answers.filter(question_id="gemeindenummer-bfs").delete()
    form_utils.add_answer(document, "gemeindenummer-bfs", 99999)

    xml = _export(sogis_client)

    assert xml.count("<ns2:Geschaeft ") == 1  # only the valid dossier is delivered

    # One ERROR record (so it reaches mail_admins) lists every skipped dossier.
    errors = [record for record in caplog.records if record.levelname == "ERROR"]
    assert len(errors) == 1
    message = errors[0].getMessage()
    assert "Gesuchsteller" in message
    assert "no usable geometry" in message
    assert "BFSNr does not accept 99999" in message

    assert SOGISExport.objects.get(identifikator="2601-2026-0").exported_at is not None
    # The three invalid dossiers stay pending for the next run.
    assert SOGISExport.objects.pending().count() == 3


@pytest.mark.django_db
def test_delivered_export_is_not_sent_again(
    sogis_client, instance_factory, instance_with_case, setup_so_instance
):
    setup_so_instance(instance_with_case(instance_factory()), "2601-2026-1", full=True)

    _export(sogis_client)

    assert SOGISExport.objects.get().exported_at is not None
    assert sogis_client.get(reverse("so-gis-export")).status_code == 204


@pytest.mark.django_db
def test_export_without_pending_dossiers_returns_no_content(sogis_client):
    assert not SOGISExport.objects.exists()

    assert sogis_client.get(reverse("so-gis-export")).status_code == 204


@pytest.mark.django_db
def test_a_delivered_export_that_turns_invalid_stays_pending(
    sogis_client, instance_factory, instance_with_case, setup_so_instance
):
    """A skipped retry that kept its old `exported_at` would vanish silently."""
    instance = setup_so_instance(
        instance_with_case(instance_factory()), "2601-2026-1", full=True
    )

    _export(sogis_client)

    delivered_at = SOGISExport.objects.get().exported_at
    assert delivered_at is not None
    assert not SOGISExport.objects.pending().exists()

    instance.case.document.answers.filter(question_id="bauherrin").delete()

    assert sogis_client.get(reverse("so-gis-export")).status_code == 204

    export = SOGISExport.objects.get()
    assert export.exported_at == delivered_at
    assert export.modified_at > export.exported_at
    assert list(SOGISExport.objects.pending()) == [export]


@pytest.mark.django_db
def test_export_rejects_a_request_without_the_sogis_client_token(
    admin_client, admin_user
):
    admin_client.force_authenticate(user=admin_user, token=None)

    response = admin_client.get(reverse("so-gis-export"))

    assert response.status_code == 403


@pytest.mark.django_db
def test_export_is_not_found_when_the_module_is_disabled(
    admin_client, admin_user, disable_gis_export_settings
):
    admin_client.force_authenticate(
        user=admin_user, token={"azp": disable_gis_export_settings.keycloak_client}
    )

    response = admin_client.get(reverse("so-gis-export"))

    assert response.status_code == 404
