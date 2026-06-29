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
from camac.settings.modules.permissions.alexandria.conditions import (
    ApplicantFile,
    IsNewDocument,
    OwnDocument,
)

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
            ("category-foo:mark:void", ~ApplicantFile()),
            ("category-foo:create", Always()),
            ("category-foo:update", OwnDocument()),
            ("category-foo:delete", OwnDocument()),
            #
            ("category-bar:move", OwnDocument()),
            ("category-bar:create", OwnDocument(include_subservice=True)),
            ("category-bar:update", OwnDocument(include_subservice=True)),
            #
            ("category-baz:move", OwnDocument(include_subservice=True)),
            (
                "category-baz:create",
                IsNewDocument() | OwnDocument(include_subservice=True),
            ),
            ("category-baz:update", OwnDocument(include_subservice=True)),
        ]
    }
}


@pytest.fixture
def document_owner(admin_user, service_factory, user_group_factory, group_factory):
    """Set up a subservice for the default admin user."""
    subservice = service_factory(name="own subservice")
    subservice_group = group_factory(service=subservice)
    subservice.groups.set([subservice_group])
    user_group_factory(group=subservice_group, user=admin_user, default_group=0)

    default_group = admin_user.get_default_group()
    default_service = default_group.service

    subservice.service_parent = default_service
    subservice.save()

    return admin_user, subservice, default_group, subservice_group


@pytest.fixture
def own_document(document_owner, instance):
    admin_user, _, default_group, _ = document_owner
    return AlexandriaDocumentFactory(
        title="own document",
        category=CategoryFactory(name="foo"),
        metainfo={"camac-instance-id": str(instance.pk)},
        created_by_user=str(admin_user.pk),
        modified_by_user=str(admin_user.pk),
        created_by_group=str(default_group.service_id),
        modified_by_group=str(default_group.service_id),
    )


@pytest.fixture
def applicant_document(instance):
    user_id = "3"
    return AlexandriaDocumentFactory(
        title="other service document",
        category=CategoryFactory(name="bar"),
        metainfo={"camac-instance-id": str(instance.pk)},
        created_by_user=user_id,
        modified_by_user=user_id,
        created_by_group=None,
        modified_by_group=None,
    )


@pytest.fixture
def subservice_document(document_owner, instance):
    admin_user, _, _, subservice_group = document_owner
    return AlexandriaDocumentFactory(
        title="subservice document",
        category=CategoryFactory(name="foo"),
        metainfo={"camac-instance-id": str(instance.pk)},
        created_by_user=str(admin_user.pk),
        modified_by_user=str(admin_user.pk),
        created_by_group=str(subservice_group.service_id),
        modified_by_group=str(subservice_group.service_id),
    )


@pytest.fixture
def other_document(instance):
    user_id = "1"
    group_id = "2"
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
    document_owner,
    be_access_levels,
    own_document,
    applicant_document,
    subservice_document,
    other_document,
    instance,
    be_permissions_settings,
):
    be_permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.FULL

    admin_user, _, default_group, subservice_group = document_owner

    request = rf.get("/foo/bar")  # doesn't have to be real
    request.user = admin_user
    request.group = default_group

    apm = AlexandriaPermissionManager.from_request(
        request, permission_settings=TEST_PERMISSIONS
    )
    apm.grant(be_instance, "USER", "geometer", admin_client.user)

    own_scope = apm.scoped_for(own_document)
    applicant_scope = apm.scoped_for(applicant_document)
    subservice_scope = apm.scoped_for(subservice_document)
    other_scope = apm.scoped_for(other_document)
    instance_scope = apm.scoped_for(instance)

    # permissions for default service on own scope/document.
    assert own_scope.get_permissions() == [
        "category-bar:create",
        "category-bar:move",
        "category-bar:update",
        "category-baz:create",
        "category-baz:move",
        "category-baz:update",
        "category-foo:create",
        "category-foo:delete",
        "category-foo:mark:void",
        "category-foo:move",
        "category-foo:update",
    ]
    # permissions for default service on applicant scope/document.
    assert applicant_scope.get_permissions() == [
        "category-foo:create",
    ]
    # permissions for default service on subservice scope/document.
    assert subservice_scope.get_permissions() == [
        "category-bar:create",
        "category-bar:update",
        "category-baz:create",
        "category-baz:move",
        "category-baz:update",
        "category-foo:create",
        "category-foo:mark:void",
    ]
    assert other_scope.get_permissions() == [
        "category-foo:create",
        "category-foo:mark:void",
    ]
    assert instance_scope.get_permissions() == [
        "category-baz:create",
        "category-foo:create",
        "category-foo:mark:void",
    ]

    assert own_scope.has("category-foo:move") is True
    assert own_scope.has("category-foo:mark:void") is True
    assert applicant_scope.has("category-foo:mark:void") is False
    assert subservice_scope.has("category-foo:move") is False
    assert subservice_scope.has("category-bar:update") is True
    assert other_scope.has("category-foo:move") is False
    assert instance_scope.has("category-foo:move") is False

    with pytest.raises(PermissionDenied):
        other_scope.require("category-foo:move")

    with pytest.raises(PermissionDenied):
        subservice_scope.require("category-foo:move")

    # Attempt a complex "move" operation
    assert own_scope.has(
        P.any("category-foo:move", "category-foo:all")
        & P.any("category-bar:create", "category-bar:all")
    )
    assert subservice_scope.has(
        P.any("category-baz:move", "category-baz:all")
        & P.any("category-bar:create", "category-bar:all")
    )

    # check subservice permissions
    request.group = subservice_group
    apm_subservice = AlexandriaPermissionManager.from_request(
        request, permission_settings=TEST_PERMISSIONS
    )
    apm_subservice.grant(be_instance, "USER", "geometer", admin_client.user)
    subservice_parent_scope = apm_subservice.scoped_for(own_document)
    subservice_own_scope = apm_subservice.scoped_for(subservice_document)

    # permissions for subservice on parent service owned document.
    assert subservice_parent_scope.get_permissions() == [
        "category-bar:create",
        "category-bar:update",
        "category-baz:create",
        "category-baz:move",
        "category-baz:update",
        "category-foo:create",
        "category-foo:mark:void",
    ]
    # permissions for subservice on own scope/document.
    assert subservice_own_scope.get_permissions() == [
        "category-bar:create",
        "category-bar:move",
        "category-bar:update",
        "category-baz:create",
        "category-baz:move",
        "category-baz:update",
        "category-foo:create",
        "category-foo:delete",
        "category-foo:mark:void",
        "category-foo:move",
        "category-foo:update",
    ]
