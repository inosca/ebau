import pytest
from django.core.management import call_command
from django.utils.module_loading import import_string

from camac.dossier_import.tests.test_dossier_import_case import TEST_IMPORT_FILE


@pytest.fixture
def setup_fixtures_required_by_application_config(django_db_setup, django_db_blocker):
    def wrapper(config):
        with django_db_blocker.unblock():
            call_command("loaddata", f"/app/{config}/config/caluma_workflow.json")
            call_command("loaddata", f"/app/{config}/config/instance.json")
            call_command("loaddata", f"/app/{config}/config/document.json")

    return wrapper


@pytest.fixture
def initialized_dossier_importer(
    db,
    setup_fixtures_required_by_application_config,
    settings,
    group_factory,
    role,
    location,
    attachment_section_factory,
):
    def wrapper(
        config, user_id: int, group_id: int, path_to_archive: str = TEST_IMPORT_FILE
    ):
        application_settings = settings.APPLICATIONS[config]
        setup_fixtures_required_by_application_config(config)
        group_factory(pk=group_id, role=role)
        importer_cls = import_string(
            application_settings["DOSSIER_IMPORT"]["XLSX_IMPORTER_CLASS"]
        )
        importer = importer_cls(
            user_id=user_id, import_settings=application_settings["DOSSIER_IMPORT"]
        )
        importer.initialize(group_id, location.pk, path_to_archive)
        return importer

    return wrapper
