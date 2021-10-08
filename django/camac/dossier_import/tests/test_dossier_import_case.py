from pathlib import Path

import pytest
from django.utils.module_loading import import_string

TEST_IMPORT_FILE = "data/import-example.zip"


@pytest.fixture
def initialized_dossier_importer(
    db,
    settings,
    service_factory,
    user_factory,
    group_factory,
    form_factory,
    form_state_factory,
    instance_state_factory,
    workflow_factory,
    attachment_section_factory,
):
    def wrapper(config, service_id: int, path_to_archive: str = TEST_IMPORT_FILE):
        application_settings = settings.APPLICATIONS[config]

        workflow_factory(pk="building-permit", allow_all_forms=True)  # TODO: check
        form_state_factory(pk=1)
        form_factory(
            pk=application_settings["DOSSIER_IMPORT"]["FORM_ID"], form_state_id=1
        )
        service = service_factory(service_id=service_id)
        group_factory(service=service)
        user_factory(username=application_settings["DOSSIER_IMPORT"]["USER"])
        for mapping in application_settings["DOSSIER_IMPORT"][
            "INSTANCE_STATE_MAPPING"
        ].values():
            instance_state_factory(pk=mapping)
        attachment_section_factory(
            pk=application_settings["DOSSIER_IMPORT"]["ATTACHMENT_SECTION_ID"]
        )

        importer_cls = import_string(
            application_settings["DOSSIER_IMPORT"]["XLSX_IMPORTER_CLASS"]
        )
        importer = importer_cls(service_id)
        importer.settings = application_settings["DOSSIER_IMPORT"]
        importer.initialize(service_id, path_to_archive)
        return importer

    return wrapper


@pytest.mark.parametrize("config,service_id", [("kt_schwyz", 42)])
def test_start_dossier_import_case(
    db, initialized_dossier_importer, settings, config, service_id
):
    importer = initialized_dossier_importer(config, service_id)

    importer.clean_up()


@pytest.mark.parametrize("config,service_id", [("kt_schwyz", 42)])
def test_create_instance_dossier_import_case(
    db, initialized_dossier_importer, settings, config, service_id
):
    importer = initialized_dossier_importer(config, service_id)
    importer.import_dossiers()
    assert len(importer.messages) == 2
    assert not Path(f"/app/tmp/dossier_import/{str(importer.import_case.id)}").exists()
    importer.clean_up()
