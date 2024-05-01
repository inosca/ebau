import pytest
from django.conf import settings
from django.core.management import call_command

from camac.user.utils import get_support_role


@pytest.mark.django_db
def test_get_support_role(any_application, request, role_factory):
    call_command(
        "loaddata",
        f"{settings.ROOT_DIR(settings.APPLICATION_NAME)}/config/user.json",
    )

    role = get_support_role()
    assert role
