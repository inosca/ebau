from collections import namedtuple

import pytest

from camac.user.permissions import permission_aware


class FakeView:
    @permission_aware
    def foo(self):
        return "fallback"

    def foo_for_municipality(self):
        return "municipality"

    def foo_for_service(self):
        return "service"


@pytest.mark.parametrize(
    "role,expected",
    [
        ("Municipality", "municipality"),
        ("Service", "service"),
        ("Applicant", "fallback"),
        ("TrustedService", "service"),
    ],
)
def test_permission_aware_decorator(role, expected, mocker):
    Group = namedtuple("Group", "role")
    Role = namedtuple("Role", "name")
    group = Group(Role(role))
    mocker.patch("camac.user.permissions.get_group", return_value=group)
    assert FakeView().foo() == expected
