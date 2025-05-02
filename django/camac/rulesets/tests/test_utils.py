import pytest

from camac.rulesets.utils import assign_responsible_user


@pytest.mark.parametrize(
    "use_case,expected_username",
    [
        ("existing", "existing_user"),
        ("no_permission", None),
        ("no_responsible_user", None),
        ("default", "new_user"),
    ],
)
def test_assign_responsible_user(
    db,
    ag_instance,
    responsible_service_factory,
    user_factory,
    use_case,
    expected_username,
    service,
    mocker,
    caluma_work_item_factory,
):
    existing_user = user_factory(username="existing_user")
    new_user = user_factory(username="new_user")
    assigned_users = []

    permission_mock = mocker.patch(
        "camac.permissions.api.PermissionManager.get_permissions"
    )
    responsible_user_mock = mocker.patch(
        "camac.rulesets.models.ResponsibleUserRuleQuerySet.get_responsible_user_for_instance"
    )

    permission_mock.return_value = ["responsible-read"]
    responsible_user_mock.return_value = new_user

    if use_case == "existing":
        responsible_service_factory(
            instance=ag_instance, service=service, responsible_user=existing_user
        )
        assigned_users = [existing_user.username]
    elif use_case == "no_permission":
        permission_mock.return_value = []
    elif use_case == "no_responsible_user":
        responsible_user_mock.return_value = None

    work_item = caluma_work_item_factory(
        case=ag_instance.case,
        addressed_groups=[str(service.pk)],
        assigned_users=assigned_users,
    )

    assign_responsible_user(ag_instance, service)

    assert (
        ag_instance.responsible_services.filter(service=service)
        .values_list("responsible_user__username", flat=True)
        .first()
        == expected_username
    )

    work_item.refresh_from_db()

    if expected_username is not None:
        assert work_item.assigned_users == [expected_username]
    else:
        assert work_item.assigned_users == []
