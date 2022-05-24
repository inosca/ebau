import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize(
    "suggestions,suggestion_answer,default_suggestions,expected_services",
    [
        ([], [], [], []),
        (
            [("non-existing-question", "foo", [0])],
            [("baubeschrieb", ["baubeschrieb-erweiterung-anbau"])],
            [1111],
            [1111],
        ),
        (
            [("baubeschrieb", "baubeschrieb-erweiterung-anbau", [1234])],
            [("baubeschrieb", ["baubeschrieb-um-ausbau"])],
            [],
            [],
        ),
        (
            [
                ("baubeschrieb", "baubeschrieb-erweiterung-anbau", [1234]),
                ("baubeschrieb", "baubeschrieb-um-ausbau", [5678]),
                ("non-existing-question", "foo", [0]),
            ],
            [("baubeschrieb", ["baubeschrieb-erweiterung-anbau"])],
            [1111],
            [1234, 1111],
        ),
        (
            [
                ("baubeschrieb", "baubeschrieb-erweiterung-anbau", [1234]),
                ("art-versickerung-dach", "oberflaechengewaesser", [5678]),
            ],
            [
                ("baubeschrieb", ["baubeschrieb-erweiterung-anbau"]),
                ("art-versickerung-dach", "oberflaechengewaesser"),
            ],
            [],
            [1234, 5678],
        ),
        (
            [
                ("baubeschrieb", "baubeschrieb-erweiterung-anbau", [1234, 5678]),
                ("art-versickerung-dach", "some value", [999]),
                ("non-existing-question", "foo", [0]),
            ],
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
    ],
)
def test_suggestion_for_instance_filter(
    admin_client,
    be_instance,
    service_factory,
    distribution_settings,
    suggestions,
    suggestion_answer,
    default_suggestions,
    expected_services,
):

    if default_suggestions:
        distribution_settings["DEFAULT_SUGGESTIONS"] = default_suggestions
        for service_id in default_suggestions:
            service_factory(pk=service_id)

    if suggestions:
        distribution_settings["SUGGESTIONS"] = suggestions
        for config in suggestions:
            for service_id in config[2]:
                service_factory(pk=service_id)

        for ans in suggestion_answer:
            be_instance.case.document.answers.create(question_id=ans[0], value=ans[1])

    response = admin_client.get(
        reverse("publicservice-list"), {"suggestion_for_instance": be_instance.pk}
    )

    assert response.status_code == status.HTTP_200_OK

    assert set(int(entry["id"]) for entry in response.json()["data"]) == set(
        expected_services
    )
