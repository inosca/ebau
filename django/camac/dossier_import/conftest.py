import datetime
import shutil
from collections import OrderedDict
from copy import deepcopy
from pathlib import Path

import pytest
from alexandria.core.factories import CategoryFactory
from django.conf import settings
from django.core.files import File
from django.core.management import call_command
from django.utils.module_loading import import_string

from camac.dossier_import.loaders import XlsxFileDossierLoader
from camac.user.models import Group

TEST_IMPORT_FILE_PATH = str(
    Path(settings.ROOT_DIR) / "camac/dossier_import/tests/data/"
)


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
def dossier(dossier_row_full, dossier_import_settings):
    loader = XlsxFileDossierLoader()
    return loader._load_dossier(dossier_row_full)


@pytest.fixture()
def dossier_loader():
    return XlsxFileDossierLoader()


@pytest.fixture
def load_fixtures_so(
    db,
    settings,
    caluma_workflow_config_so,
    so_dossier_import_settings,
    document_factory,
    dynamic_option_factory,
    service_factory,
    so_decision_settings,
    so_construction_monitoring_settings,
    so_permissions_settings,
):
    extra_fixtures = [
        settings.ROOT_DIR("kt_so/config/permissions.json"),
        settings.ROOT_DIR("kt_so/config/caluma_form.json"),
        settings.ROOT_DIR("kt_so/config/caluma_form_default_answers.json"),
        settings.ROOT_DIR("kt_so/config/caluma_decision_form.json"),
        settings.ROOT_DIR("kt_so/config/caluma_construction_monitoring_form.json"),
        settings.ROOT_DIR("kt_so/config/caluma_construction_monitoring_workflow.json"),
    ]

    caluma_workflow_config_so.allow_forms.add("migriertes-dossier")
    service = service_factory(service_group__name="municipality")
    dynamic_option_factory(
        slug=str(service.pk), question_id="gemeinde", document=document_factory()
    )

    so_dossier_import_settings["ALEXANDRIA_CATEGORY"] = CategoryFactory(
        allowed_mime_types=["application/pdf"]
    ).pk

    yield service, extra_fixtures


@pytest.fixture
def load_fixtures_sz(
    db,
    settings,
    caluma_workflow_config_sz,
    sz_construction_monitoring_settings,
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
    construction_control_for,
    document_factory,
    dynamic_option_factory,
    be_permissions_settings,
    application_settings,
):
    # Needed in order to make instance.responsible_service() work properly
    application_settings["ACTIVE_SERVICES"] = deepcopy(
        settings.APPLICATIONS["kt_bern"]["ACTIVE_SERVICES"]
    )

    django_fixture_paths = [
        settings.ROOT_DIR("kt_bern/config/permissions.json"),
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
    form,
    role,
    user,
    group,
    location,
    attachment_section,
    application_settings,
    role_factory,
):
    def wrapper(config):
        # Needed for permissions module `instance_created` trigger
        role_factory(name="Support")

        common_fixtures_paths = [
            # list of fixtures common to all configs. e. g.:
            settings.ROOT_DIR(f"{config}/config/instance.json")
        ]

        settings.APPLICATION_NAME = config
        short_name = settings.APPLICATIONS[config]["SHORT_NAME"]
        application_settings["SHORT_NAME"] = short_name

        dossier_import_settings = request.getfixturevalue(
            f"{short_name}_dossier_import_settings"
        )
        service, config_fixtures = request.getfixturevalue(
            f"load_fixtures_{short_name}"
        )

        dossier_import_settings["USER"] = user.username
        writer_cls = import_string(settings.DOSSIER_IMPORT["WRITER_CLASS"])
        this_group, _ = Group.objects.update_or_create(
            pk=group.pk, defaults={"role": role}
        )
        dossier_writer = writer_cls(
            user_id=user.pk,
            group_id=this_group.pk,
            location_id=location.pk,
        )

        if config in ["kt_bern", "kt_so"]:
            this_group.service = service
            this_group.save()
            dossier_writer._group.refresh_from_db()
        elif config == "kt_schwyz":
            application_settings["SHORT_DOSSIER_NUMBER"] = True

        if config == "kt_so":
            application_settings["DOCUMENT_BACKEND"] = "alexandria"
        else:
            application_settings["DOCUMENT_BACKEND"] = "camac-ng"

        dossier_import_settings["FORM_ID"] = form.pk
        dossier_import_settings["ATTACHMENT_SECTION_ID"] = attachment_section.pk

        fixture_paths = common_fixtures_paths + config_fixtures
        if len(fixture_paths):
            call_command("loaddata", *fixture_paths)
        return dossier_writer

    return wrapper
