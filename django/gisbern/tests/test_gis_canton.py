import pytest
from django.urls import reverse


@pytest.fixture(scope="module")
def vcr_config():
    return {
        # add "body" to default match_on because we're passing the
        # egrid number in the body.
        "match_on": ["method", "scheme", "host", "port", "path", "query", "body"],
        "cassette_library_dir": "gisbern/tests/cassettes",
        "decode_compressed_response": True,
    }


@pytest.mark.parametrize(
    "egrid",
    [
        "CH643546955207",
        "CH673533354667",
        "CH851446093521",
        "doesntexist",
        "emptypolygon",
        "emptygis",
    ],
)
@pytest.mark.vcr()
def test_gis_canton(egrid, client, vcr_config, snapshot):
    response = client.get(reverse("egrid", kwargs={"egrid": egrid}))
    snapshot.assert_match(response.json())
