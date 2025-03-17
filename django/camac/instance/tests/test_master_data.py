import pytest
from caluma.caluma_workflow import (
    factories as caluma_workflow_factories,
    models as caluma_workflow_models,
)
from django.urls import reverse
from django.utils.translation import override
from pytest_lazy_fixtures import lf
from rest_framework import status
from syrupy.filters import paths

from ..master_data import MasterData


def test_master_data_exceptions(
    db,
    instance,
    instance_with_case,
    master_data_settings,
):
    master_data_settings["CONFIG"] = {
        "bar": ("unconfigured", "bar"),
        "baz": ("case_meta", "baz", {"value_parser": "boolean"}),
        "an_instance_property": ("instance_property", "case__form"),
    }
    instance.case = caluma_workflow_factories.CaseFactory(meta={"baz": True})
    instance.save()
    master_data = MasterData(instance.case)

    with pytest.raises(AttributeError) as e:
        assert master_data.foo

    assert (
        str(e.value)
        == "Key 'foo' is not configured in master data config. Available keys are: bar, baz, an_instance_property"
    )

    with pytest.raises(AttributeError) as e:
        assert master_data.bar

    assert (
        str(e.value)
        == "Resolver 'unconfigured' used in key 'bar' is not defined in master data class"
    )

    with pytest.raises(AttributeError) as e:
        assert master_data.baz

    assert str(e.value) == "Parser 'boolean' is not defined in master data class"

    with pytest.raises(AttributeError) as e:
        assert master_data.an_instance_property

    assert (
        str(e.value)
        == "Instance property lookup failed for lookup `case__form` with 'Case' object has no attribute 'form'."
    )


def test_master_data_parsers(
    db,
    application_settings,
    snapshot,
    form_field_factory,
    instance,
    master_data_is_visible_mock,
    master_data_settings,
    utils,
):
    master_data_settings["CONFIG"] = {
        "date": ("case_meta", "my-date", {"value_parser": "date"}),
        "datetime": ("case_meta", "my-datetime", {"value_parser": "datetime"}),
        "success": (
            "answer",
            "my-success",
            {
                "value_parser": (
                    "value_mapping",
                    {"mapping": {"my-success-yes": True, "my-success-no": False}},
                )
            },
            "multiple-choice",
            {
                "value_parser": (
                    "value_mapping",
                    {
                        "mapping": {
                            "multiple-choice-yes": True,
                            "multiple-choice-no": False,
                        }
                    },
                )
            },
        ),
        "static_value": ("static", "some-value"),
        "my_values": (
            "ng_table",
            ["values-v1", "values-v2"],
            {
                "column_mapping": {
                    "my_static_value": ("static", 3.14),
                    "my_value": "value-single",
                    "my_list": (
                        "list-values",
                        {
                            "value_parser": (
                                "list_mapping",
                                {
                                    "mapping": {
                                        "my_list_value": "value-list",
                                    }
                                },
                            )
                        },
                    ),
                }
            },
        ),
    }

    case = caluma_workflow_factories.CaseFactory(
        meta={"my-date": "2021-08-18", "my-datetime": "2021-08-18T06:58:08.397Z"},
        instance=instance,
    )

    utils.add_answer(case.document, "my-success", "my-success-yes")
    utils.add_answer(
        case.document, "multiple-choice", ["multiple-choice-yes", "multiple-choice-no"]
    )

    form_field_factory(
        instance=instance,
        name="values-v1",
        value=[
            {
                "value-single": 0,
                "list-values": [
                    {"value-list": 1},
                    {"value-list": 2},
                ],
            }
        ],
    )
    form_field_factory(
        instance=instance,
        name="values-v2",
        value=[
            {
                "value-single": 10,
                "list-values": [
                    {"value-list": 11},
                    {"value-list": 12},
                ],
            }
        ],
    )

    master_data = MasterData(case)

    snapshot.assert_match(
        {
            key: getattr(master_data, key)
            for key in master_data_settings["CONFIG"].keys()
        }
    )


