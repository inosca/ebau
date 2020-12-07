from collections import namedtuple

import pytest

from ..extensions.data_sources import Municipalities, Services


@pytest.mark.parametrize(
    "test_class,expected,is_rsta",
    [
        (Municipalities, [[1, "service1"]], False),
        (
            Municipalities,
            [[2, "service2 (nicht aktiviert)"]],
            True,
        ),
        (
            Services,
            [["1", "service1"], ["3", "service3"], ["4", "service4"], ["-1", "Andere"]],
            True,
        ),
        (
            Services,
            [["1", "service1"], ["3", "service3"], ["4", "service4"], ["-1", "Andere"]],
            False,
        ),
    ],
)
def test_data_sources(
    db,
    service_factory,
    service_group_factory,
    test_class,
    expected,
    is_rsta,
):
    if is_rsta:
        service1 = service_factory(
            pk=1, name="service1", disabled=False, service_group__name="district"
        )

    else:
        service1 = service_factory(
            pk=1,
            name="service1",
            disabled=False,
            service_group__name="municipality",
        )

    service_factory(
        pk=2, name="service2", disabled=True, service_group__name="municipality"
    )
    service_factory(
        pk=3, name="service3", disabled=False, service_group__name="district"
    )
    service_factory(
        pk=4, name="service4", disabled=False, service_group__name="service"
    )

    User = namedtuple("OIDCUser", "group")
    user = User(group=service1.pk)

    data = test_class().get_data(user)

    assert data == expected
