import pytest


@pytest.fixture
def mandatory_answers(db):
    return {"beschreibung-bauvorhaben": "test beschreibung"}
