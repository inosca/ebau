import pytest

from camac.constants.kt_bern import SERVICE_GROUP_RSTA

from ..extensions.data_sources import Municipalities, Services


@pytest.mark.parametrize(
    "test_class,service_group_name,expected,is_rsta",
    [
        (
            Municipalities,
            "municipality",
            [[1, "service1"], [2, "service2 (nicht aktiviert)"]],
            True,
        ),
        (Municipalities, "municipality", [[1, "service1"]], False),
        (
            Services,
            "service",
            [["1", "service1"], ["-1", "Andere"]],
            True,
        ),
        (Services, "service", [["1", "service1"], ["-1", "Andere"]], False),
    ],
)
def test_data_sources(
    db,
    service_factory,
    service_group_factory,
    test_class,
    service_group_name,
    expected,
    is_rsta,
):
    if is_rsta:
        sg = service_group_factory(pk=SERVICE_GROUP_RSTA, name=service_group_name)
        service1 = service_factory(
            pk=1, name="service1", disabled=False, service_group=sg
        )
    else:
        service1 = service_factory(
            pk=1,
            name="service1",
            disabled=False,
            service_group__name=service_group_name,
        )
    service_factory(
        pk=2, name="service2", disabled=True, service_group=service1.service_group
    )
    service_factory(pk=3, name="service3", disabled=False, service_group__pk=666)

    data = test_class().get_data(None)

    assert data == expected
