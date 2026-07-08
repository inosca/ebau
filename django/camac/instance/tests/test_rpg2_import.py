import pytest

from camac.instance.rpg2_import import (
    RPG2ImportReader,
    RPG2Labeler,
    RPG2Transform,
)
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
