import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize(
    "role__name,expected_count",
    [("Applicant", 0), ("Service", 3)],
)
@pytest.mark.django_db
def test_billing_entry_template_list(
    admin_client,
    billing_v2_entry_template_factory,
    expected_count,
    service_factory,
    service_group_factory,
    service_group,
    service,
):
    # Visible templates
    global_template = billing_v2_entry_template_factory()
    service_template = billing_v2_entry_template_factory()
    service_template.services.set([service])
    service_group_template = billing_v2_entry_template_factory()
    service_group_template.service_groups.set([service_group])

    # Not visible templates
    other_service_template = billing_v2_entry_template_factory()
    other_service_template.services.set([service_factory()])
    other_service_group_template = billing_v2_entry_template_factory()
    other_service_group_template.service_groups.set([service_group_factory()])

    response = admin_client.get(reverse("billing-v2-entry-template-list"))

    assert response.status_code == status.HTTP_200_OK
    result = response.json()["data"]
    assert len(result) == expected_count

    if expected_count > 0:
        actual_ids = set([str(r["id"]) for r in result])
        expected_ids = {
            str(global_template.pk),
            str(service_template.pk),
            str(service_group_template.pk),
        }

        assert actual_ids == expected_ids
