import pytest
from django.urls import reverse
from rest_framework import status

from camac.constants.kt_gr import ARE_SERVICE_GROUP


@pytest.mark.parametrize(
    "access_level__slug,role__name,service_group__name,expected_count",
    [
        # services can not see any deadline types
        ("distribution-service", "service-lead", "service", 0),
        # municipality can see deadline types
        ("lead-authority", "municipality-lead", "municipality", 3),
        # ARE can see deadline types
        ("lead-authority", "service-lead", ARE_SERVICE_GROUP, 3),
    ],
)
def test_deadline_types_list_gr(
    db,
    admin_client,
    service_factory,
    service,
    deadline_type_factory,
    service_group_factory,
    service_group,
    expected_count,
    access_level,
    role,
    gr_deadlines_settings,
    set_application_gr,
    disable_deadline_side_effects,
):
    """Test the deadline types visibilities for GR."""

    # Visible deadline types
    global_deadline_type = deadline_type_factory()
    service_deadline_type = deadline_type_factory()
    service_deadline_type.services.set([service])
    service_group_deadline_type = deadline_type_factory()
    service_group_deadline_type.service_groups.set([service_group])

    # Not visible deadline types
    other_service_deadline_type = deadline_type_factory()
    other_service_deadline_type.services.set([service_factory()])
    other_service_group_deadline_type = deadline_type_factory()
    other_service_group_deadline_type.service_groups.set([service_group_factory()])

    response = admin_client.get(reverse("deadline-types-list"))

    assert response.status_code == status.HTTP_200_OK
    result = response.json()["data"]
    assert len(result) == expected_count

    if expected_count > 0:
        actual_ids = set([str(r["id"]) for r in result])
        expected_ids = {
            str(global_deadline_type.pk),
            str(service_deadline_type.pk),
            str(service_group_deadline_type.pk),
        }

        assert actual_ids == expected_ids


@pytest.mark.parametrize(
    "access_level__slug,role__name,service_group__name",
    [
        ("lead-authority", "municipality-lead", "municipality"),
    ],
)
@pytest.mark.parametrize(
    "form_slug,expected_count",
    [
        ("baugesuch", 5),
        ("baugesuch-v2", 5),
        ("baugesuch-v3", 2),
        ("bauanzeige", 2),
        ("bauanzeige-v2", 4),
        ("bauanzeige-v3", 2),
        (None, 7),
    ],
)
def test_deadline_types_list_instance_gr(
    db,
    admin_client,
    service_factory,
    service,
    deadline_type_factory,
    service_group_factory,
    instance_factory,
    caluma_case_factory,
    service_group,
    form_slug,
    expected_count,
    access_level,
    role,
    gr_deadlines_settings,
    set_application_gr,
    disable_deadline_side_effects,
):
    """Test the deadline types visibilities for GR."""

    # Baugesuch deadlines
    for _ in range(1, 4):
        deadline_type = deadline_type_factory(form_types=["baugesuch", "baugesuch-v2"])
        deadline_type.service_groups.set([service_group])

    # bauanzeige deadlines
    for _ in range(1, 3):
        deadline_type = deadline_type_factory(
            form_types=["bauanzeige-v2", "bauanzeige-v4"]
        )
        deadline_type.services.set([service])

    # show for all deadline types
    deadline_type_factory(form_types=None)
    deadline_type_factory(form_types=[])

    # Not visible deadline types
    other_service_deadline_type = deadline_type_factory()
    other_service_deadline_type.services.set([service_factory()])
    other_service_group_deadline_type = deadline_type_factory()
    other_service_group_deadline_type.service_groups.set([service_group_factory()])

    instance_case = caluma_case_factory(document__form__pk=form_slug)
    instance = instance_factory(case=instance_case)

    response = admin_client.get(
        reverse("deadline-types-list"),
        {"instance": str(instance.pk) if form_slug else ""},
    )

    assert response.status_code == status.HTTP_200_OK
    result = response.json()["data"]
    assert len(result) == expected_count


@pytest.mark.parametrize(
    "access_level__slug,role__name,service_group__name",
    [("lead-authority", "municipality-lead", "municipality")],
)
@pytest.mark.parametrize(
    "search_name,expected_count",
    [
        # No search term, expect all deadline types
        (None, 3),
        # Search for "G", all visible
        ("G", 3),
        # Search for "Global", all visible
        ("Global", 3),
        # Search for "Global Type", expect "Globaltest" not to match
        ("Global Type", 2),
        # Search for " Type", all visible
        (" Type ", 3),
        # Search specific fro "Type C", only one match
        ("Type C ", 1),
    ],
)
def test_deadline_types_filters(
    db,
    gr_deadlines_settings,
    admin_client,
    deadline_type_factory,
    service_group,
    access_level,
    role,
    search_name,
    expected_count,
    disable_deadline_side_effects,
):
    """Test the deadline types filtering by name."""
    deadline_type_factory(name="Global Type A")
    deadline_type_factory(name="Global Type B")
    deadline_type_factory(name="Globaltest Type C")

    filters = {
        "name": search_name if search_name is not None else "",
    }
    response = admin_client.get(reverse("deadline-types-list"), filters)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()["data"]
    assert len(result) == expected_count
