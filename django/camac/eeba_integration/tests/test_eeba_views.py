import pytest
from django.http import response as http_response
from django.urls import reverse
from pytest_lazy_fixtures import lf
from rest_framework import status

from camac.eeba_integration.exceptions import (
    EebaHandlerServerException,
)
from camac.eeba_integration.views import CustomPermission


@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
def test_eeba_check_integration_view_success(
    admin_client,
    mocker,
    gr_instance,
    set_application_gr,
):
    url = reverse("check-eeba-integration", kwargs={"pk": gr_instance.pk})
    dummy_result = {
        "integration_id": "dummy_integration",
        "state": "dummy_state",
        "required": "dummy_required",
        "web_url": "dummy_web_url",
    }
    mocker.patch(
        "camac.eeba_integration.client.EebaHandler.check_eeba_needed",
        return_value=dummy_result,
    )
    response = admin_client.post(url, format="json", data={})

    assert response.status_code == status.HTTP_200_OK
    assert response.data == dummy_result


@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
def test_eeba_check_integration_view_permission_denied(
    admin_client, mocker, gr_instance, set_application_gr
):
    url = reverse("check-eeba-integration", kwargs={"pk": gr_instance.pk})
    mocker.patch.object(
        CustomPermission, "has_camac_edit_permission", return_value=False
    )
    response = admin_client.post(url, format="json", data={})

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
def test_eeba_check_integration_view_instance_not_found(
    admin_client, mocker, gr_instance, set_application_gr
):
    url = reverse("check-eeba-integration", kwargs={"pk": gr_instance.pk})
    mocker.patch(
        "camac.eeba_integration.views.EebaCheckIntegrationView.get_object",
        side_effect=http_response.Http404("No Instance matches the given query."),
    )

    response = admin_client.post(url, format="json", data={})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data == {"error": "No Instance matches the given query."}


@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
def test_eeba_check_integration_view_instance_server_error(
    admin_client, mocker, gr_instance, set_application_gr
):
    url = reverse("check-eeba-integration", kwargs={"pk": gr_instance.pk})
    mocker.patch(
        "camac.eeba_integration.views.EebaCheckIntegrationView.get_object",
        side_effect=EebaHandlerServerException("Test server errror."),
    )

    response = admin_client.post(url, format="json", data={})

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.data == {"error": "An unexpected error occurred."}


@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
def test_eeba_patch_integration_view_missing_new_instance_id(
    admin_client,
    gr_instance,
    set_application_gr,
):
    url = reverse("patch-eeba-integration", kwargs={"pk": gr_instance.pk})
    response = admin_client.patch(url, format="json", data={})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {"error": "new_instance_id is required."}


@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
def test_eeba_patch_integration_view_success(
    admin_client, mocker, gr_instance, set_application_gr
):
    url = reverse("patch-eeba-integration", kwargs={"pk": gr_instance.pk})
    dummy_response = mocker.MagicMock(status_code=status.HTTP_204_NO_CONTENT)
    mocker.patch(
        "camac.eeba_integration.client.EebaHandler.patch_eeba_integration",
        return_value=dummy_response,
    )

    data = {"new_instance_id": "new123"}
    response = admin_client.patch(url, format="json", data=data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {"success": "Integration patched successfully."}


@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
def test_eeba_patch_integration_view_failure(
    admin_client, mocker, gr_instance, set_application_gr
):
    url = reverse("patch-eeba-integration", kwargs={"pk": gr_instance.pk})
    dummy_response = mocker.MagicMock(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    mocker.patch(
        "camac.eeba_integration.client.EebaHandler.patch_eeba_integration",
        return_value=dummy_response,
    )

    data = {"new_instance_id": "new123"}
    response = admin_client.patch(url, format="json", data=data)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.data == {"error": "Integration patching failed."}
