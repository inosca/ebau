import json

import pytest
from django.urls import reverse
from pytest_lazy_fixtures import lf
from rest_framework import status

from camac.eeba_integration.exceptions import (
    EebaHandlerBadRequestException,
    EebaHandlerServerException,
)


@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
def test_integration_create(
    admin_client,
    mocker,
    gr_instance,
    set_application_gr,
):
    url = reverse("eeba-integration-create", args=[gr_instance.pk])
    mocker.patch(
        "camac.eeba_integration.views.EebaHandler.create_eeba_integration",
        return_value={"integration_id": "35374476-0694-42ed-84d4-8da544d0a60e"},
    )
    response = admin_client.post(url, data={})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"integration_id": "35374476-0694-42ed-84d4-8da544d0a60e"}


@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
def test_integration_create_server_error(
    admin_client, mocker, gr_instance, set_application_gr
):
    url = reverse("eeba-integration-create", args=[gr_instance.pk])
    mocker.patch(
        "camac.eeba_integration.views.EebaHandler.create_eeba_integration",
        side_effect=EebaHandlerServerException("Creation server error"),
    )
    response = admin_client.post(url, data={})
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Creation server error" in response.json().get("error", "")


@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
def test_integration_check(
    admin_client, mocker, gr_instance, set_application_gr, dummy_get_response_data
):
    integration_id = "35374476-0694-42ed-84d4-8da544d0a60e"
    url = reverse("eeba-integration-detail", args=[gr_instance.pk, integration_id])
    mocker.patch(
        "camac.eeba_integration.views.EebaHandler.check_eeba_needed",
        return_value=dummy_get_response_data,
    )
    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == dummy_get_response_data


