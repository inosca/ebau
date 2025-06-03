import pytest
from django.urls import reverse
from rest_framework import status


@pytest.fixture
def ag_services(service_factory, service):
    service_factory(
        trans__name="my-subservice",
        service_group=service.service_group,
        service_parent=service,
    )

    for service_group, name in [
        # Restricted AFB services
        ("service-afb", "afb"),
        # Restricted cantonal services
        ("service-cantonal", "agv-bs"),
        ("service-cantonal", "agv-esp"),
        ("service-cantonal", "bks-dp"),
        ("service-cantonal", "bks-ka"),
        ("service-cantonal", "dvi-awa-iga"),
        ("service-cantonal", "amb"),
        ("service-cantonal", "aew"),
        ("service-cantonal", "axpo"),
        ("service-cantonal", "gvm"),
        ("service-cantonal", "dgs-avs-vet"),
        ("service-cantonal", "dgs-avs-lmi"),
        # Unrestricted services
        ("municipality", "some-municipality"),
        ("service-cantonal", "some-cantonal-service"),
        ("service-extra-cantonal", "some-extra-cantonal-service"),
    ]:
        parent_service = service_factory(
            trans__name=name,
            slug=name,
            service_group__name=service_group,
        )

        service_factory(
            trans__name=f"{name}-subservice",
            service_group__name=service_group,
            service_parent=parent_service,
        )


@pytest.mark.parametrize("is_authority", [True, False])
@pytest.mark.parametrize(
    "service_group__name",
    ["municipality", "service-afb", "service-cantonal"],
)
def test_ag_distribution_services(
    db,
    admin_client,
    set_application_ag,
    is_authority,
    mocker,
    service_factory,
    snapshot,
    service,
    ag_distribution_settings,
    ag_services,
    ag_instance,
):
    mocker.patch(
        "camac.instance.models.Instance.responsible_service",
        return_value=service if is_authority else service_factory(),
    )

    response = admin_client.get(
        reverse("publicservice-list"),
        {
            "available_in_distribution_for_instance": ag_instance.pk,
            "exclude_own_service": True,
        },
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()["data"]

    assert set([i["attributes"]["name"] for i in data]) == snapshot
