import pytest
from django.http import QueryDict

from camac.gis.clients.base import GISBaseClient
from camac.gis.models import GISConfig


@pytest.fixture
def gis_client(db, gis_config_factory):
    gis_config_factory.create_batch(5)

    return GISBaseClient(QueryDict(), GISConfig.objects.all())


def test_process_config(db, gis_config, gis_client):
    with pytest.raises(NotImplementedError):
        gis_client.process_config(gis_config)


@pytest.mark.parametrize(
    "value,cast,result",
    [
        ("1234", "integer", 1234),
        ("test", "integer", None),
        ("12.4", "float", 12.4),
        ("test", "float", None),
        (123, "string", "123"),
        (1.3, "string", "1.3"),
    ],
)
def test_cast(gis_client, value, cast, result):
    assert gis_client.cast(value, cast) == result
