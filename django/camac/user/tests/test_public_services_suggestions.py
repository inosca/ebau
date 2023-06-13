from itertools import chain

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.fixture
def mock_cache(mocker):
    cached_result = {}

    def cache_set(key, value, timeout):
        cached_result[key] = value

    def cache_get(key):
        return cached_result[key] if key in cached_result else None

    mocker.patch("django.core.cache.cache.set", side_effect=cache_set)
    mocker.patch("django.core.cache.cache.get", side_effect=cache_get)


@pytest.mark.parametrize(
    "num_queries,num_queries_cached,suggestions,suggestion_answer,default_suggestions,expected_services",
    [
        (2, 2, {}, [], [], []),
        (
            6,
            3,
            {"QUESTIONS": {("non-existing-question", "foo"): [0]}},
            [("baubeschrieb", ["baubeschrieb-erweiterung-anbau"])],
            [1111],
            [1111],
        ),
        (
            5,
            2,
            {"QUESTIONS": {("baubeschrieb", "baubeschrieb-erweiterung-anbau"): [1234]}},
            [("baubeschrieb", ["baubeschrieb-um-ausbau"])],
            [],
            [],
        ),
        (
            6,
            3,
            {
                "QUESTIONS": {
                    ("baubeschrieb", "baubeschrieb-erweiterung-anbau"): [1234],
                    ("baubeschrieb", "baubeschrieb-um-ausbau"): [5678],
                    ("non-existing-question", "foo"): [0],
                }
            },
            [("baubeschrieb", ["baubeschrieb-erweiterung-anbau"])],
            [1111],
            [1234, 1111],
        ),
        (
            6,
            3,
            {
                "QUESTIONS": {
                    ("baubeschrieb", "baubeschrieb-erweiterung-anbau"): [1234],
                    ("art-versickerung-dach", "oberflaechengewaesser"): [5678],
                },
            },
            [
                ("baubeschrieb", ["baubeschrieb-erweiterung-anbau"]),
                ("art-versickerung-dach", "oberflaechengewaesser"),
            ],
            [],
            [1234, 5678],
        ),
        (
            6,
            3,
            {
                "QUESTIONS": {
                    ("baubeschrieb", "baubeschrieb-erweiterung-anbau"): [1234, 5678],
                    ("art-versickerung-dach", "some value"): [999],
                    ("non-existing-question", "foo"): [0],
                }
            },
            [
                (
                    "baubeschrieb",
                    ["baubeschrieb-erweiterung-anbau", "baubeschrieb-um-ausbau"],
                ),
                ("art-versickerung-dach", "some value"),
            ],
            [],
            [1234, 5678, 999],
        ),
        (
            5,
            3,
            {"FORM": {"main-form": [20046]}},
            [],
            [],
            [20046],
        ),
    ],
)
def test_suggestion_for_instance_filter_caluma(
    admin_client,
    be_instance,
    service_factory,
    distribution_settings,
    django_assert_num_queries,
    suggestions,
    suggestion_answer,
    default_suggestions,
    expected_services,
    num_queries,
    num_queries_cached,
    mock_cache,
):
    if default_suggestions:
        distribution_settings["DEFAULT_SUGGESTIONS"] = default_suggestions
        for service_id in default_suggestions:
            service_factory(pk=service_id)

    if suggestions:
        distribution_settings["SUGGESTIONS"] = suggestions
        for service_id in set(
            chain(*[chain(*config.values()) for config in suggestions.values()])
        ):
            service_factory(pk=service_id)

        for ans in suggestion_answer:
            be_instance.case.document.answers.create(question_id=ans[0], value=ans[1])

    with django_assert_num_queries(num_queries):
        response = admin_client.get(
            reverse("publicservice-list"),
            {"suggestion_for_instance": be_instance.pk},
        )

    assert response.status_code == status.HTTP_200_OK

    assert set(int(entry["id"]) for entry in response.json()["data"]) == set(
        expected_services
    )

    # Cached service suggestions
    with django_assert_num_queries(num_queries_cached):
        response = admin_client.get(
            reverse("publicservice-list"),
            {"suggestion_for_instance": be_instance.pk},
        )


