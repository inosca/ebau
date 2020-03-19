import pytest

from ..extensions.data_sources import Municipalities, Services


@pytest.mark.parametrize(
    "test_class,service_group_name,expected",
    [
        (Municipalities, "municipality", [[1, "service1"], [2, "service2"]]),
        (Services, "service", [["1", "service1"], ["2", "service2"], ["-1", "Andere"]]),
    ],
)
def test_data_sources(db, service_factory, test_class, service_group_name, expected):
    service1 = service_factory(
        pk=1, name="service1", disabled=False, service_group__name=service_group_name
    )
    service_factory(
        pk=2, name="service2", disabled=False, service_group=service1.service_group
    )
    service_factory(pk=3, name="service3", disabled=False, service_group__pk=666)

    data = test_class().get_data(None)

    assert data == expected
