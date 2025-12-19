import pytest

from camac.dossier_import.config.kt_ag.dossier_import.dossier_classes import (
    KtAargauDossier,
    ProceduralStatusEntry,
)
from camac.dossier_import.config.kt_ag.dossier_import.writer_mappings import (
    DossierState,
    map_target_state,
)


@pytest.fixture
def dossier():
    return KtAargauDossier("EBPA-1234-5678", "Testgesuch")


@pytest.mark.skip(reason="manual use only")
def test_map_target_state_non_ebau_municipality_finished(dossier):
    # Test for non-EBAU municipality with "Definitiver Abschluss" status
    dossier.responsible_municipality = "1"  # Non-EBAU municipality
    dossier.cantonal_status = "Definitiver Abschluss"

    map_target_state(dossier)
    assert dossier._meta.target_state == DossierState.FINISHED.value


@pytest.mark.skip(reason="manual use only")
def test_map_target_state_non_ebau_municipality_other(dossier):
    # Test for non-EBAU municipality with other status
    dossier.responsible_municipality = "1"  # Non-EBAU municipality
    dossier.cantonal_status = "In Bearbeitung"

    map_target_state(dossier)
    assert dossier._meta.target_state == DossierState.CIRCULATION.value


@pytest.mark.skip(reason="manual use only")
def test_map_target_state_ebau_municipality_finished(dossier):
    # Test for EBAU municipality with finished status
    dossier.responsible_municipality = "4012"
    dossier.municipal_status = "Gesuch archiviert"
    dossier.procedural_status = []

    map_target_state(dossier)
    assert dossier._meta.target_state == DossierState.FINISHED.value


@pytest.mark.skip(reason="manual use only")
def test_map_target_state_ebau_municipality_construction_monitoring(dossier):
    # Test for EBAU municipality in construction monitoring
    dossier.responsible_municipality = "4012"
    dossier.municipal_status = "Verfügung erstellt"
    dossier.procedural_status = []

    map_target_state(dossier)
    assert dossier._meta.target_state == DossierState.CONSTRUCTION_MONITORING.value


@pytest.mark.skip(reason="manual use only")
def test_map_target_state_ebau_municipality_decision_pending(dossier):
    # Test for EBAU municipality with pending decision
    dossier.responsible_municipality = "4012"
    dossier.municipal_status = "In Bearbeitung"
    dossier.procedural_status = [
        ProceduralStatusEntry(action="Materielle Prüfung gestartet")
    ]

    map_target_state(dossier)
    assert dossier._meta.target_state == DossierState.DECISION.value


@pytest.mark.skip(reason="manual use only")
def test_map_target_state_ebau_municipality_circulation(dossier):
    # Test for EBAU municipality in circulation
    dossier.responsible_municipality = "4012"
    dossier.municipal_status = "In öffentlicher Auflage"
    dossier.procedural_status = [
        ProceduralStatusEntry(action="Stellungnahmen eingefordert")
    ]

    map_target_state(dossier)
    assert dossier._meta.target_state == DossierState.CIRCULATION.value


@pytest.mark.skip(reason="manual use only")
def test_map_target_state_ebau_municipality_circulation_5a(dossier):
    # Test for EBAU municipality in circulation
    dossier.responsible_municipality = "4012"
    dossier.municipal_status = "any"
    dossier.procedural_status = [
        ProceduralStatusEntry(
            action="Vorprüfung abgeschlossen (ohne Unterlagenergänzung)"
        )
    ]

    map_target_state(dossier)
    assert dossier._meta.target_state == DossierState.CIRCULATION.value


@pytest.mark.skip(reason="manual use only")
def test_map_target_state_ebau_municipality_preliminary_check_8(dossier):
    # Test for EBAU municipality in preliminary check
    dossier.responsible_municipality = "4012"
    dossier.municipal_status = "Gesuch übermittelt"
    dossier.procedural_status = []

    map_target_state(dossier)
    assert dossier._meta.target_state == DossierState.FORMAL_EXAM.value


@pytest.mark.skip(reason="manual use only")
def test_map_target_state_ebau_municipality_preliminary_check_7(dossier):
    # Test for EBAU municipality in preliminary check
    dossier.responsible_municipality = "4012"
    dossier.municipal_status = "Gesuch in Bearbeitung"
    dossier.procedural_status = [
        ProceduralStatusEntry(action="Eingangsbestätigung versandt")
    ]

    map_target_state(dossier)
    assert dossier._meta.target_state == DossierState.FORMAL_EXAM.value


@pytest.mark.skip(reason="manual use only")
def test_map_target_state_ebau_municipality_preliminary_check_6(dossier):
    # Test for EBAU municipality in preliminary check
    dossier.responsible_municipality = "4012"
    dossier.municipal_status = "Anfrage / Stellungnahme offen"
    dossier.procedural_status = [
        ProceduralStatusEntry(action="Ergänzung / Überarbeitung eingereicht")
    ]

    map_target_state(dossier)
    assert dossier._meta.target_state == DossierState.FORMAL_EXAM.value


@pytest.mark.skip(reason="manual use only")
def test_map_target_state_ebau_municipality_circulation_fallback(dossier):
    # Test fallback case for EBAU municipality
    dossier.responsible_municipality = "4012"
    dossier.municipal_status = "Unbekannter Status"
    dossier.procedural_status = []

    map_target_state(dossier)
    assert dossier._meta.target_state == DossierState.CIRCULATION.value