@pytest.mark.parametrize(
    "num_queries,num_queries_cached,suggestions,suggestion_answer,default_suggestions,expected_services",
    [
        (
            4,
            2,
            {"SUBMODULES": [], "QUESTIONS": []},
            [],
            [],
            [],
        ),
        (
            6,
            3,
            {
                # active (wald-forstlich and wald-auswirkung active)
                "SUBMODULES": [
                    (
                        "fachthemen.wald",
                        [1234],
                    )
                ],
                "QUESTIONS": [],
            },
            [
                ("art-der-nutzung", ["Öffentliche Nutzung", "Forstwirtschaft"]),
                ("baukosten", 20000),
                # active ('Forstwirtschaft' in art-der-nutzung)
                ("wald-forstlich", "Ja"),
                # active (1000 < baukosten)
                ("wald-auswirkungen", "Keine"),
            ],
            [],
            [1234],
        ),
        (
            6,
            3,
            {
                "SUBMODULES": [],
                # not active (wald-auswirkungen not active)
                "QUESTIONS": [
                    (
                        "('Nein' in 'wald-forstlich'|value) && ('Keine' in 'wald-auswirkungen'|value)",
                        [5678],
                    )
                ],
            },
            [
                ("art-der-nutzung", ["Öffentliche Nutzung", "Forstwirtschaft"]),
                ("baukosten", 500),
                # active ('Forstwirtschaft' in art-der-nutzung)
                ("wald-forstlich", "Nein"),
                # not active (1000 > baukosten)
                ("wald-auswirkungen", "Keine"),
            ],
            [4444],
            [4444],
        ),
        (
            6,
            3,
            {
                # active (wald-forstlich active)
                "SUBMODULES": [("fachthemen.wald", [1234])],
                # not active (wald-auswirkungen not active)
                "QUESTIONS": [
                    (
                        "('Nein' in 'wald-forstlich'|value) && ('Keine' in 'wald-auswirkungen'|value)",
                        [5678],
                    )
                ],
            },
            [
                ("art-der-nutzung", ["Öffentliche Nutzung", "Forstwirtschaft"]),
                ("baukosten", 500),
                # active ('Forstwirtschaft' in art-der-nutzung)
                ("wald-forstlich", "Nein"),
                # not active (1000 > baukosten)
                ("wald-auswirkungen", "Keine"),
            ],
            [4444],
            [1234, 4444],
        ),
        (
            6,
            3,
            {
                # active (wald-auswirkungen active)
                "SUBMODULES": [("fachthemen.wald", [1234])],
                # active
                "QUESTIONS": [
                    ("'Keine' in 'wald-auswirkungen'|value", [5678]),
                ],
            },
            [
                ("art-der-nutzung", ["Öffentliche Nutzung"]),
                ("baukosten", 2000),
                # not active ('Forstwirtschaft' not in art-der-nutzung)
                ("wald-forstlich", "Ja"),
                # active (1000 < baukosten)
                ("wald-auswirkungen", "Keine"),
            ],
            [],
            [1234, 5678],
        ),
        (
            6,
            3,
            {
                # not active (wald-auswirkungen and wald-forstlich not active)
                "SUBMODULES": [("fachthemen.wald", [1234])],
                "QUESTIONS": [("'Forstwirtschaft' in 'art-der-nutzung'|value", [5678])],
            },
            [
                ("art-der-nutzung", ["Öffentliche Nutzung"]),
                ("baukosten", 500),
                # not active ('Forstwirtschaft' not in art-der-nutzung)
                ("wald-forstlich", "Ja"),
                # not active (1000 > baukosten)
                ("wald-auswirkungen", "Keine"),
            ],
            [4444],
            [4444],
        ),
    ],
)
def test_suggestion_for_instance_filter_camac_ng(
    admin_client,
    sz_instance,
    service_factory,
    form_field_factory,
    distribution_settings,
    django_assert_num_queries,
    form_factory,
    mock_cache,
    suggestions,
    suggestion_answer,
    default_suggestions,
    expected_services,
    num_queries,
    num_queries_cached,
):
    """Test service suggestions for camac-ng form backends.

    Used question and module configuration:
        "fachthemen.wald": {
            ...
            "parent": "fachthemen",
            "questions": ["wald-forstlich", "wald-auswirkungen"]
        }

        "art-der-nutzung": {
            ...
            "type": "checkbox",
            "config": {
                "options": [
                "Landwirtschaft",
                "Öffentliche Nutzung",
                "Forstwirtschaft"
                ]
            },
        },
        "baukosten": {
            ...
            "type": "number-separator",
            "config": {
                "min": 0
            }
        },
        "wald-forstlich": {
            ...
            "type": "radio",
            "active-expression": "'Forstwirtschaft' in 'art-der-nutzung'|value",
            "config": {
                "options": ["Ja", "Nein"]
            }
        },
        "wald-auswirkungen": {
            ...
            "type": "text",
            "active-expression": "1000 < 'baukosten'|value",
            "config": {}
        }
    """

    if default_suggestions:
        distribution_settings["DEFAULT_SUGGESTIONS"] = default_suggestions
        for service_id in default_suggestions:
            service_factory(pk=service_id)

    if suggestions:
        distribution_settings["SUGGESTIONS"] = suggestions

        sz_instance.form = form_factory(name="baugesuch")
        sz_instance.save()

        for config in [*suggestions["SUBMODULES"], *suggestions["QUESTIONS"]]:
            for service_id in config[1]:
                service_factory(pk=service_id)

        for ans in suggestion_answer:
            form_field_factory(name=ans[0], value=ans[1], instance=sz_instance)

    with django_assert_num_queries(num_queries):
        response = admin_client.get(
            reverse("publicservice-list"),
            {"suggestion_for_instance": sz_instance.pk},
        )

    assert response.status_code == status.HTTP_200_OK

    assert set(int(entry["id"]) for entry in response.json()["data"]) == set(
        expected_services
    )

    # Cached service suggestions
    with django_assert_num_queries(num_queries_cached):
        response = admin_client.get(
            reverse("publicservice-list"),
            {"suggestion_for_instance": sz_instance.pk},
        )
