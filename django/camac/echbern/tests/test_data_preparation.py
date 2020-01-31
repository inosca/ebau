from ..data_preparation import get_document
from .caluma_responses import full_document


def test_get_document(requests_mock, snapshot):
    requests_mock.post("http://camac-ng.local/graphql/", json=full_document)
    data = get_document(1, 3, "Bearer")
    snapshot.assert_match(data)
