import json
from uuid import uuid4

import pytest
from caluma.caluma_form.models import Form, Question
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status

from camac.utils import build_url


@pytest.fixture
def gis_apply_data(form_question_factory, question_option_factory, caluma_forms_so):
    main_form = Form.objects.get(pk="main-form")
    plot_form = Form.objects.create(slug="parzelle")

    form_question_factory(
        form=plot_form,
        question__slug="e-grid",
        question__type=Question.TYPE_TEXT,
    )

    form_question_factory(
        form=main_form,
        question__slug="ort",
        question__type=Question.TYPE_TEXT,
    )
    form_question_factory(
        form=main_form,
        question__slug="schutzzone",
        question__type=Question.TYPE_MULTIPLE_CHOICE,
    )
    form_question_factory(
        form=main_form,
        question__slug="parzellen",
        question__type=Question.TYPE_TABLE,
        question__row_form=plot_form,
    )

    question_option_factory(question_id="schutzzone", option__slug="schutzzone-ueb")
    question_option_factory(question_id="schutzzone", option__slug="schutzzone-au")

    data = {
        "ort": {
            "hidden": False,
            "label": "Ort",
            "value": "Bern",
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
    requests_mock,
    settings,
    so_instance,
):
    requests_mock.get(
        build_url(settings.API_HOST, f"/api/v1/instances/{so_instance.pk}"),
        json={
            "data": {
                "id": so_instance.pk,
                "type": "instances",
                "meta": {"permissions": {"main": ["write"] if has_permission else []}},
            }
        },
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
        assert set(response.json()["questions"]) == set(data.keys())

        answers = so_instance.case.document.answers.all()

        assert answers.get(question_id="ort").value == "Bern"
        assert answers.get(question_id="ort").meta["gis-value"] == "Bern"

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
