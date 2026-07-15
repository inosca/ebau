import pytest
from caluma.caluma_workflow.models import Task, WorkItem
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status

from camac.caluma.extensions.permissions import CustomPermission
from camac.instance.rpg2_import import (
    RPG2ImportReader,
    RPG2Labeler,
    RPG2Transform,
)
from camac.permissions import api as permissions_api
from camac.settings.modules.rpg2_schema import ImportMappingEntry


@pytest.fixture
def reader(db, mocker, instance):
    mocker.patch("camac.instance.rpg2_import.MasterData")
    return RPG2ImportReader(instance)


def test_transform_apply_success():
    assert (
        RPG2Transform.apply("first_choice_from_multiple", ["option-a", "option-b"])
        == "option-a"
    )


def test_transform_apply_raises_for_unknown_name():
    with pytest.raises(
        ValueError,
        match="Unknown rpg2 transform: no_such_transform. Please define no_such_transform as a @staticmethod in RPG2Transform",
    ):
        RPG2Transform.apply("no_such_transform", "some value")


@pytest.mark.parametrize(
    ("input_value", "expected"),
    [
        (["option-a", "option-b"], "option-a"),
        (["option-b"], "option-b"),
        ([], None),
        (None, None),
        ("not-a-list", None),
    ],
)
def test_first_choice_from_multiple(input_value, expected):
    assert RPG2Transform.first_choice_from_multiple(input_value) == expected


@pytest.mark.parametrize(
    ("option_slug", "source_slugs", "expected"),
    [
        ("source-question-a01", ["source-question"], "a01"),
        ("source-question-v5-a01", ["source-question-v7", "source-question-v5"], "a01"),
        ("unrelated-a01", ["source-question"], "unrelated-a01"),
    ],
)
def test_strip_source_root(option_slug, source_slugs, expected):
    assert RPG2ImportReader._strip_source_root(option_slug, source_slugs) == expected


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("is_option_target", "transform", "value", "expected"),
    [
        (True, None, None, None),
        (True, None, "source-question-a01", "a01"),
        (True, None, ["source-question-a01", "source-question-a02"], ["a01", "a02"]),
        (
            True,
            "first_choice_from_multiple",
            ["source-question-a02", "source-question-a01"],
            "a02",
        ),
        (True, "first_choice_from_multiple", [], None),
        (False, None, 5, 5),
    ],
)
def test_apply_transform_and_strip(
    reader, is_option_target, transform, value, expected
):
    config = ImportMappingEntry(
        is_option_target=is_option_target,
        transform=transform,
        source_slugs=["source-question"],
    )
    assert reader._apply_transform_and_strip(value, config) == expected


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("source_row", "expected"),
    [
        ({"column-a": "source-column-a-a01", "column-b": None}, {"column-a": "a01"}),
        (
            {"column-a": "source-column-a-a01", "column-b": 10},
            {"column-a": "a01", "column-b": 10},
        ),
        ({"column-a": None, "column-b": None}, {}),
    ],
)
def test_parse_row(reader, source_row, expected):
    row_mapping = {
        "column-a": ImportMappingEntry(
            is_option_target=True, source_slugs=["source-column-a"]
        ),
        "column-b": ImportMappingEntry(source_slugs=["source-column-b"]),
    }
    assert reader._parse_row(source_row, row_mapping) == expected


@pytest.mark.django_db
def test_resolve_source_answer(reader):
    source_config = ImportMappingEntry(
        source_slugs=["source-question"],
        from_work_item="some-task",
        is_option_target=True,
    )
    reader.md.answer_resolver.return_value = "source-question-a01"

    assert reader._resolve_source(source_config) == "a01"
    reader.md.answer_resolver.assert_called_once_with(
        lookup=["source-question"], document_from_work_item="some-task"
    )


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("table_rows", "expected"),
    [
        (
            [
                {"column-a": "source-column-a-a01", "column-b": 10},
                {"column-a": None, "column-b": None},
            ],
            [{"column-a": "a01", "column-b": 10}],
        ),
        ([{"column-a": None, "column-b": None}], None),
    ],
)
def test_resolve_source_table(reader, table_rows, expected):
    source_config = ImportMappingEntry(
        source_slugs=["source-table"],
        row_mapping={
            "column-a": ImportMappingEntry(
                is_option_target=True, source_slugs=["source-column-a"]
            ),
            "column-b": ImportMappingEntry(source_slugs=["source-column-b"]),
        },
    )
    reader.md.table_resolver.return_value = table_rows

    assert reader._resolve_source(source_config) == expected
    _, kwargs = reader.md.table_resolver.call_args
    assert kwargs["column_mapping"] == {
        "column-a": ["source-column-a"],
        "column-b": ["source-column-b"],
    }


