from itertools import chain

import pytest
from django.urls import reverse
from rest_framework import status

from camac.tests.form_utils import FormUtils
from camac.user.models import Service
from camac.user.utils import get_service_suggestions


@pytest.mark.parametrize(
    (
        "suggestions",
        "suggestion_answer",
        "default_suggestions",
        "expected_services",
    ),
    [
        ({}, [], [], []),
        (
            {"QUESTIONS": {("non-existing-question", "foo"): [0]}},
            [("baubeschrieb", ["baubeschrieb-erweiterung-anbau"])],
            [1111],
            [1111],
        ),
        (
            {"QUESTIONS": {("baubeschrieb", "baubeschrieb-erweiterung-anbau"): [1234]}},
            [("baubeschrieb", ["baubeschrieb-um-ausbau"])],
            [],
            [],
        ),
        (
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
            {"FORM": {"main-form": [20046]}},
            [],
            [],
            [20046],
        ),
    ],
)
@pytest.mark.django_db
def test_suggestion_for_instance_filter_caluma(
    be_instance,
    default_suggestions,
    distribution_settings,
    expected_services,
    form_utils: FormUtils,
    suggestion_answer,
    suggestions,
    django_assert_num_queries,
):
    if default_suggestions:
        distribution_settings["DEFAULT_SUGGESTIONS"] = default_suggestions

    if suggestions:
        distribution_settings["SUGGESTIONS"] = suggestions

        for question, value in suggestion_answer:
            form_utils.add_answer(be_instance.case.document, question, value)

    expected_queries = 1 if default_suggestions or suggestions.get("QUESTIONS") else 0
    with django_assert_num_queries(expected_queries):
        assert get_service_suggestions(be_instance) == set(expected_services)

    with django_assert_num_queries(0):
        assert get_service_suggestions(be_instance) == set(expected_services)


@pytest.mark.parametrize(
    (
        "suggestions",
        "suggestion_answer",
        "default_suggestions",
        "expected_services",
    ),
    [
        (
            {"SUBMODULES": [], "QUESTIONS": []},
            [],
            [],
            [],
        ),
        (
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
@pytest.mark.django_db
def test_suggestion_for_instance_filter_camac_ng(
    default_suggestions,
    distribution_settings,
    expected_services,
    form_factory,
    form_field_factory,
    suggestion_answer,
    suggestions,
    sz_instance,
    django_assert_num_queries,
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

    if suggestions:
        distribution_settings["SUGGESTIONS"] = suggestions

        sz_instance.form = form_factory(name="baugesuch")
        sz_instance.form.family = sz_instance.form
        sz_instance.form.save()
        sz_instance.save()

        for question, value in suggestion_answer:
            form_field_factory(name=question, value=value, instance=sz_instance)

    with django_assert_num_queries(2):
        assert get_service_suggestions(sz_instance) == set(expected_services)

    with django_assert_num_queries(0):
        assert get_service_suggestions(sz_instance) == set(expected_services)


@pytest.mark.parametrize(("form_backend"), ["caluma", "camac-ng"])
@pytest.mark.parametrize(("use_slugs"), [True, False])
@pytest.mark.django_db
def test_suggestion_for_instance_filter_api(
    admin_client,
    application_settings,
    distribution_settings,
    form_backend,
    instance,
    service_factory,
    use_slugs,
):
    expected_services = [
        service_factory(slug="foo"),
        service_factory(slug="bar"),
        service_factory(slug="baz"),
    ]

    application_settings["FORM_BACKEND"] = form_backend
    distribution_settings["DEFAULT_SUGGESTIONS"] = [
        service.slug if use_slugs else service.pk for service in expected_services
    ]

    response = admin_client.get(
        reverse("publicservice-list"),
        {"suggestion_for_instance": instance.pk},
    )

    assert response.status_code == status.HTTP_200_OK

    ids = {int(row["id"]) for row in response.json()["data"]}
    slugs = set(Service.objects.filter(pk__in=ids).values_list("slug", flat=True))

    assert ids == {service.pk for service in expected_services}
    assert slugs == {"foo", "bar", "baz"}


@pytest.mark.parametrize(
    ("is_bab", "is_responsible", "expected_services"),
    [
        (
            False,
            False,
            ["are", "awn", "amz", "anu", "gvg-brandschutz", "pro-infirmis"],
        ),
        (
            False,
            True,
            ["are", "awn", "amz", "anu", "gvg-brandschutz", "pro-infirmis"],
        ),
        (
            True,
            False,
            ["are", "awn", "amz", "anu", "gvg-brandschutz", "pro-infirmis"],
        ),
        # bab + responsible service can only see a limited set of suggestions
        (True, True, ["are", "gvg-brandschutz", "pro-infirmis"]),
    ],
)
@pytest.mark.parametrize(
    ("role__name", "service_group__name"), [("municipality-lead", "municipality")]
)
@pytest.mark.django_db
def test_suggestion_for_instance_filter_caluma_gr(
    admin_client,
    expected_services,
    form_utils: FormUtils,
    gr_distribution_settings,
    gr_instance,
    instance_service_factory,
    is_bab,
    is_responsible,
    service_factory,
    service,
    set_application_gr,
):
    gr_instance.case.meta["is-bab"] = is_bab
    gr_instance.case.save()

    if is_responsible:
        instance_service_factory(instance=gr_instance, service=service, active=1)

    # create all necessary services
    for slug in set(
        chain(
            *[
                chain(*config.values())
                for config in gr_distribution_settings["SUGGESTIONS"].values()
            ]
        )
    ):
        service_factory(slug=slug)

    # create questions/answers to trigger suggestions.
    for question, value in [
        # are
        ("ausserhalb-bauzone", ["ausserhalb-bauzone-ja"]),
        # awn
        ("waldareal", "waldareal-ja"),
        # amz
        ("wohnnutzung", "wohnnutzung-ja"),
        # pro-infirmis
        (
            "mehr-als-vier-wohneinheiten",
            "mehr-als-vier-wohneinheiten-ja",
        ),
        # anu
        (
            "beschreibung-der-nutzung",
            "beschreibung-der-nutzung-abfallanlage",
        ),
        # gvg-brandschutz
        (
            "haustechnische-anlagen-brandschutz",
            "haustechnische-anlagen-brandschutz-ja",
        ),
    ]:
        form_utils.add_answer(gr_instance.case.document, question, value)

    response = admin_client.get(
        reverse("publicservice-list"),
        {"suggestion_for_instance": gr_instance.pk},
    )
    assert response.status_code == status.HTTP_200_OK
    assert {
        str(Service.objects.get(pk=entry["id"]).slug)
        for entry in response.json()["data"]
    } == set(expected_services)
