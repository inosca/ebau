from types import SimpleNamespace

import pytest

from camac.deadlines.mixins import DeadlinePermissionMixin


def make_service(service_group_name):
    return SimpleNamespace(
        service_group=SimpleNamespace(name=service_group_name),
    )


@pytest.mark.parametrize(
    ("service_group_name", "expected_access"),
    [
        ("municipality", True),
        ("service-bab", True),
        ("service", False),
    ],
)
def test_deadline_access_so(
    service_group_name,
    expected_access,
    set_application_so,
    mocker,
):
    mocker.patch(
        "camac.deadlines.mixins.is_module_enabled",
        return_value=True,
    )

    assert (
        DeadlinePermissionMixin().has_deadline_access(make_service(service_group_name))
        is expected_access
    )


def test_service_bab_deadline_access_not_enabled_by_default(
    set_application_test,
    mocker,
):
    mocker.patch(
        "camac.deadlines.mixins.is_module_enabled",
        return_value=True,
    )

    assert not DeadlinePermissionMixin().has_deadline_access(
        make_service("service-bab")
    )
