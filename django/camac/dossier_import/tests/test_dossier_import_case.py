from pathlib import Path

import pytest
from django.utils.module_loading import import_string

TEST_IMPORT_FILE = "data/import-example.zip"


@pytest.fixture
def initialized_dossier_importer(
    db,
    settings,
    location_factory,
    user_factory,
    group_factory,
    form_factory,
    form_state_factory,
    instance_state_factory,
    workflow_factory,
):
    def wrapper(config, location: str, path_to_file: str = TEST_IMPORT_FILE):
        application_settings = settings.APPLICATIONS[config]
        workflow_factory(pk="building-permit", allow_all_forms=True)  # TODO: check
        form_state_factory(pk=1)
        form_factory(
            pk=application_settings["DOSSIER_IMPORT"]["FORM_ID"], form_state_id=1
        )
        location_factory(name=location)
        user_factory(username=application_settings["DOSSIER_IMPORT"]["USER"])
        group_factory(name=application_settings["DOSSIER_IMPORT"]["GROUP"])
        for mapping in application_settings["DOSSIER_IMPORT"][
            "INSTANCE_STATE_MAPPING"
        ].values():
            instance_state_factory(pk=mapping)

        importer_cls = import_string(
            application_settings["DOSSIER_IMPORT"]["XLSX_IMPORTER_CLASS"]
        )
        importer = importer_cls(location)
        importer.settings = application_settings["DOSSIER_IMPORT"]
        importer.initialize(location, path_to_file)
        return importer

    return wrapper


@pytest.mark.parametrize("config,location", [("kt_schwyz", "Feuisisberg")])
def test_start_dossier_import_case(
    db, initialized_dossier_importer, settings, config, location
):
    importer = initialized_dossier_importer(config, location)
    assert hasattr(importer, "import_case")
    assert len(importer.dossiers) == 2
    importer.clean_up()
    assert not Path(f"/app/tmp/dossier_import/{str(importer.import_case.id)}").exists()


@pytest.mark.parametrize("config,location", [("kt_schwyz", "Feuisisberg")])
def test_create_instance_dossier_import_case(
    db, initialized_dossier_importer, settings, config, location
):
    importer = initialized_dossier_importer(config, location)
    importer.import_dossiers()
    for dossier in importer.dossiers:
        assert (
            dossier.Meta.instance.fields.filter(
                name__in=["bauherrschaft", "bezeichnung"]
            ).count()
            == 2
        )