@pytest.mark.parametrize(
    "canton_master_data_settings,language,case,select_related,prefetch_related,num_queries",
    [
        pytest.param(
            lf("be_master_data_settings"),
            "de",
            lf("be_master_data_case"),
            ["document"],
            [
                "document__answers",
                "document__answers__question__options",
                "document__answers__answerdocument_set",
                "document__answers__answerdocument_set__document__answers",
                "document__dynamicoption_set",
                "work_items__document__answers",
                "work_items__document__answers__answerdocument_set",
                "work_items__document__answers__answerdocument_set__document__answers",
            ],
            66,
            id="BE DE",
        ),
        pytest.param(
            lf("be_master_data_settings"),
            "fr",
            lf("be_master_data_case"),
            ["document"],
            [
                "document__answers",
                "document__answers__question__options",
                "document__answers__answerdocument_set",
                "document__answers__answerdocument_set__document__answers",
                "document__dynamicoption_set",
                "work_items__document__answers",
                "work_items__document__answers__answerdocument_set",
                "work_items__document__answers__answerdocument_set__document__answers",
            ],
            66,
            id="BE FR",
        ),
        pytest.param(
            lf("ur_master_data_settings"),
            "de",
            lf("ur_master_data_case"),
            ["document", "instance"],
            [
                "document__answers",
                "document__answers__answerdocument_set",
                "document__answers__answerdocument_set__document__answers",
                "document__dynamicoption_set",
                "instance__workflowentry_set",
                "instance__answers",
            ],
            30,
            id="UR",
        ),
        pytest.param(
            lf("sz_master_data_settings"),
            "de",
            lf("sz_master_data_case_gwr"),
            ["instance", "instance__form"],
            ["instance__fields", "instance__workflowentry_set", "work_items"],
            # 1. Query for fetching case
            # 2. Query for prefetching fields
            # 3. Query for prefetching workflow entries
            # 4. Query for prefetching work_items
            # 5. Query for selecting form
            5,
            id="SZ GWR v1",
        ),
        pytest.param(
            lf("sz_master_data_settings"),
            "de",
            lf("sz_master_data_case_gwr_v2"),
            ["instance", "instance__form"],
            ["instance__fields", "instance__workflowentry_set", "work_items"],
            # 1. Query for fetching case
            # 2. Query for prefetching fields
            # 3. Query for prefetching workflow entries
            # 4. Query for prefetching work_items
            # 5. Query for selecting form
            5,
            id="SZ GWR v2",
        ),
        pytest.param(
            lf("so_master_data_settings"),
            "de",
            lf("so_master_data_case"),
            ["document"],
            [
                "document__answers",
                "document__answers__question__options",
                "document__answers__answerdocument_set",
                "document__answers__answerdocument_set__document__answers",
                "document__answers__answerdocument_set__document__answers__question__options",
                "document__dynamicoption_set",
                "work_items__document__answers",
                "work_items__document__answers__answerdocument_set",
                "work_items__document__answers__answerdocument_set__document__answers",
            ],
            38,
            id="SO",
        ),
        pytest.param(
            lf("ag_master_data_settings"),
            "de",
            lf("ag_master_data_case"),
            ["document"],
            [
                "document__answers",
                "document__answers__question__options",
                "document__answers__answerdocument_set",
                "document__answers__answerdocument_set__document__answers",
                "document__answers__answerdocument_set__document__answers__question__options",
                "document__dynamicoption_set",
                "work_items__document__answers",
                "work_items__document__answers__answerdocument_set",
                "work_items__document__answers__answerdocument_set__document__answers",
            ],
            58,
            id="AG",
        ),
    ],
)
def test_master_data(
    db,
    snapshot,
    django_assert_num_queries,
    language,
    case,
    select_related,
    prefetch_related,
    num_queries,
    canton_master_data_settings,
):
    with django_assert_num_queries(num_queries), override(language):
        case = (
            caluma_workflow_models.Case.objects.filter(pk=case.pk)
            .select_related(*select_related)
            .prefetch_related(*prefetch_related)
            .first()
        )

        master_data = MasterData(case)

        assert master_data.to_dict() == snapshot(
            exclude=paths(
                "landowners.0.row_id",
                "applicants.0.row_id",
                "invoice_recipients.0.row_id",
                "project_authors.0.row_id",
            )
        )


@pytest.mark.parametrize("role__name", [("Municipality")])
@pytest.mark.parametrize(
    "query,expected_status",
    [
        ({}, status.HTTP_200_OK),
        ({"fields": "some_property"}, status.HTTP_200_OK),
        ({"fields": "not_configured"}, status.HTTP_400_BAD_REQUEST),
    ],
)
def test_master_data_api(
    db,
    admin_client,
    expected_status,
    instance,
    master_data_settings,
    query,
    snapshot,
):
    master_data_settings["CONFIG"] = {
        "some_property": ("static", "Foo"),
        "some_other_property": ("static", "Bar"),
    }

    response = admin_client.get(
        reverse("instance-master-data", args=[instance.pk]), data=query
    )

    assert response.status_code == expected_status
    assert response.json() == snapshot


@pytest.mark.parametrize(
    "property_name,expected",
    [
        ("caluma_question", "caluma-question"),
        ("caluma_table", "caluma-table"),
        ("ng_question", "ng-question"),
        ("ng_table", "ng-table"),
        ("not_configured", None),
        ("static", None),
        ("case_meta", None),
    ],
)
def test_get_question_slug(master_data_settings, property_name, expected):
    master_data_settings["CONFIG"] = {
        # Question properties
        "caluma_question": ("answer", "caluma-question"),
        "caluma_table": ("table", "caluma-table"),
        "ng_question": ("ng_answer", "ng-question"),
        "ng_table": ("ng_table", "ng-table"),
        # Other properties
        "static": ("static", "foo"),
        "case_meta": ("case_meta", "bar"),
    }

    assert MasterData.get_question_slug(property_name) == expected
