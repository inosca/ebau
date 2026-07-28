import pytest
from django.urls import reverse
from pytest_lazy_fixtures import lf
from rest_framework import status


@pytest.mark.parametrize(
    ("role__name", "instance__user"), [("Applicant", lf("admin_user"))]
)
@pytest.mark.django_db
def test_status_timeline(admin_client, instance, mocker, procedure_status_settings):
    steps = {"submit": "running"}
    pending = [{"name": "Some task", "services": ["Some service"]}]
    timeline_mock = mocker.patch(
        "camac.procedure_status.views.get_status_timeline", return_value=steps
    )
    overview_mock = mocker.patch(
        "camac.procedure_status.views.get_pending_work_items_overview",
        return_value=pending,
    )

    response = admin_client.get(reverse("status-timeline-detail", args=[instance.pk]))

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"steps": steps, "pending": pending}

    timeline_mock.assert_called_once_with(instance)
    overview_mock.assert_called_once_with(instance)


@pytest.mark.parametrize(
    ("role__name", "instance__user"), [("Applicant", lf("admin_user"))]
)
@pytest.mark.django_db
def test_disabled_module(admin_client, disable_procedure_status_settings, instance):
    response = admin_client.get(reverse("status-timeline-detail", args=[instance.pk]))

    assert response.status_code == status.HTTP_404_NOT_FOUND
