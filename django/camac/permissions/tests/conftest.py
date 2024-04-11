import pytest

from camac.permissions.models import AccessLevel


@pytest.fixture
def be_access_levels(be_permissions_settings, db, access_level_factory):
    for access_level in be_permissions_settings["ACCESS_LEVELS"]:
        if not AccessLevel.objects.filter(slug=access_level).exists():
            access_level_factory(slug=access_level)
