import pytest
from django.http import QueryDict

from camac.gis.clients.base import GISBaseClient
from camac.gis.models import GISDataSource


def test_process_data_source(db, gis_data_source):
    gis_client = GISBaseClient(QueryDict(), GISDataSource.objects.all())

    with pytest.raises(NotImplementedError):
        gis_client.process_data_source(gis_data_source)
