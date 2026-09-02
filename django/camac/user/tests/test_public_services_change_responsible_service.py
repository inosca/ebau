from contextlib import nullcontext as no_exception

import pytest
from caluma.caluma_form.models import Form
from django.urls import reverse
from rest_framework import status


@pytest.fixture
def be_services(service_factory):
    for service_group, name in [
        ("municipality", "municipality"),
        ("district", "district"),
        ("lead-service", "lead-service"),
        ("service", "agr-bauen"),
        ("construction-control", "construction-control"),
        ("geometer", "geometer"),
        ("legal-authority", "legal-authority"),
    ]:
        service_factory(
            name=name,
            slug=name,
            service_group__name=service_group,
        )


@pytest.fixture
def ag_services(service_factory):
    for service_group, name in [
        ("municipality", "municipality"),
        ("municipality-light", "municipality-light"),
        ("service-afb", "service-afb"),
        ("service-cantonal", "service-cantonal"),
        ("service-external", "service-external"),
        ("authority-pgv", "authority-pgv"),
    ]:
        service_factory(
            name=name,
            slug=name,
            service_group__name=service_group,
        )


@pytest.mark.parametrize(
    ("service_type", "expected_exception", "expected_service_slugs"),
    [
        pytest.param(
            "municipality",
            no_exception(),
            ["municipality", "district", "lead-service", "agr-bauen"],
            id="service_type_municipality",
        ),
        pytest.param(
            "construction-control",
            no_exception(),
            ["construction-control"],
            id="service_type_construction_control",
        ),
        pytest.param(
            "test",
            pytest.raises(ValueError, match="Invalid responsible service type"),
            [],
            id="service_type_invalid",
        ),
    ],
)
@pytest.mark.django_db
def test_public_service_filter_is_responsible_service_type_be(
    admin_client,
    service_factory,
    be_change_responsible_service_settings,
    be_services,
    service_type,
    expected_exception,
    expected_service_slugs,
):
    with expected_exception:
        query_filters = {"is_responsible_service_type": service_type}
        response = admin_client.get(
            reverse("publicservice-list"),
            data=query_filters,
        )

        assert response.status_code == status.HTTP_200_OK

        data = response.json()["data"]

        assert len(data) == len(expected_service_slugs)
        assert sorted([s["attributes"]["name"] for s in data]) == sorted(
            expected_service_slugs
        )


@pytest.mark.parametrize(
    ("service_type", "expected_exception", "expected_service_slugs"),
    [
        pytest.param(
            "municipality",
            no_exception(),
            ["municipality", "municipality-light", "service-afb"],
            id="service_type_municipality",
        ),
        pytest.param(
            "construction-control",
            pytest.raises(ValueError, match="Invalid responsible service type"),
            [],
            id="service_type_municipality",
        ),
    ],
)
@pytest.mark.django_db
def test_public_service_filter_is_responsible_service_type_ag(
    admin_client,
    service_factory,
    ag_change_responsible_service_settings,
    ag_services,
    service_type,
    expected_exception,
    expected_service_slugs,
):
    with expected_exception:
        query_filters = {"is_responsible_service_type": service_type}
        response = admin_client.get(
            reverse("publicservice-list"),
            data=query_filters,
        )

        assert response.status_code == status.HTTP_200_OK

        data = response.json()["data"]

        assert len(data) == len(expected_service_slugs)
        assert sorted([s["attributes"]["name"] for s in data]) == sorted(
            expected_service_slugs
        )


@pytest.mark.parametrize(
    ("form_slug", "expected_service_slugs"),
    [
        pytest.param(
            "baugesuch",
            ["municipality", "district", "lead-service", "construction-control"],
            id="form_default",
        ),
        pytest.param(
            "baugesuch-v2",
            ["municipality", "district", "lead-service", "construction-control"],
            id="form_default_versioned",
        ),
        pytest.param(
            "antrag-auf-auszahlung",
            [
                "municipality",
                "district",
                "lead-service",
                "agr-bauen",
                "construction-control",
            ],
            id="form_demolition_payment",
        ),
        pytest.param(
            "antrag-auf-auszahlung-v2",
            [
                "municipality",
                "district",
                "lead-service",
                "agr-bauen",
                "construction-control",
            ],
            id="form_demolition_payment_versioned",
        ),
    ],
)
@pytest.mark.django_db
def test_public_service_filter_available_responsible_service_for_instance_be(
    admin_client,
    service_factory,
    caluma_form_factory,
    be_change_responsible_service_settings,
    be_services,
    be_instance,
    form_slug,
    expected_service_slugs,
):
    be_instance.case.document.form = caluma_form_factory(slug=form_slug)
    be_instance.case.document.save()

    query_filters = {"available_responsible_service_for_instance": be_instance.pk}
    response = admin_client.get(
        reverse("publicservice-list"),
        data=query_filters,
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()["data"]

    assert len(data) == len(expected_service_slugs)
    assert sorted([s["attributes"]["name"] for s in data]) == sorted(
        expected_service_slugs
    )


@pytest.mark.parametrize(
    ("form_slug", "expected_service_slugs"),
    [
        pytest.param(
            "baugesuch",
            [],
            id="form_default",
        ),
        pytest.param(
            "baugesuch-v2",
            [],
            id="form_default_versioned",
        ),
        pytest.param(
            "auszahlung-abbruchpraemie",
            ["service-afb"],
            id="form_demolition_payment",
        ),
        pytest.param(
            "auszahlung-abbruchpraemie-v2",
            ["service-afb"],
            id="form_demolition_payment_versioned",
        ),
    ],
)
@pytest.mark.django_db
def test_public_service_filter_available_responsible_service_for_instance_ag(
    admin_client,
    service_factory,
    caluma_form_factory,
    ag_change_responsible_service_settings,
    ag_services,
    ag_instance,
    form_slug,
    expected_service_slugs,
):
    form, _ = Form.objects.get_or_create(pk=form_slug)
    ag_instance.case.document.form = form
    ag_instance.case.document.save()

    query_filters = {"available_responsible_service_for_instance": ag_instance.pk}
    response = admin_client.get(
        reverse("publicservice-list"),
        data=query_filters,
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()["data"]

    assert len(data) == len(expected_service_slugs)
    assert sorted([s["attributes"]["name"] for s in data]) == sorted(
        expected_service_slugs
    )
