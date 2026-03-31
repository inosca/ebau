import pytest
from django.urls import reverse
from rest_framework import status

from camac.permissions.switcher import PERMISSION_MODE


@pytest.fixture(autouse=True)
def mock_visibility(mocker, permissions_settings):
    """Mock visiblity rules for confirmations and rounds.

    We explicitly bypass any and all visibility rules for the applicant
    confirmations and rounds as those are already tested in
    `test_applicant_confirmations_visibility.py`.
    """

    permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.FULL

    permission_manager_mock = mocker.patch(
        "camac.permissions.api.PermissionManager.filter_queryset",
        side_effect=lambda qs, _: qs,
    )
    confirmation_for_request_mock = mocker.patch(
        "camac.applicants.models.ApplicantConfirmationQuerySet.for_request",
        side_effect=lambda self, _: self,
        autospec=True,
    )
    round_for_request_mock = mocker.patch(
        "camac.applicants.models.ApplicantConfirmationRoundQuerySet.for_request",
        side_effect=lambda self, _: self,
        autospec=True,
    )

    return (
        permission_manager_mock,
        confirmation_for_request_mock,
        round_for_request_mock,
    )


@pytest.mark.parametrize("batch_size", [2, 5])
def test_applicant_confirmation_list(
    db,
    admin_client,
    applicant_confirmation_factory,
    batch_size,
    django_assert_num_queries,
    mock_visibility,
):
    applicant_confirmation_factory.create_batch(batch_size, source_questions__count=2)

    url = reverse("applicant-confirmations-list")

    # Expected queries:
    # 1. user / group / role (middleware)
    # 2. confirmations
    # 3. source questions (prefetch)
    with django_assert_num_queries(3):
        response = admin_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    # Make sure visibility layer was called
    permission_manager_mock, confirmation_for_request_mock, _ = mock_visibility
    assert permission_manager_mock.call_count == 1
    assert confirmation_for_request_mock.call_count == 1


def test_applicant_confirmation_detail(
    db, admin_client, applicant_confirmation_factory
):
    confirmation = applicant_confirmation_factory()

    url = reverse("applicant-confirmations-detail", args=[confirmation.pk])
    response = admin_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    result = response.json()["data"]
    assert result["id"] == str(confirmation.pk)
    assert result["type"] == "applicant-confirmations"
    assert set(result["attributes"].keys()) == {
        "closed-at",
        "created-at",
        "display-name",
        "roles",
        "status",
    }
    assert set(result["relationships"].keys()) == {
        "applicant",
        "round",
        "user",
    }


@pytest.mark.parametrize("batch_size", [2, 5])
def test_applicant_confirmation_round_list(
    db,
    admin_client,
    applicant_confirmation_round_factory,
    batch_size,
    django_assert_num_queries,
    mock_visibility,
):
    confirmations_per_round = 3
    applicant_confirmation_round_factory.create_batch(
        batch_size, confirmations__count=confirmations_per_round
    )

    url = reverse("applicant-confirmation-rounds-list")

    # Expected queries:
    # 1. user / group / role (middleware)
    # 2. rounds
    # 3. confirmations (prefetch)
    with django_assert_num_queries(3):
        response = admin_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == batch_size

    # Make sure visibility layer was called
    permission_manager_mock, _, round_for_request_mock = mock_visibility
    assert permission_manager_mock.call_count == 1
    assert round_for_request_mock.call_count == 1

    # 1. user / group / role (middleware)
    # 2. rounds
    # 3. confirmations (prefetch)
    # 4. applicants of confirmations (prefetch for include)
    # 5. users of confirmations (prefetch for include)
    # 6. source questions of confirmations (prefetch for include)
    with django_assert_num_queries(6):
        response_with_included = admin_client.get(
            url, data={"include": "confirmations"}
        )

    result_with_included = response_with_included.json()
    assert len(result_with_included["data"]) == batch_size
    assert len(result_with_included["included"]) == batch_size * confirmations_per_round


def test_applicant_confirmation_round_detail(
    db, admin_client, applicant_confirmation_round_factory
):
    round = applicant_confirmation_round_factory()

    url = reverse("applicant-confirmation-rounds-detail", args=[round.pk])
    response = admin_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    result = response.json()["data"]
    assert result["id"] == str(round.pk)
    assert result["type"] == "applicant-confirmation-rounds"
    assert set(result["attributes"].keys()) == {
        "closed-at",
        "created-at",
        "status",
        "step",
    }
    assert set(result["relationships"].keys()) == {
        "confirmations",
        "instance",
    }


def test_applicant_confirmation_round_create(
    db,
    admin_client,
    applicant_confirmation_round_factory,
    caluma_document_factory,
    mocker,
):
    document = caluma_document_factory()
    start_mock = mocker.patch(
        "camac.applicants.models.ApplicantConfirmationRoundManager.start_for_document",
        return_value=applicant_confirmation_round_factory(),
    )

    url = reverse("applicant-confirmation-rounds-list")

    bad_response = admin_client.post(url)
    assert bad_response.status_code == status.HTTP_400_BAD_REQUEST

    response = admin_client.post(
        url,
        data={
            "data": {
                "type": "applicant-confirmation-rounds",
                "relationships": {
                    "document": {
                        "data": {
                            "id": str(document.pk),
                            "type": "documents",
                        }
                    }
                },
            }
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert start_mock.call_count == 1
    assert start_mock.call_args[0][0] == document


def test_applicant_confirmation_confirm(
    db, admin_client, applicant_confirmation_factory, mocker
):
    confirmation = applicant_confirmation_factory()
    confirm_mock = mocker.patch(
        "camac.applicants.models.ApplicantConfirmation.confirm",
        return_value=confirmation,
    )

    url = reverse("applicant-confirmations-confirm", args=[confirmation.pk])
    response = admin_client.post(url)

    assert response.status_code == status.HTTP_200_OK
    assert confirm_mock.call_count == 1
    assert response.json()["data"]["id"] == str(confirmation.pk)


@pytest.mark.parametrize("action", ["invalidate", "cancel"])
def test_applicant_confirmation_round_actions(
    db, action, admin_client, applicant_confirmation_round_factory, mocker
):
    round = applicant_confirmation_round_factory()
    action_mock = mocker.patch(
        f"camac.applicants.models.ApplicantConfirmationRound.{action}",
        return_value=round,
    )

    url = reverse(f"applicant-confirmation-rounds-{action}", args=[round.pk])
    response = admin_client.post(url)

    assert response.status_code == status.HTTP_200_OK
    assert action_mock.call_count == 1
    assert response.json()["data"]["id"] == str(round.pk)
