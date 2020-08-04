import pytest
from django.core.management import call_command


@pytest.mark.parametrize(
    "user__email,two_users,service__email,user_group__default_group,expect_service_email",
    [
        ("", False, "", 1, ""),
        ("foo@example.com", False, "bar@example.com", 1, "foo@example.com"),
        ("foo@example.com", False, "bar@example.com", 0, "bar@example.com"),
        ("", True, "", 1, "seconduser@example.org"),
        (
            "foo@example.com",
            True,
            "bar@example.com",
            1,
            "foo@example.com,seconduser@example.org",
        ),
        ("foo@example.com", True, "bar@example.com", 0, "seconduser@example.org"),
    ],
)
def test_user_email_to_service(
    db,
    user,
    two_users,
    user_factory,
    user_group_factory,
    user_group,
    service,
    expect_service_email,
):

    if two_users:
        user_group_factory(
            user=user_factory(email="seconduser@example.org"),
            default_group=1,
            group=user_group.group,
        )

    call_command("user_email_to_service")
    service.refresh_from_db()
    assert service.email == expect_service_email
