import pytest
import vcr
from django.urls import reverse


@vcr.use_cassette()
@pytest.mark.parametrize("egrid", ["CH643546955207"])
def test_gis_canton(egrid, client, snapshot):
    response = client.get(reverse("egrid", kwargs={"egrid": egrid}))
    snapshot.assert_match(response.json())
