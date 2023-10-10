import pytest


@pytest.fixture(autouse=True)
def mock_clamd(mocker):
    mocker.patch("django_clamd.validators.validate_file_infection", return_value=None)
