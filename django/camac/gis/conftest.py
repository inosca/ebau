import pytest
from syrupy.filters import props


@pytest.fixture
def mock_municipalities(mocker):
    def mock(names=[]):
        mocker.patch(
            "camac.caluma.extensions.data_sources.Municipalities.get_data",
            return_value=[[i + 1, {"de": name}] for i, name in enumerate(names)],
        )

    return mock


@pytest.fixture
def gis_snapshot(snapshot):
    return snapshot(exclude=props("cache"))
