import datetime
from collections import OrderedDict

import pytest
from django.core.management import call_command
from django.utils.module_loading import import_string

from camac.dossier_import.tests.test_dossier_import_case import TEST_IMPORT_FILE
from camac.user.models import Group


@pytest.fixture
def setup_fixtures_required_by_application_config(django_db_setup, django_db_blocker):
    """Set up application configuration data.

    Use this when testing real life dependent procedures and not because you're to
    lazy to setup your test requirements. These fixtures are a bloat and unnecessarily
    slow down the pipeline.
    """

    def load_data(config):
        with django_db_blocker.unblock():
            call_command("loaddata", f"/app/{config}/config/instance.json")
            call_command("loaddata", f"/app/{config}/config/caluma_workflow.json")
            call_command("loaddata", f"/app/{config}/config/caluma_form.json")
            call_command("loaddata", f"/app/{config}/config/document.json")

    return load_data


@pytest.fixture
def make_workflow_items_for_config(workflow_item_factory):
    def loop_workflow_item_factory(config):
        for pk in {"kt_schwyz": [10, 15, 55, 56, 47, 59, 67]}.get(config, []):
            workflow_item_factory(pk=pk)

    return loop_workflow_item_factory


@pytest.fixture
def dossier_row():
    return OrderedDict(
        [
            ("ID", "2017-84"),
            ("CANTONAL-ID", "B2017-0683"),
            ("STATUS", "SUBMITTED"),
            ("PARCEL", 1180.1182),
            ("EGRID", "CH207838732652, CH207838735643"),
            ("COORDINATE-N", "2‘685‘785, 2‘685‘135"),
            ("COORDINATE-E", "1‘213‘425, 1‘213‘489"),
            (
                "PROPOSAL",
                "Projektänderung zu Um- und Anbau am Wohnhaus und Solaranlage",
            ),
            ("ADDRESS-STREET", "Unterfeld"),
            ("ADDRESS-STREET-NR", "3a"),
            ("ADDRESS-CITY", "Steinerberg"),
            ("USAGE", "W2"),
            ("TYPE", "vereinfachtes Verfahren"),
            ("SUBMIT-DATE", datetime.datetime(2017, 4, 12, 0, 0)),
            ("PUBLICATION-DATE", datetime.datetime(2017, 4, 15, 0, 0)),
            ("DECISION-DATE", datetime.datetime(2017, 4, 17, 0, 0)),
            ("CONSTRUCTION-START-DATE", datetime.datetime(2017, 4, 19, 0, 0)),
            ("PROFILE-APPROVAL-DATE", datetime.datetime(2017, 4, 20, 0, 0)),
            ("FINAL-APPROVAL-DATE", datetime.datetime(2017, 4, 23, 0, 0)),
            ("COMPLETION-DATE", datetime.datetime(2017, 4, 24, 0, 0)),
            ("CUSTOM-1", ""),
            ("CUSTOM-2", ""),
            ("LINK", ""),
            ("APPLICANT-FIRST-NAME", "Ulrich"),
            ("APPLICANT-LAST-NAME", "Kissling"),
            ("APPLICANT-COMPANY", "Swisscom"),
            ("APPLICANT-STREET", "Gribschstrasse"),
            ("APPLICANT-STREET-NUMBER", "3a"),
            ("APPLICANT-CITY", "Steinerberg"),
            ("APPLICANT-PHONE", "0771234123"),
            ("APPLICANT-EMAIL", "urlichkissling@example.com"),
            ("LANDOWNER-FIRST-NAME", "Ulrich"),
            ("LANDOWNER-LAST-NAME", "Kissling"),
            ("LANDOWNER-COMPANY", "Swisscom"),
            ("LANDOWNER-STREET", "Gribschstrasse"),
            ("LANDOWNER-STREET-NUMBER", "3a"),
            ("LANDOWNER-CITY", "Steinerberg"),
            ("LANDOWNER-PHONE", "0771234123"),
            ("LANDOWNER-EMAIL", "urlichkissling@example.com"),
            ("PROJECTAUTHOR-FIRST-NAME", "Ulrich"),
            ("PROJECTAUTHOR-LAST-NAME", "Kissling"),
            ("PROJECTAUTHOR-COMPANY", "Swisscom"),
            ("PROJECTAUTHOR-STREET", "Gribschstrasse"),
            ("PROJECTAUTHOR-STREET-NUMBER", "3a"),
            ("PROJECTAUTHOR-CITY", "Steinerberg"),
            ("PROJECTAUTHOR-PHONE", "0771234123"),
            ("PROJECTAUTHOR-EMAIL", "urlichkissling@example.com"),
        ]
    )


@pytest.fixture
def make_dossier_writer(
    db,
    setup_fixtures_required_by_application_config,
    make_workflow_items_for_config,
    settings,
    group_factory,
    role,
    location,
):
    def init_writer(
        config, user_id: int, group_id: int, path_to_archive: str = TEST_IMPORT_FILE
    ):
        make_workflow_items_for_config(config)
        settings.APPLICATION = settings.APPLICATIONS[config]
        setup_fixtures_required_by_application_config(config)
        Group.objects.get_or_create(pk=group_id, defaults={"role": role})
        writer_cls = import_string(
            settings.APPLICATION["DOSSIER_IMPORT"][
                "ZIP_ARCHIVE_IMPORT_DOSSIER_WRITER_CLASS"
            ]
        )
        return writer_cls(
            user_id,
            group_id,
            location.pk,
            path_to_archive,
            import_settings=settings.APPLICATION["DOSSIER_IMPORT"],
        )

    return init_writer


@pytest.fixture
def get_dossier_loader(db, settings, application_settings):
    # this fixture requires configured DOSSIER_IMPORT properties in `settings.py`
    # and generally might not run as expected with the 'demo' configuration.
    def get_loader():
        return import_string(
            settings.APPLICATION["DOSSIER_IMPORT"][
                "ZIP_ARCHIVE_IMPORT_DOSSIER_LOADER_CLASS"
            ]
        )()

    return get_loader
