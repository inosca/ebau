import pytest
import vcr
from django.urls import reverse

my_vcr = vcr.VCR(
    # add "body" to default match_on because we're passing the
    # egrid number in the body.
    match_on=["method", "scheme", "host", "port", "path", "query", "body"],
    cassette_library_dir="gisbern/tests/cassettes",
    decode_compressed_response=True,
)


@pytest.mark.parametrize(
    "egrid", ["CH643546955207", "CH673533354667", "CH851446093521", "doesntexist"]
)
def test_gis_canton(egrid, client, snapshot):
    with my_vcr.use_cassette(egrid + ".yml"):
        response = client.get(reverse("egrid", kwargs={"egrid": egrid}))
        snapshot.assert_match(response.json())
