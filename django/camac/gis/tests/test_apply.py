import json
from uuid import uuid4

import pytest
from caluma.caluma_form.models import Form, Question
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status


@pytest.fixture
def gis_apply_data(
    caluma_form_question_factory,
    caluma_question_option_factory,
    caluma_question_factory,
    caluma_forms_so,
):
    main_form = Form.objects.get(pk="main-form")
    plot_form = Form.objects.create(slug="parzelle")

    # Question exists but is not in the form - should be skipped
    caluma_question_factory(slug="question-not-in-form", type=Question.TYPE_CHOICE)

    caluma_form_question_factory(
        form=plot_form,
        question__slug="e-grid",
        question__type=Question.TYPE_TEXT,
    )

    caluma_form_question_factory(
        form=main_form,
        question__slug="ort",
        question__type=Question.TYPE_TEXT,
    )
    caluma_form_question_factory(
        form=main_form,
        question__slug="plz",
        question__type=Question.TYPE_INTEGER,
    )
    caluma_form_question_factory(
        form=main_form,
        question__slug="flaeche",
        question__type=Question.TYPE_FLOAT,
    )
    caluma_form_question_factory(
        form=main_form,
        question__slug="schutzzone",
        question__type=Question.TYPE_MULTIPLE_CHOICE,
    )
    caluma_form_question_factory(
        form=main_form,
        question__slug="parzellen",
        question__type=Question.TYPE_TABLE,
        question__row_form=plot_form,
    )

    caluma_question_option_factory(
        question_id="schutzzone", option__slug="schutzzone-ueb"
    )
    caluma_question_option_factory(
        question_id="schutzzone", option__slug="schutzzone-au"
    )

    data = {
        "question-not-in-form": {
            "hidden": False,
            "label": "Diese Frage ist nicht in diesem Formular!",
            "value": "Geht nicht",
        },
        "question-does-not-exist": {
            "hidden": False,
            "label": "Diese Frage gibt es nicht!",
            "value": "Geht nicht",
        },
        "ort": {
            "hidden": False,
            "label": "Ort",
            "value": "Bern",
        },
        "flaeche": {
            "hidden": False,
            "label": "Ort",
            "value": 12.8,
        },
        "plz": {
            "hidden": False,
            "label": "Ort",
            "value": 9102,
        },
        "schutzzone": {
            "hidden": False,
            "label": "Schutzzone",
            "value": [
                {"value": "schutzzone-ueb", "displayName": "üB"},
                {"value": "schutzzone-au", "displayName": "Aᵤ"},
            ],
        },
        "parzellen": {
            "form": plot_form.slug,
            "hidden": False,
            "label": "Parzellen",
            "value": [
                {
                    "e-grid": {
                        "label": "EGRID",
                        "value": "CH607506603227",
                    }
                },
                {
                    "e-grid": {
                        "label": "EGRID",
                        "value": "CH607506603233",
                    }
                },
            ],
        },
    }

    key = uuid4()

    cache.set(key, data)

    yield data, key

    cache.delete(key)


@pytest.mark.parametrize(
    "has_permission,has_cache,expected_status",
    [
        (True, True, status.HTTP_201_CREATED),
        (True, False, status.HTTP_400_BAD_REQUEST),
        (False, True, status.HTTP_403_FORBIDDEN),
    ],
)
def test_gis_apply(
    admin_client,
    expected_status,
    gis_apply_data,
    has_cache,
    has_permission,
    mocker,
    settings,
    so_instance,
):
    mocker.patch(
        "camac.instance.serializers.CalumaInstanceSerializer.get_permissions",
        return_value={"main": ["write"] if has_permission else []},
    )

    data, cache_key = gis_apply_data

    if not has_cache:
        cache.delete(cache_key)

    response = admin_client.post(
        reverse("gis-apply"),
        data=json.dumps(
            {
                "cache": str(cache_key),
                "instance": so_instance.pk,
            }
        ),
        content_type="application/json",
    )

    assert response.status_code == expected_status

    if response.status_code == status.HTTP_201_CREATED:
        ignored_keys = {"question-not-in-form", "question-does-not-exist"}

        assert set(response.json()["questions"]) == set(data.keys()) - ignored_keys

        answers = so_instance.case.document.answers.all()

        assert answers.filter(question_id__in=ignored_keys).count() == 0

        assert answers.get(question_id="ort").value == "Bern"
        assert answers.get(question_id="ort").meta["gis-value"] == "Bern"

        assert answers.get(question_id="plz").value == 9102
        assert answers.get(question_id="plz").meta["gis-value"] == 9102

        assert answers.get(question_id="flaeche").value == 12.8
        assert answers.get(question_id="flaeche").meta["gis-value"] == 12.8

        assert answers.get(question_id="schutzzone").value == [
            "schutzzone-ueb",
            "schutzzone-au",
        ]
        assert answers.get(question_id="schutzzone").meta["gis-value"] == [
            "schutzzone-ueb",
            "schutzzone-au",
        ]

        table_answer = answers.get(question_id="parzellen")
        assert table_answer.documents.count() == 2
        assert set(table_answer.documents.values_list("answers__value", flat=True)) == {
            "CH607506603227",
            "CH607506603233",
        }
