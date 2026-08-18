import json

import pytest
from django.conf import settings
from django.utils.timezone import now

from camac.gis_export.models import SOGISExport
from camac.tests.data import so_personal_row_factory


@pytest.mark.django_db
def test_sync_annotates_every_field(
    instance_factory, instance_with_case, setup_so_instance
):
    """The annotations are what the formatter builds on, so assert them here."""
    instance = setup_so_instance(
        instance_with_case(instance_factory()), "2601-2026-1", full=True, parcels=2
    )

    SOGISExport.objects.sync()

    export = SOGISExport.objects.get()

    assert export.instance_id == instance.pk
    assert export.identifikator == "2601-2026-1"
    assert export.bfsnr == 2601
    # The raw instance state is stored; formatters._map_status maps it to the enum.
    assert export.status == "subm"
    assert export.ausserhalb_bauzone is True
    assert export.ebau_link == f"{settings.INTERNAL_BASE_URL}/cases/{instance.pk}"
    assert export.hash

    # Gesuchsteller is a BAG {1..*}: both bauherrin rows map, each carrying its
    # applicant under `adresse` and its optional representation under `vertretung`.
    assert len(export.gesuchsteller) == 2
    assert all(e["adresse"]["natuerliche_person"]["name"] for e in export.gesuchsteller)
    assert all(e["adresse"]["adresse"]["ortschaft"] for e in export.gesuchsteller)
    vertretungen = [e["vertretung"] for e in export.gesuchsteller]
    assert sum(v is not None for v in vertretungen) == 1  # one row has_representation
    represented = next(v for v in vertretungen if v is not None)
    assert represented["natuerliche_person"]["name"]
    assert export.plot_point == {"ost": "2607000.5", "nord": "1228500.5"}
    assert sorted(plot["nummer"] for plot in export.grundstuecke) == ["1234", "1235"]
    assert export.bauprojekt["beschreibung"] == "Neubau Mehrfamilienhaus"
    assert export.bauprojekt["bauwerk_art"] == ["Hochbaute", "Tiefbaute"]
    # Labels are aggregated in slug order (Option pk), not selection order.
    assert export.bauprojekt["nutzungszweck"] == ["Arbeiten", "Wohnen"]

    # Two gebaeude rows aggregate into two Bauwerke, each with its choice labels.
    bauwerke = export.bauprojekt["bauwerke"]
    assert sorted(b["bezeichnung"] for b in bauwerke) == ["Bauwerk 0", "Bauwerk 1"]
    assert all(b["arbeiten_art"] == ["Neubau", "Umbau"] for b in bauwerke)

    # The juristic table maps a juristische_person; a natural table leaves it null.
    assert export.grundeigentuemer["juristische_person"]["name"]
    assert export.projektverfasser["juristische_person"] is None

    # Fields that were never value-asserted on the DB path before.
    assert sorted(s["slug"] for s in export.zirkulation) == ["afu", "arp"]
    assert export.zustaendige_person["group_slug"] == "municipality"
    assert export.zustaendige_person["abteilung"]
    assert export.entscheid["entscheid"] == "entscheid-entscheid-zustimmung"
    # The dossier has two publications; the export takes the latest one and reads
    # both dates off it (conftest seeds May then June).
    assert export.auflage == {"startdatum": "2026-06-01", "enddatum": "2026-06-30"}


@pytest.mark.django_db
def test_gesuchsteller_pairs_each_applicant_with_its_own_vertretung(
    instance_factory, instance_with_case, setup_so_instance, form_utils
):
    """Each entry in the BAG must keep its own Vertretung.

    A represented and an unrepresented applicant in the same dossier must not
    swap representations, and the unrepresented one must stay without.
    """
    instance = setup_so_instance(instance_with_case(instance_factory()), "2601-2026-1")

    represented = so_personal_row_factory(has_representation=True)
    represented["nachname"] = "Represented"
    represented["vertretung-nachname"] = "TheRepresentative"
    unrepresented = so_personal_row_factory()
    unrepresented["nachname"] = "Unrepresented"

    document = instance.case.document
    document.answers.filter(question_id="bauherrin").delete()
    form_utils.add_table_answer(document, "bauherrin", [represented, unrepresented])

    SOGISExport.objects.sync()

    by_applicant = {
        entry["adresse"]["natuerliche_person"]["name"]: entry
        for entry in SOGISExport.objects.get().gesuchsteller
    }
    assert (
        by_applicant["Represented"]["vertretung"]["natuerliche_person"]["name"]
        == "TheRepresentative"
    )
    assert by_applicant["Unrepresented"]["vertretung"] is None


