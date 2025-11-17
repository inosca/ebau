from uuid import uuid4

import pytest
from alexandria.core.factories import (
    CategoryFactory,
    DocumentFactory as AlexandriaDocumentFactory,
)
from rest_framework.exceptions import PermissionDenied

from camac.alexandria.permissions import (
    AlexandriaPermissionManager,
)
from camac.permissions.api import P
from camac.permissions.conditions import Always
from camac.permissions.switcher import PERMISSION_MODE
from camac.settings.modules.permissions.alexandria import OwnDocument

# TODO Implement
#
# Idea: a context is always used where the permission manager currently
# uses an instance (or instance id). the context can be subtyped, for
# subtyped instances of the permission manager.
#
# This should allow for sub-permission-managers (module specific managers)
# to define their own, extended context, that their own checks then can
# use.
# The test cases here currently denote some usecases.
#
# Ideally, the contexts can be built up as needed from the environment, but
# should always be strictly+strongly typed, so the checks don't have to
# do too much work to check for incomplete contexts.

TEST_PERMISSIONS = {
    "ACCESS_LEVELS": {
        "geometer": [
            ("category-foo:move", OwnDocument()),
            ("category-foo:create", Always()),
            ("category-foo:update", OwnDocument()),
            ("category-foo:delete", OwnDocument()),
            #
            ("category-bar:move", OwnDocument()),
            ("category-bar:create", OwnDocument()),
            ("category-bar:update", OwnDocument()),
        ]
    }
}


@pytest.fixture
def own_document(admin_user, instance):
    return AlexandriaDocumentFactory(
        title="own document",
        category=CategoryFactory(name="foo"),
        metainfo={"camac-instance-id": str(instance.pk)},
        created_by_user=admin_user.pk,
        modified_by_user=admin_user.pk,
        created_by_group=admin_user.get_default_group().service_id,
        modified_by_group=admin_user.get_default_group().service_id,
    )


@pytest.fixture
def other_document(admin_user, instance):
    user_id = uuid4()
    group_id = uuid4()
    return AlexandriaDocumentFactory(
        title="other service document",
        category=CategoryFactory(name="bar"),
        metainfo={"camac-instance-id": str(instance.pk)},
        created_by_user=user_id,
        modified_by_user=user_id,
        created_by_group=group_id,
        modified_by_group=group_id,
    )


@pytest.mark.parametrize("role__name", ["Geometer"])
def test_permission_manager_context(
    rf,
    be_instance,
    admin_client,
    be_access_levels,
    own_document,
    other_document,
    instance,
    be_permissions_settings,
):
    be_permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.FULL

    request = rf.get("/foo/bar")  # doesn't have to be real
    request.user = admin_client.user
    request.group = admin_client.user.get_default_group()

    apm = AlexandriaPermissionManager.from_request(
        request, permission_settings=TEST_PERMISSIONS
    )
    apm.grant(be_instance, "USER", "geometer", admin_client.user)

    own_scope = apm.scoped_for(own_document)
    other_scope = apm.scoped_for(other_document)
    instance_scope = apm.scoped_for(instance)

    assert own_scope.get_permissions() == [
        "category-bar:create",
        "category-bar:move",
        "category-bar:update",
        "category-foo:create",
        "category-foo:delete",
        "category-foo:move",
        "category-foo:update",
    ]
    assert other_scope.get_permissions() == ["category-foo:create"]
    assert instance_scope.get_permissions() == ["category-foo:create"]

    assert own_scope.has("category-foo:move") is True
    assert other_scope.has("category-foo:move") is False
    assert instance_scope.has("category-foo:move") is False

    with pytest.raises(PermissionDenied):
        other_scope.require("category-foo:move")

    # Attempt a complex "move" operation from foo to bar
    assert own_scope.has(
        P.any("category-foo:move", "category-foo:all")
        & P.any("category-bar:create", "category-bar:all")
    )
