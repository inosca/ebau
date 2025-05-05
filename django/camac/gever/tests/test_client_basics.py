import datetime

import pytest

from camac.gever import apimodels, constants
from camac.gever.client import GEVERClient


@pytest.mark.vcr
def test_auth_and_init(be_gever_settings):
    client = GEVERClient()
    # Yes authentication works
    assert client._token


@pytest.mark.vcr
def test_search_geschaeft(be_gever_settings):
    client = GEVERClient()
    data = client.geschaeft.search_by_tentaql("FULLTEXT[dvo]")
    # We don't expect an actual result from our "random" search
    assert isinstance(data, list)


@pytest.mark.vcr
def test_get_geschaeft_by_uuid(gever_geschaeft_in_cmi, be_gever_settings):
    client = GEVERClient()
    # This GUID is know to currently exist. This is just for development,
    # we don't expect this to be around forever
    data = client.geschaeft.by_guid(gever_geschaeft_in_cmi.guid)
    assert isinstance(data, apimodels.Geschaeft)
    assert isinstance(data.customVerfahrenseingang, datetime.date)
    assert isinstance(data.customVerfahrensende, datetime.date)
    assert isinstance(data.beginn, datetime.date)


def test_template_paths(geschaeft_object_templates):
    slugs = [t.pk for t in geschaeft_object_templates]

    assert sorted(constants.GESCHAEFT_TEMPLATES) == sorted(slugs)
