import datetime
import shutil
from collections import OrderedDict
from pathlib import Path

import pytest
from django.conf import settings
from django.core.files import File
from django.core.management import call_command
from django.utils.module_loading import import_string

from camac.dossier_import.loaders import XlsxFileDossierLoader

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
        ("ADDRESS-ZIP", "6416"),
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
        ("PROJECT-COST", "Projektkosten CHF 250.000"),
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
    return dossier_row_sparse | OrderedDict(data)


@pytest.fixture
def dossier(dossier_row_full, dossier_import_settings):
    loader = XlsxFileDossierLoader()
    return loader._load_dossier(dossier_row_full)


@pytest.fixture
def dossier_loader():
    return XlsxFileDossierLoader()


@pytest.fixture
def load_fixtures_so(
    caluma_workflow_config_so,
    service_factory,
    so_construction_monitoring_settings,
    so_decision_settings,
):
    caluma_workflow_config_so.allow_forms.add("migriertes-dossier")
    service = service_factory(
        external_identifier="2601", service_group__name="municipality"
    )

    return service, [
        # TODO: Simplify to only require common and dossier import form fixtures
        "kt_so/config/caluma_form.json",
        "kt_so/config/caluma_form_v2.json",
        "kt_so/config/caluma_form_default_answers.json",
        "kt_so/config/caluma_decision_form.json",
    ]


@pytest.fixture
def load_fixtures_gr(
    caluma_workflow_config_gr,
    # TODO: Uncomment this as soon as the construction monitoring module in GR
    # is permanently enabled
    # gr_construction_monitoring_settings,
    gr_decision_settings,
    gr_distribution_settings,
    service_factory,
):
    caluma_workflow_config_gr.allow_forms.add("migriertes-dossier")
    service = service_factory(service_group__name="municipality")

    return service, [
        # TODO: Simplify to only require common and dossier import form fixtures
        "kt_gr/config/caluma_form.json",
        "kt_gr/config/caluma_form_v2.json",
        "kt_gr/config/caluma_form_v3.json",
        "kt_gr/config/caluma_form_v4.json",
        "kt_gr/config/caluma_form_v5.json",
        "kt_gr/config/caluma_form_v6.json",
        "kt_gr/config/caluma_form_common.json",
        "kt_gr/config/caluma_decision_form.json",
        # TODO: This should be removed when the reference to the question
        # "complete-material-exam" in the `caluma_form.json` fixture is removed.
        # Why is it there in the first place?
        "kt_gr/config/caluma_material_exam_form.json",
    ]


@pytest.fixture
def load_fixtures_ag(
    ag_construction_monitoring_settings,
    ag_decision_settings,
    caluma_workflow_config_ag,
    service_factory,
    user_factory,
):
    caluma_workflow_config_ag.allow_forms.add("importiertes-dossier")
    service = service_factory(service_group__name="municipality")

    # Needed to verify import of responsible user
    user_factory(email="aduncan@example.org")

    # Needed for workflow
    service_factory(slug="afb", service_group__name="service-afb")

    return service, [
        # TODO: Simplify to only require common and dossier import form fixtures
        "kt_ag/config/caluma_form.json",
        "kt_ag/config/caluma_form_common.json",
        "kt_ag/config/caluma_decision_form.json",
    ]


@pytest.fixture
def load_fixtures_sz(
    caluma_workflow_config_sz,
    location,
    sz_construction_monitoring_settings,
    workflow_item_factory,
):
    location.communal_federal_number = "1312"
    location.save()

    for pk in [10, 15]:
        workflow_item_factory(pk=pk)

    return None, ["kt_schwyz/config/buildingauthority.json"]


@pytest.fixture
def load_fixtures_be(
    be_decision_settings,
    caluma_workflow_config_be,
    construction_control_for,
    service_factory,
):
    service = service_factory(service_group__name="municipality")
    construction_control_for(service)

    return service, [
        "kt_bern/config/caluma_form_common.json",
        "kt_bern/config/caluma_dossier_import_form.json",
        "kt_bern/config/caluma_ebau_number_form.json",
        "kt_bern/config/caluma_decision_form.json",
    ]


@pytest.fixture
def setup_dossier_writer(
    alexandria_category_factory,
    attachment_section,
    form,
    group,
    location,
    mocker,
    request,
    role_factory,
    settings,
    user,
):
    def wrapper(config):
        # Needed for permissions module `instance_created` trigger
        mocker.patch(
            "camac.permissions.config.common.get_support_role",
            return_value=role_factory(),
        )

        common_fixtures = [
            # list of fixtures common to all configs. e. g.:
            f"{config}/config/instance.json",
            f"{config}/config/permissions.json",
        ]

        short_name = settings.APPLICATIONS[config]["SHORT_NAME"]
        request.getfixturevalue(f"set_application_{short_name}")

        request.getfixturevalue(f"{short_name}_permissions_settings")
        dossier_import_settings = request.getfixturevalue(
            f"{short_name}_dossier_import_settings"
        )
        service, config_fixtures = request.getfixturevalue(
            f"load_fixtures_{short_name}"
        )

        dossier_import_settings["USER"] = user.username
        dossier_import_settings["FORM_ID"] = form.pk
        dossier_import_settings["ATTACHMENT_SECTION_ID"] = attachment_section.pk
        dossier_import_settings["ALEXANDRIA_CATEGORY"] = alexandria_category_factory(
            allowed_mime_types=["application/pdf"]
            if config == "kt_so"
            else ["application/pdf", "text/plain"]
        ).pk

        group.service = service
        group.save()

        writer_cls = import_string(settings.DOSSIER_IMPORT["WRITER_CLASS"])
        dossier_writer = writer_cls(
            user_id=user.pk,
            group_id=group.pk,
            location_id=location.pk,
        )

        # TODO: This is where most of the time in the test suite is wasted. If
        # we manage to shrink the data that is being loaded for **every** test,
        # we may gain quite the performance improvement.
        # Another approach could be to use the pre-filled cantonal test DB like
        # it's done in this PoC:
        # https://git.adfinis.com/camac-ng/camac-ng/-/merge_requests/12850
        call_command(
            "loaddata",
            [settings.ROOT_DIR(path) for path in common_fixtures + config_fixtures],
        )

        return dossier_writer

    return wrapper