@pytest.mark.django_db
def test_stores_the_drawn_geometry_and_the_plot_fallback(
    instance_factory, instance_with_case, setup_so_instance
):
    """The formatter derives the geometry, so sync only has to store its inputs."""
    drawn = {"markers": [{"x": 2600000.5, "y": 1200000.5}], "geometry": "POINT"}
    setup_so_instance(
        instance_with_case(instance_factory()), "2601-2026-1", gis_karte=drawn
    )

    SOGISExport.objects.sync()

    export = SOGISExport.objects.get()
    assert json.loads(export.gis_geometry) == drawn
    # Kept even with a drawn geometry, so the two are hashed independently.
    assert export.plot_point == {"ost": "2607000.5", "nord": "1228500.5"}


@pytest.mark.django_db
def test_stores_no_drawn_geometry_for_dossiers_predating_the_map(
    instance_factory, instance_with_case, setup_so_instance
):
    setup_so_instance(instance_with_case(instance_factory()), "2601-2026-1", parcels=2)

    SOGISExport.objects.sync()

    export = SOGISExport.objects.get()
    assert export.gis_geometry is None
    assert export.plot_point == {"ost": "2607000.5", "nord": "1228500.5"}


@pytest.mark.django_db
def test_stores_an_unreadable_map_answer_verbatim(
    instance_factory, instance_with_case, setup_so_instance
):
    """Parsing belongs to the formatter, where one bad dossier stays isolated."""
    setup_so_instance(
        instance_with_case(instance_factory()), "2601-2026-1", gis_karte="not json"
    )

    SOGISExport.objects.sync()

    assert SOGISExport.objects.get().gis_geometry == "not json"


@pytest.mark.django_db
def test_bauprojekt_without_buildings_has_empty_bauwerke(
    instance_factory, instance_with_case, setup_so_instance
):
    """A Tiefbaute-only project has a Bauprojekt but zero gebaeude rows.

    The gebaeude (Bauwerke) form is only rendered for Hochbaute, so this is a
    real, common shape the single-building fixture never exercised.
    """
    setup_so_instance(
        instance_with_case(instance_factory()), "2601-2026-1", full=True, buildings=0
    )

    SOGISExport.objects.sync()

    export = SOGISExport.objects.get()
    assert export.bauprojekt is not None
    assert export.bauprojekt["bauwerke"] == []


@pytest.mark.django_db
def test_sync_only_writes_changed_instances(
    instance_factory, instance_with_case, setup_so_instance, form_utils
):
    instance = setup_so_instance(instance_with_case(instance_factory()), "2601-2026-1")

    SOGISExport.objects.sync()

    export = SOGISExport.objects.get()
    original_hash = export.hash
    original_modified_at = export.modified_at

    SOGISExport.objects.sync()

    export.refresh_from_db()
    assert SOGISExport.objects.count() == 1
    assert export.hash == original_hash
    assert export.modified_at == original_modified_at

    instance.case.document.answers.filter(question_id="gemeindenummer-bfs").delete()
    form_utils.add_answer(instance.case.document, "gemeindenummer-bfs", 2602)

    SOGISExport.objects.sync()

    export.refresh_from_db()
    assert SOGISExport.objects.count() == 1
    assert export.hash != original_hash
    assert export.bfsnr == 2602


@pytest.mark.django_db
def test_pending_holds_everything_not_delivered_yet(
    instance_factory, instance_with_case, setup_so_instance
):
    setup_so_instance(instance_with_case(instance_factory()), "2601-2026-1")
    SOGISExport.objects.sync()

    export = SOGISExport.objects.get()
    assert list(SOGISExport.objects.pending()) == [export]

    SOGISExport.objects.mark_exported([export.pk])

    assert not SOGISExport.objects.pending().exists()


@pytest.mark.django_db
def test_pending_holds_exports_changed_since_delivery(
    instance_factory, instance_with_case, setup_so_instance, form_utils
):
    """`modified_at > exported_at` is what makes a changed dossier due again."""
    instance = setup_so_instance(instance_with_case(instance_factory()), "2601-2026-1")
    SOGISExport.objects.sync()

    export = SOGISExport.objects.get()
    SOGISExport.objects.mark_exported([export.pk])
    assert not SOGISExport.objects.pending().exists()

    instance.case.meta.update({"dossier-number": "2601-2026-99"})
    instance.case.save()

    SOGISExport.objects.sync()

    export.refresh_from_db()
    assert export.identifikator == "2601-2026-99"
    assert export.modified_at > export.exported_at
    assert list(SOGISExport.objects.pending()) == [export]


@pytest.mark.django_db
def test_mark_exported_only_marks_the_given_exports(
    instance_factory, instance_with_case, setup_so_instance
):
    for number in ("2601-2026-1", "2601-2026-2"):
        setup_so_instance(instance_with_case(instance_factory()), number)
    SOGISExport.objects.sync()

    delivered, pending = SOGISExport.objects.order_by("identifikator")

    before = now()
    SOGISExport.objects.mark_exported([delivered.pk])

    delivered.refresh_from_db()
    pending.refresh_from_db()

    assert delivered.exported_at >= before
    assert pending.exported_at is None
    assert list(SOGISExport.objects.pending()) == [pending]