@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
def test_integration_check_bad_request(
    admin_client, mocker, gr_instance, set_application_gr
):
    integration_id = "35374476-0694-42ed-84d4-8da544d0a60e"
    url = reverse("eeba-integration-detail", args=[gr_instance.pk, integration_id])
    mocker.patch(
        "camac.eeba_integration.views.EebaHandler.check_eeba_needed",
        side_effect=EebaHandlerBadRequestException("Check bad request error"),
    )
    response = admin_client.get(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Check bad request error" in response.json().get("error", "")


@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
def test_integration_check_server_error(
    admin_client, mocker, gr_instance, set_application_gr
):
    integration_id = "35374476-0694-42ed-84d4-8da544d0a60e"
    url = reverse("eeba-integration-detail", args=[gr_instance.pk, integration_id])
    mocker.patch(
        "camac.eeba_integration.views.EebaHandler.check_eeba_needed",
        side_effect=EebaHandlerServerException("Check server error"),
    )
    response = admin_client.get(url)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Check server error" in response.json().get("error", "")


@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
def test_integration_patch(admin_client, mocker, gr_instance, set_application_gr):
    integration_id = "35374476-0694-42ed-84d4-8da544d0a60e"
    url = reverse("eeba-integration-detail", args=[gr_instance.pk, integration_id])
    payload = {"new_instance_id": 789}
    mocker.patch(
        "camac.eeba_integration.views.EebaHandler.patch_eeba_integration",
        return_value={},
    )
    response = admin_client.patch(
        url, data=json.dumps(payload), content_type="application/json"
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {}


@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
def test_integration_patch_missing_new_instance_id(
    admin_client, mocker, gr_instance, set_application_gr
):
    integration_id = "35374476-0694-42ed-84d4-8da544d0a60e"
    url = reverse("eeba-integration-detail", args=[gr_instance.pk, integration_id])
    response = admin_client.patch(url, data={}, content_type="application/json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "new_instance_id is required" in response.json().get("error", "")


@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
def test_integration_patch_bad_request(
    admin_client, mocker, gr_instance, set_application_gr
):
    integration_id = "35374476-0694-42ed-84d4-8da544d0a60e"
    url = reverse("eeba-integration-detail", args=[gr_instance.pk, integration_id])
    payload = {"new_instance_id": 678}
    mocker.patch(
        "camac.eeba_integration.views.EebaHandler.patch_eeba_integration",
        side_effect=EebaHandlerBadRequestException("Patch bad request error"),
    )
    response = admin_client.patch(
        url, data=json.dumps(payload), content_type="application/json"
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Patch bad request error" in response.json().get("error", "")


@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
def test_integration_patch_server_error(
    admin_client, mocker, gr_instance, set_application_gr
):
    integration_id = "35374476-0694-42ed-84d4-8da544d0a60e"
    url = reverse("eeba-integration-detail", args=[gr_instance.pk, integration_id])
    payload = {"new_instance_id": 678}
    mocker.patch(
        "camac.eeba_integration.views.EebaHandler.patch_eeba_integration",
        side_effect=EebaHandlerServerException("Patch server error"),
    )
    response = admin_client.patch(
        url, data=json.dumps(payload), content_type="application/json"
    )
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Patch server error" in response.json().get("error", "")


@pytest.mark.parametrize("retry_action", ["retry", "rerun"])
@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
def test_integration_retry(
    admin_client,
    mocker,
    gr_instance,
    set_application_gr,
    retry_action,
    dummy_get_response_data,
):
    integration_id = "35374476-0694-42ed-84d4-8da544d0a60e"
    url = reverse(
        "eeba-integration-retry", args=[gr_instance.pk, integration_id, retry_action]
    )
    mocker.patch(
        "camac.eeba_integration.views.EebaHandler.retry_eeba_check",
        return_value=dummy_get_response_data,
    )
    response = admin_client.post(url, data={})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == dummy_get_response_data


@pytest.mark.parametrize("retry_action", ["retry", "rerun"])
@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
def test_integration_retry_bad_request(
    admin_client, mocker, gr_instance, retry_action, set_application_gr
):
    integration_id = "35374476-0694-42ed-84d4-8da544d0a60e"
    url = reverse(
        "eeba-integration-retry", args=[gr_instance.pk, integration_id, retry_action]
    )
    mocker.patch(
        "camac.eeba_integration.views.EebaHandler.retry_eeba_check",
        side_effect=EebaHandlerBadRequestException("Retry bad request error"),
    )
    response = admin_client.post(url, data={})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Retry bad request error" in response.json().get("error", "")


@pytest.mark.parametrize("retry_action", ["retry", "rerun"])
@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
def test_integration_retry_server_error(
    admin_client, mocker, gr_instance, retry_action, set_application_gr
):
    integration_id = "35374476-0694-42ed-84d4-8da544d0a60e"
    url = reverse(
        "eeba-integration-retry", args=[gr_instance.pk, integration_id, retry_action]
    )
    mocker.patch(
        "camac.eeba_integration.views.EebaHandler.retry_eeba_check",
        side_effect=EebaHandlerServerException("Retry server error"),
    )
    response = admin_client.post(url, data={})
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Retry server error" in response.json().get("error", "")


@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
def test_invalid_post_request(admin_client, gr_instance, set_application_gr):
    # test the POST endpoint when an integration_id is provided but no retry_action.
    integration_id = "35374476-0694-42ed-84d4-8da544d0a60e"
    url = reverse("eeba-integration-detail", args=[gr_instance.pk, integration_id])
    response = admin_client.post(
        url, data=json.dumps({}), content_type="application/json"
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["error"] == "Invalid POST request."


@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
def test_invalid_get_request(admin_client, gr_instance, set_application_gr):
    # test the GET endpoint when integration_id is missing in the URL.
    url = reverse("eeba-integration-create", args=[gr_instance.pk])
    response = admin_client.get(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["error"] == "Invalid GET request."


@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
def test_invalid_patch_request_missing_integration_id(
    admin_client, gr_instance, set_application_gr
):
    # test the PATCH endpoint when integration_id is missing in the URL.
    url = reverse("eeba-integration-create", args=[gr_instance.pk])
    payload = {"new_instance_id": "new-test-instance"}
    response = admin_client.patch(
        url, data=json.dumps(payload), content_type="application/json"
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["error"] == "Invalid PATCH request."