def test_rpg2_labeler_raises_for_unsupported_types():
    with pytest.raises(NotImplementedError):
        RPG2Labeler().lookup_dynamic_choice(None, None)


@pytest.fixture
def rpg2_edit_permission(mocker):
    mocker.patch.object(
        CustomPermission, "has_camac_edit_permission", return_value=True
    )


def _add_rpg2_work_item(instance, caluma_work_item_factory, settings):
    rpg2_task = Task.objects.get(pk=settings.RPG2.task)
    caluma_work_item_factory(
        task_id=settings.RPG2.task,
        case=instance.case,
        status=WorkItem.STATUS_READY,
        document__form_id=rpg2_task.form,
    )


@pytest.fixture
def rpg2_ag_instance(
    ag_instance,
    ag_rpg2_settings,
    ag_access_levels,
    admin_client,
    caluma_work_item_factory,
    caluma_document_factory,
    settings,
):
    call_command("loaddata", settings.ROOT_DIR("kt_ag/config/caluma_rpg2_form.json"))
    _add_rpg2_work_item(ag_instance, caluma_work_item_factory, settings)
    caluma_work_item_factory(
        task_id="cantonal-exam",
        case=ag_instance.case,
        status=WorkItem.STATUS_COMPLETED,
        document=caluma_document_factory(),
    )
    # for visibility
    permissions_api.grant(
        ag_instance,
        grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
        access_level="distribution-service",
        service=admin_client.user.groups.first().service,
    )
    return ag_instance


@pytest.fixture
def rpg2_ag_instance_with_answers(rpg2_ag_instance, form_utils):
    document = rpg2_ag_instance.case.document
    form_utils.add_answer(
        document,
        question="ausserhalb-bauzone",
        value="ausserhalb-bauzone-ja",
        options=["ausserhalb-bauzone-ja"],
    )
    form_utils.add_answer(document, question="anzahl-neue-gebaeude-greater-6m", value=3)
    form_utils.add_answer(
        document, question="anzahl-gebaeude-greater-6-m-die-abgebrochen-werden", value=1
    )
    form_utils.add_answer(
        document,
        question="werden-flaechen-neu-versiegelt-oder-entsiegelt",
        value="werden-flaechen-neu-versiegelt-oder-entsiegelt-ja",
        options=["werden-flaechen-neu-versiegelt-oder-entsiegelt-ja"],
    )
    form_utils.add_table_answer(
        document,
        question="versiegelte-entsiegelte-flaechen",
        rows=[
            {
                "art-der-ver-bzw-entsiegelung": {
                    "value": "art-der-ver-bzw-entsiegelung-entsiegelte-renaturierte-flaechen-gebaeude",
                    "options": [
                        "art-der-ver-bzw-entsiegelung-entsiegelte-renaturierte-flaechen-gebaeude"
                    ],
                },
                "flaeche-m-versiegelt": 120,
                "materialisierung-der-neu-versiegelten-flaechen": {
                    "value": "materialisierung-der-neu-versiegelten-flaechen-andere",
                    "options": [
                        "materialisierung-der-neu-versiegelten-flaechen-andere"
                    ],
                },
                "beschreibung-versiegelte-flaeche": "Beschreibung Text",
                "nutzung-der-versiegelten-flaeche": {
                    "value": "nutzung-der-versiegelten-flaeche-andere",
                    "options": ["nutzung-der-versiegelten-flaeche-andere"],
                },
                "beschreibung-versiegelte-flaeche-andere": "Beschreibung Andere",
                "wann-wurde-die-flaeche-versiegelt": {
                    "value": "wann-wurde-die-flaeche-versiegelt-nach-dem-29-sept-2023",
                    "options": [
                        "wann-wurde-die-flaeche-versiegelt-nach-dem-29-sept-2023"
                    ],
                },
            }
        ],
    )
    form_utils.add_answer(
        rpg2_ag_instance.case.work_items.get(task_id="cantonal-exam").document,
        question="kantonale-pruefung-gesuchscodes",
        value=[
            "kantonale-pruefung-gesuchscodes-a02",
            "kantonale-pruefung-gesuchscodes-a01",
        ],
        options=[
            "kantonale-pruefung-gesuchscodes-a02",
            "kantonale-pruefung-gesuchscodes-a01",
        ],
    )
    return rpg2_ag_instance


