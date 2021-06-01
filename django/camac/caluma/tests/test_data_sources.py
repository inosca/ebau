from collections import namedtuple

import pytest

from ..extensions.countries import COUNTRIES
from ..extensions.data_sources import (
    Authorities,
    Countries,
    Locations,
    Mitberichtsverfahren,
    Municipalities,
    Services,
)


@pytest.mark.parametrize(
    "role,expected_count", [("Portal User", 1), ("Some internal role", 2)]
)
def test_locations(db, role, location_factory, expected_count):
    User = namedtuple("OIDCUser", "camac_role")
    user = User(camac_role=role)

    location_factory(name="Foo", zip=123)
    location_factory(name="Foo", zip=None)

    data = Locations().get_data(user)
    assert len(data) == expected_count


@pytest.mark.parametrize(
    "role,expected_count",
    [("Koordinationsstelle Baugesuche BG", 4), ("Something else", 0)],
)
def test_mitberichtsverfahren(db, role, location_factory, expected_count):
    User = namedtuple("OIDCUser", "camac_role")
    user = User(camac_role=role)

    location_factory(name="Foo", zip=123)
    location_factory(name="Foo", zip=None)

    data = Mitberichtsverfahren().get_data(user)
    assert len(data) == expected_count


@pytest.mark.parametrize(
    "test_class,expected,is_rsta",
    [
        (Authorities, [[1, "Baukommission Altdorf"]], False),
        (Municipalities, [[1, {"de": "Bern", "fr": "Berne"}]], False),
        (
            Municipalities,
            [[2, {"de": "Biel (nicht aktiviert)", "fr": "Bienne (non activé)"}]],
            True,
        ),
        (
            Services,
            [
                ["1", {"de": "Gemeinde Bern", "fr": "Municipalité Berne"}],
                ["3", {"de": "service3", "fr": "service3"}],
                ["4", {"de": "service4", "fr": "service4"}],
                ["-1", {"de": "Andere", "fr": "Autres"}],
            ],
            False,
        ),
        (
            Countries,
            COUNTRIES,
            False,
        ),
    ],
)
def test_data_sources(
    db,
    multilang,
    service_factory,
    service_t_factory,
    service_group_factory,
    test_class,
    expected,
    is_rsta,
    authority_factory,
):
    if is_rsta:
        service1 = service_factory(
            pk=1,
            trans__name="service1",
            trans__language="de",
            disabled=False,
            service_group__name="district",
        )
    else:
        service1 = service_factory(
            pk=1,
            trans__name="Leitbehörde Bern",
            trans__language="de",
            disabled=False,
            service_group__name="municipality",
        )
        service_t_factory(
            service=service1, name="Autorité directrice Berne", language="fr"
        )
        authority_factory(pk=1, name="Baukommission Altdorf")

    service2 = service_factory(
        pk=2,
        trans__name="Leitbehörde Biel",
        trans__language="de",
        disabled=True,
        service_group__name="municipality",
    )
    service_t_factory(
        service=service2, name="Autorité directrice Bienne", language="fr"
    )

    service_factory(
        pk=3,
        trans__name="service3",
        trans__language="de",
        disabled=False,
        service_group__name="district",
    )

    service_factory(
        pk=4,
        trans__name="service4",
        trans__language="de",
        disabled=False,
        service_group__name="service",
    )

    User = namedtuple("OIDCUser", "group")
    user = User(group=service1.pk)

    data = test_class().get_data(user)

    assert data == expected
