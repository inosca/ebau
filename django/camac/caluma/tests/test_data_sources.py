import pytest

from ..extensions.data_sources import (
    SERVICE_GROUP_MUNICIPALITY,
    SERVICE_GROUP_SERVICE,
    Municipalities,
    Services,
)


@pytest.mark.parametrize(
    "test_class,service_group_pk,expected",
    [
        (
            Municipalities,
            SERVICE_GROUP_MUNICIPALITY,
            [[1, "service1"], [2, "service2"]],
        ),
        (
            Services,
            SERVICE_GROUP_SERVICE,
            [["1", "service1"], ["2", "service2"], ["-1", "Andere"]],
        ),
    ],
)
def test_data_sources(db, service_factory, test_class, service_group_pk, expected):
    service1 = service_factory(
        pk=1, name="service1", disabled=False, service_group__pk=service_group_pk
    )
    service_factory(
        pk=2, name="service2", disabled=False, service_group=service1.service_group
    )
    service_factory(pk=3, name="service3", disabled=False, service_group__pk=666)

    data = test_class().get_data(None)

    assert data == expected