@pytest.mark.django_db
def test_rpg2_import_success_ag(
    admin_client,
    rpg2_ag_instance_with_answers,
    rpg2_edit_permission,
):
    instance = rpg2_ag_instance_with_answers

    # check get data response
    resp = admin_client.get(reverse("instance-rpg2-data", args=[instance.pk]))
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()["data"]

    assert set(data) == {
        "rpg2-bewilligungsgrund",
        "rpg2-anzahl-neue-gebaeude",
        "rpg2-anzahl-gebaeude-abbruch",
        "rpg2-versiegelt-oder-entsiegelt",
        "rpg2-versiegelte-entsiegelte-flaechen",
    }
    assert data["rpg2-bewilligungsgrund"]["value"] == "rpg2-bewilligungsgrund-a02"
    assert data["rpg2-anzahl-neue-gebaeude"]["value"] == 3
    assert data["rpg2-anzahl-gebaeude-abbruch"]["value"] == 1
    assert (
        data["rpg2-versiegelt-oder-entsiegelt"]["value"]
        == "rpg2-versiegelt-oder-entsiegelt-ja"
    )

    table_rows = data["rpg2-versiegelte-entsiegelte-flaechen"]["value"]
    assert len(table_rows) == 1
    row = table_rows[0]
    assert set(row) == {
        "rpg2-art-versiegelung-entsiegelung",
        "rpg2-flaeche-quadrat-meter",
        "rpg2-materialisierung-neu-versiegelten-flaechen",
        "rpg2-materialisierung-neu-versiegelten-flaechen-beschreibung",
        "rpg2-nutzung-versiegelten-flaechen",
        "rpg2-nutzung-versiegelten-flaechen-beschreibung",
        "rpg2-wann-wurde-flaeche-versiegelt",
    }
    assert row["rpg2-wann-wurde-flaeche-versiegelt"]["value"] == (
        "rpg2-wann-wurde-flaeche-versiegelt-nach-dem-29-sept-2023"
    )
    assert (
        row["rpg2-materialisierung-neu-versiegelten-flaechen-beschreibung"]["value"]
        == "Beschreibung Text"
    )

    # check apply data response
    apply_resp = admin_client.post(reverse("instance-rpg2-apply", args=[instance.pk]))

    assert apply_resp.status_code == status.HTTP_200_OK
    assert set(apply_resp.json()["questions"]) == set(data)

    # check written answers
    rpg2_document = instance.case.work_items.get(task_id="rpg2").document
    answers = rpg2_document.answers
    assert (
        answers.get(question_id="rpg2-bewilligungsgrund").value
        == "rpg2-bewilligungsgrund-a02"
    )
    assert answers.get(question_id="rpg2-anzahl-neue-gebaeude").value == 3
    assert answers.get(question_id="rpg2-anzahl-gebaeude-abbruch").value == 1
    assert (
        answers.get(question_id="rpg2-versiegelt-oder-entsiegelt").value
        == "rpg2-versiegelt-oder-entsiegelt-ja"
    )

    rows = answers.get(
        question_id="rpg2-versiegelte-entsiegelte-flaechen"
    ).documents.all()
    assert rows.count() == 1

    written_row = rows.first()
    assert (
        written_row.answers.get(question_id="rpg2-wann-wurde-flaeche-versiegelt").value
        == "rpg2-wann-wurde-flaeche-versiegelt-nach-dem-29-sept-2023"
    )
    assert (
        written_row.answers.get(
            question_id="rpg2-materialisierung-neu-versiegelten-flaechen-beschreibung"
        ).value
        == "Beschreibung Text"
    )


@pytest.mark.django_db
def test_rpg2_import_get_empty_for_unanswered_source_ag(
    admin_client,
    rpg2_ag_instance,
    rpg2_edit_permission,
):
    get_resp = admin_client.get(
        reverse("instance-rpg2-data", args=[rpg2_ag_instance.pk])
    )
    assert get_resp.status_code == status.HTTP_200_OK
    assert get_resp.json()["data"] == {}


@pytest.mark.parametrize(
    ("denied_access_reason", "expected_status"),
    [
        (None, status.HTTP_200_OK),
        ("disabled", status.HTTP_403_FORBIDDEN),
        ("no_work_item", status.HTTP_403_FORBIDDEN),
        ("no_write_permission", status.HTTP_403_FORBIDDEN),
    ],
)
@pytest.mark.django_db
def test_has_rpg2_edit_permission_ag(
    admin_client,
    rpg2_ag_instance,
    ag_rpg2_settings,
    denied_access_reason,
    mocker,
    expected_status,
):
    has_write_permission = denied_access_reason != "no_write_permission"
    mocker.patch.object(
        CustomPermission,
        "has_camac_edit_permission",
        return_value=has_write_permission,
    )
    if denied_access_reason == "disabled":
        ag_rpg2_settings.enabled = False

    elif denied_access_reason == "no_work_item":
        rpg2_ag_instance.case.work_items.filter(task_id="rpg2").delete()

    get_resp = admin_client.get(
        reverse("instance-rpg2-data", args=[rpg2_ag_instance.pk])
    )
    apply_resp = admin_client.post(
        reverse("instance-rpg2-apply", args=[rpg2_ag_instance.pk])
    )
    assert get_resp.status_code == expected_status
    assert apply_resp.status_code == expected_status


