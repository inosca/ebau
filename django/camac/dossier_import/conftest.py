import datetime
import shutil
from collections import OrderedDict
from pathlib import Path

import pytest
from django.core.files import File
from django.core.management import call_command
from django.utils.module_loading import import_string

from camac.dossier_import.loaders import XlsxFileDossierLoader
from camac.dossier_import.tests.test_dossier_import_case import TEST_IMPORT_FILE_PATH
from camac.user.models import Group


@pytest.fixture
def archive_file(settings):
    def get_django_file(name, path=TEST_IMPORT_FILE_PATH, mode="rb"):
        target_path = Path(settings.MEDIA_ROOT) / "dossier_imports"
        target_path.mkdir(parents=True, exist_ok=True)
        shutil.copy(str(Path(path) / name), str(target_path / name))
        return File(open(str(Path(path) / name), mode), name=f"dossier_imports/{name}")

    return get_django_file


@pytest.fixture
def dossier_row_sparse():
    return OrderedDict(
        [
            ("ID", "2017-84"),
            ("STATUS", "SUBMITTED"),
            (
                "PROPOSAL",
                "Projektänderung zu Um- und Anbau am Wohnhaus und Solaranlage",
            ),
            ("SUBMIT-DATE", datetime.datetime(2017, 4, 12, 0, 0)),
        ]
    )


@pytest.fixture
def dossier_row_full(dossier_row_sparse):
    data = [
        ("CANTONAL-ID", "2020-1"),
        ("WORKFLOW", "PRELIMINARY"),
        ("PARCEL", "1180, 1182"),
        ("EGRID", "CH207838732652,CH207838735643"),
        ("COORDINATE-N", "1‘213‘425,1‘213‘489"),
        ("COORDINATE-E", "2‘685‘785,2‘685‘135"),
        ("PROPOSAL", "Neubau,Einfamilienhaus"),
        ("ADDRESS-STREET", "Unterfeld"),
        ("ADDRESS-STREET-NR", "4"),
        ("ADDRESS-CITY", "Steinerberg"),
        ("USAGE", "W2"),
        ("TYPE", "Baugesuch"),
        ("SUBMIT-DATE", datetime.datetime(2017, 4, 17)),
        ("PUBLICATION-DATE", datetime.datetime(2017, 4, 18)),
        ("DECISION-DATE", datetime.datetime(2017, 4, 19)),
        ("CONSTRUCTION-START-DATE", datetime.datetime(2017, 4, 20)),
        ("PROFILE-APPROVAL-DATE", datetime.datetime(2017, 4, 21)),
        ("FINAL-APPROVAL-DATE", datetime.datetime(2017, 4, 22)),
        ("COMPLETION-DATE", datetime.datetime(2017, 4, 23)),
        ("CUSTOM-1", "custom-value-1"),
        ("CUSTOM-2", "custom-value-2"),
        ("LINK", "https://example.com"),
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
    dossier_row_sparse.update(data)
    return dossier_row_sparse


@pytest.fixture()
def dossier(dossier_row_full):
    loader = XlsxFileDossierLoader()
    return loader._load_dossier(dossier_row_full)


@pytest.fixture()
def dossier_loader():
    return XlsxFileDossierLoader()


@pytest.fixture
def make_dossier_writer(
    db,
    settings,
    user,
    group,
    role,
    location,
):
    def init_writer(config):
        Group.objects.get_or_create(pk=group.pk, defaults={"role": role})
        writer_cls = import_string(
            settings.APPLICATION["DOSSIER_IMPORT"]["WRITER_CLASS"]
        )
        return writer_cls(
            user_id=user.pk,
            group_id=group.pk,
            location_id=location.pk,
            import_settings=settings.APPLICATION["DOSSIER_IMPORT"],
        )

    return init_writer


@pytest.fixture
def load_fixtures_sz(
    db,
    settings,
    caluma_workflow_config_sz,
    sz_construction_monitoring_settings,
    instance_state_factory,
    workflow_item_factory,
):
    django_fixture_paths = [
        settings.ROOT_DIR("kt_schwyz/config/buildingauthority.json")
    ]

    for pk in [10, 15]:
        workflow_item_factory(pk=pk)
    yield None, django_fixture_paths


@pytest.fixture()
def load_fixtures_be(
    db,
    settings,
    caluma_workflow_config_be,
    caluma_forms_be,
    be_decision_settings,
    decision_factory,
    service_factory,
    instance_state_factory,
    construction_control_for,
    document_factory,
    dynamic_option_factory,
):
    django_fixture_paths = [
        settings.ROOT_DIR("kt_bern/config/caluma_form_common.json"),
        settings.ROOT_DIR("kt_bern/config/caluma_dossier_import_form.json"),
        settings.ROOT_DIR("kt_bern/config/caluma_ebau_number_form.json"),
    ]
    service = service_factory(service_group__name="municipality")
    construction_control_for(service)
    dynamic_option_factory(
        slug=str(service.pk), question_id="gemeinde", document=document_factory()
    )
    yield service, django_fixture_paths


@pytest.fixture()
def setup_dossier_writer(
    request,
    db,
    settings,
    role,
    form,
    service,
    user,
    make_dossier_writer,
    attachment_section,
):
    def wrapper(config):
        common_fixtures_paths = [
            # list of fixtures common to all configs. e. g.:
            settings.ROOT_DIR(f"{config}/config/instance.json")
        ]
        settings.APPLICATION = settings.APPLICATIONS[config]
        settings.APPLICATION["DOSSIER_IMPORT"]["USER"] = user.username
        dossier_writer = make_dossier_writer(config)
        group = dossier_writer._group
        if config == "kt_schwyz":
            _, config_fixtures = request.getfixturevalue("load_fixtures_sz")
        if config == "kt_bern":
            service, config_fixtures = request.getfixturevalue("load_fixtures_be")
            group.service = service
            group.save()
        settings.APPLICATION["DOSSIER_IMPORT"]["FORM_ID"] = form.pk
        settings.APPLICATION["DOSSIER_IMPORT"]["ATTACHMENT_SECTION_ID"] = (
            attachment_section.pk
        )
        fixture_paths = common_fixtures_paths + config_fixtures
        if len(fixture_paths):
            call_command("loaddata", *fixture_paths)
        return dossier_writer

    return wrapper
