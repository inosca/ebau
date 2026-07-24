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
    ("role__name", "expected"),
    [
        ("Municipality", "municipality"),
        ("Service", "service"),
        ("Applicant", "fallback"),
        ("TrustedService", "service"),
    ],
)
@pytest.mark.django_db
def test_permission_aware_decorator(group, expected, mocker):
    mocker.patch("camac.user.permissions.get_group", return_value=group)
    assert FakeView().foo() == expected