@pytest.fixture
def rpg2_be_instance(
    be_instance,
    be_rpg2_settings,
    be_access_levels,
    admin_client,
    caluma_work_item_factory,
    settings,
):
    call_command("loaddata", settings.ROOT_DIR("kt_bern/config/caluma_rpg2_form.json"))
    _add_rpg2_work_item(be_instance, caluma_work_item_factory, settings)
    # for visibility
    permissions_api.grant(
        be_instance,
        grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
        access_level="distribution-service",
        service=admin_client.user.groups.first().service,
    )

    return be_instance


@pytest.fixture
def rpg2_be_instance_with_answers(rpg2_be_instance, form_utils):
    document = rpg2_be_instance.case.document
    form_utils.add_answer(
        document,
        question="versiegelt-oder-entsiegelt-v7",
        value="versiegelt-oder-entsiegelt-v7-ja",
        options=["versiegelt-oder-entsiegelt-v7-ja"],
    )
    form_utils.add_table_answer(
        document,
        question="versiegelte-entsiegelte-flaechen-v7",
        rows=[
            {
                "art-versiegelung-entsiegelung-v7": {
                    "value": "art-versiegelung-entsiegelung-v7-neue-versiegelte-flaechen",
                    "options": [
                        "art-versiegelung-entsiegelung-v7-neue-versiegelte-flaechen"
                    ],
                },
                "flaeche-quadrat-meter-v7": 250.0,
            },
            {
                "art-versiegelung-entsiegelung-v7": {
                    "value": "art-versiegelung-entsiegelung-v7-entsiegelte-flaechen",
                    "options": [
                        "art-versiegelung-entsiegelung-v7-entsiegelte-flaechen"
                    ],
                },
                "flaeche-quadrat-meter-v7": 100.0,
            },
        ],
    )
    return rpg2_be_instance


@pytest.mark.django_db
def test_rpg2_import_success_be(
    admin_client,
    rpg2_be_instance_with_answers,
    rpg2_edit_permission,
):
    instance = rpg2_be_instance_with_answers

    # check get data response
    resp = admin_client.get(reverse("instance-rpg2-data", args=[instance.pk]))
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()["data"]

    assert set(data) == {
        "rpg2-versiegelt-oder-entsiegelt",
        "rpg2-versiegelte-entsiegelte-flaechen",
    }
    assert (
        data["rpg2-versiegelt-oder-entsiegelt"]["value"]
        == "rpg2-versiegelt-oder-entsiegelt-ja"
    )

    table = data["rpg2-versiegelte-entsiegelte-flaechen"]
    assert table["form"] == "rpg2-versiegelte-entsiegelte-flaechen"
    table_rows = table["value"]
    assert len(table_rows) == 2
    for row in table_rows:
        assert set(row) == {
            "rpg2-art-versiegelung-entsiegelung",
            "rpg2-flaeche-quadrat-meter",
        }

    first_row, second_row = table_rows
    assert first_row["rpg2-art-versiegelung-entsiegelung"]["value"] == (
        "rpg2-art-versiegelung-entsiegelung-neue-versiegelte-flaechen"
    )
    assert first_row["rpg2-flaeche-quadrat-meter"]["value"] == 250.0
    assert second_row["rpg2-art-versiegelung-entsiegelung"]["value"] == (
        "rpg2-art-versiegelung-entsiegelung-entsiegelte-flaechen"
    )
    assert second_row["rpg2-flaeche-quadrat-meter"]["value"] == 100.0

    # check apply data response
    apply_resp = admin_client.post(reverse("instance-rpg2-apply", args=[instance.pk]))
    assert apply_resp.status_code == status.HTTP_200_OK
    assert set(apply_resp.json()["questions"]) == set(data)

    # check written answers
    rpg2_document = instance.case.work_items.get(task_id="rpg2").document
    assert (
        rpg2_document.answers.get(question_id="rpg2-versiegelt-oder-entsiegelt").value
        == "rpg2-versiegelt-oder-entsiegelt-ja"
    )
    rows = rpg2_document.answers.get(
        question_id="rpg2-versiegelte-entsiegelte-flaechen"
    ).documents.all()
    assert rows.count() == 2
    for row in rows:
        assert row.answers.filter(
            question_id="rpg2-art-versiegelung-entsiegelung"
        ).exists()
        assert row.answers.filter(question_id="rpg2-flaeche-quadrat-meter").exists()
