import pytest

from camac.dossier_import.dossier_classes import Dossier
from camac.tags.models import Keyword


@pytest.fixture
def ag_writer(setup_dossier_writer, ag_dossier_import_settings):
    # Lazy import to avoid KeyError: 'DELETE_KEYWORD'
    return setup_dossier_writer("kt_ag")


@pytest.mark.django_db
class TestKtAargauFindExistingInstance:
    def test_find_by_dossier_id_keyword(self, ag_writer, ag_instance):
        """Tests if an instance is found via the Dossier-ID as a Keyword."""
        # 1. Dossier-ID "12345" as Keyword
        Keyword.objects.create(
            name="12345", service=ag_writer._group.service
        ).instances.add(ag_instance)
        # 2. Cantonal-ID "BVUAFB-2023-001" as Keyword
        Keyword.objects.create(
            name="BVUAFB-2023-001", service=ag_writer._group.service
        ).instances.add(ag_instance)
        # 3. Cantonal-ID "2023-123" in case.meta
        ag_instance.case.meta["dossier-number"] = "2023-123"
        ag_instance.case.save()
        ag_instance.group = ag_writer._group
        ag_instance.save()

        # Check resolution for all 3 values
        assert (
            ag_writer.find_existing_instance(Dossier(id="12345", proposal=""), None)
            == ag_instance
        )
        assert (
            ag_writer.find_existing_instance(
                Dossier(id="999", proposal="", cantonal_id="BVUAFB-2023-NONEXISTENT"),
                None,
            )
            is None
        )
        assert (
            ag_writer.find_existing_instance(
                Dossier(id="999", proposal="", cantonal_id="2023-999"), None
            )
            is None
        )

    def test_find_by_cantonal_id_sap_migration(self, ag_writer, ag_instance):
        """Tests if an instance is found via the cantonal_id (SAP Migration 'BVUAFB')."""
        # 1. Dossier-ID "12345" as Keyword
        Keyword.objects.create(
            name="12345", service=ag_writer._group.service
        ).instances.add(ag_instance)
        # 2. Cantonal-ID "BVUAFB-2023-001" as Keyword
        Keyword.objects.create(
            name="BVUAFB-2023-001", service=ag_writer._group.service
        ).instances.add(ag_instance)
        # 3. Cantonal-ID "2023-123" in case.meta
        ag_instance.case.meta["dossier-number"] = "2023-123"
        ag_instance.case.save()
        ag_instance.group = ag_writer._group
        ag_instance.save()

        # Check resolution: First value should be found, others not
        assert (
            ag_writer.find_existing_instance(
                Dossier(id="999", proposal="", cantonal_id="BVUAFB-2023-001"),
                None,
            )
            == ag_instance
        )
        assert (
            ag_writer.find_existing_instance(Dossier(id="23456", proposal=""), None)
            is None
        )
        assert (
            ag_writer.find_existing_instance(
                Dossier(id="999", proposal="", cantonal_id="2023-999"), None
            )
            is None
        )

    def test_find_by_cantonal_id_diba_light(self, ag_writer, ag_instance):
        """Tests if an instance is found via the cantonal_id in Case-Meta (DIBA light)."""
        # Prepare instance with dossier-number in meta
        # 1. Dossier-ID "12345" as Keyword
        Keyword.objects.create(
            name="12345", service=ag_writer._group.service
        ).instances.add(ag_instance)
        # 2. Cantonal-ID "BVUAFB-2023-001" as Keyword
        Keyword.objects.create(
            name="BVUAFB-2023-001", service=ag_writer._group.service
        ).instances.add(ag_instance)
        # 3. Cantonal-ID "2023-123" in case.meta
        ag_instance.case.meta["dossier-number"] = "2023-123"
        ag_instance.case.save()
        # Important: The instance must be assigned to the correct service
        ag_instance.group = ag_writer._group
        ag_instance.save()

        assert (
            ag_writer.find_existing_instance(
                Dossier(id="999", proposal="Test", cantonal_id="2023-123"), None
            )
            == ag_instance
        )

        # Negative checks:
        # 1. Non-existent cantonal_id
        assert (
            ag_writer.find_existing_instance(
                Dossier(id="999", proposal="", cantonal_id="BVUAFB-2023-NONEXISTENT"),
                None,
            )
            is None
        )
        # 2. Non-existent ID (keyword)
        assert (
            ag_writer.find_existing_instance(Dossier(id="23456", proposal=""), None)
            is None
        )

    def test_not_found_returns_none(self, ag_writer):
        """Tests if None is returned when nothing is found."""
        dossier = Dossier(id="nonexistent", proposal="Test")
        found = ag_writer.find_existing_instance(dossier, None)
        assert found is None

    def test_not_found_raises_error_on_prod_intern(self, ag_writer, monkeypatch):
        """Tests if an exception is raised when cantonal_id is not found and KEYCLOAK_CLIENT=diba-prod-intern."""
        from camac.dossier_import.config.kt_ag import KtAargauDossierWriter

        monkeypatch.setenv("KEYCLOAK_CLIENT", "diba-prod-intern")
        dossier = Dossier(id="999", proposal="Test", cantonal_id="2023-999")

        with pytest.raises(KtAargauDossierWriter.ConfigurationError) as excinfo:
            ag_writer.find_existing_instance(dossier, None)

        assert "Dossier with cantonal_id 2023-999 not found" in str(excinfo.value)

    def test_cantonal_id_no_match_no_error(self, ag_writer):
        """Tests if None is returned when cantonal_id exists but does not match any schema."""
        dossier = Dossier(id="999", proposal="Test", cantonal_id="SOME-OTHER-ID")
        found = ag_writer.find_existing_instance(dossier, None)
        assert found is None
