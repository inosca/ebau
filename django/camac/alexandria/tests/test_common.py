import pytest

from camac.alexandria.extensions.common import (
    get_permission_key,
    has_alexandria_create_permission,
    has_alexandria_delete_permission,
    has_alexandria_mark_permission,
    has_alexandria_move_permission,
)
from camac.permissions.api import GRANT_CHOICES, grant
from camac.permissions.conditions import Always, Never
from camac.permissions.switcher import PERMISSION_MODE


@pytest.mark.parametrize(
    (
        "use_role_permission_mapping",
        "append_role",
        "service_group__name",
        "role__name",
        "expected_permission_key",
    ),
    [
        (False, False, "service-cantonal", "service-lead", "cantonal"),
        (False, False, "service-cantonal", "subservice", "cantonal"),
        (False, False, "municipality", "municipality-lead", "municipality-lead"),
        (False, False, "municipality", "subservice", "subservice"),
        (False, True, "service-cantonal", "service-lead", "cantonal-service-lead"),
        (False, True, "service-cantonal", "subservice", "cantonal-subservice"),
        (False, True, "municipality", "municipality-lead", "municipality-lead"),
        (False, True, "municipality", "subservice", "subservice"),
        (True, False, "service-cantonal", "service-lead", "cantonal"),
        (True, False, "service-cantonal", "subservice", "cantonal"),
        (True, False, "municipality", "municipality-lead", "municipality"),
        (True, False, "municipality", "subservice", "service"),
        (True, True, "service-cantonal", "service-lead", "cantonal-service"),
        (True, True, "service-cantonal", "subservice", "cantonal-service"),
        (True, True, "municipality", "municipality-lead", "municipality"),
        (True, True, "municipality", "subservice", "service"),
    ],
)
def test_get_permission_key(
    db,
    alexandria_settings,
    append_role,
    application_settings,
    expected_permission_key,
    group,
    use_role_permission_mapping,
):
    application_settings["ROLE_PERMISSIONS"] = {
        "service-lead": "service",
        "subservice": "service",
        "municipality-lead": "municipality",
    }

    alexandria_settings["PERMISSION_KEY"] = {
        "SERVICE_GROUP_MAPPING": {"service-cantonal": "cantonal"},
        "SERVICE_GROUP_APPEND_ROLE": append_role,
        "USE_ROLE_PERMISSIONS_MAPPING": use_role_permission_mapping,
    }

    assert get_permission_key(group) == expected_permission_key


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_has_alexandria_permission_v1(
    db,
    alexandria_category_factory,
    alexandria_document_factory,
    alexandria_settings,
    fake_request,
    instance,
):
    alexandria_settings["USE_V2_PERMISSIONS"] = False

    allowed_category = alexandria_category_factory(
        metainfo={
            "access": {
                "Municipality": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "scope": "All",
                            "permission": "create",
                        },
                        {
                            "scope": "All",
                            "permission": "delete",
                        },
                        {
                            "scope": "All",
                            "marks": ["void"],
                            "fields": ["marks"],
                            "permission": "update",
                        },
                    ],
                }
            }
        }
    )
    disallowed_category = alexandria_category_factory()
    allowed_document = alexandria_document_factory(
        metainfo={"camac-instance-id": instance.pk},
        category=allowed_category,
    )
    disallowed_document = alexandria_document_factory(
        metainfo={"camac-instance-id": instance.pk},
        category=disallowed_category,
    )

    # allowed category / document
    assert (
        has_alexandria_create_permission(fake_request, instance, allowed_category)
        is True
    )
    assert has_alexandria_delete_permission(fake_request, allowed_document) is True
    assert (
        has_alexandria_mark_permission(fake_request, allowed_document, "void") is True
    )

    # disallowed category / document
    assert (
        has_alexandria_create_permission(fake_request, instance, disallowed_category)
        is False
    )
    assert has_alexandria_delete_permission(fake_request, disallowed_document) is False
    assert (
        has_alexandria_mark_permission(fake_request, disallowed_document, "void")
        is False
    )


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize(
    ("marks", "from_permission", "to_permission", "expected"),
    [
        # no permissions, denied
        ([], [], [], False),
        # target misses create permission
        (
            [],
            [{"scope": "All", "permission": "update"}],
            [],
            False,
        ),
        # allowed move without marks
        (
            [],
            [{"scope": "All", "permission": "update"}],
            [{"scope": "All", "permission": "create"}],
            True,
        ),
        # target allows marks, but misses decison mark, denied
        (
            ["void", "decision"],
            [{"scope": "All", "permission": "update"}],
            [
                {"scope": "All", "permission": "create"},
                {"scope": "All", "marks": ["void"], "permission": "update"},
            ],
            False,
        ),
        # target allows the required marks, allowed
        (
            ["void", "decision"],
            [{"scope": "All", "permission": "update"}],
            [
                {"scope": "All", "permission": "create"},
                {"scope": "All", "marks": ["void", "decision"], "permission": "update"},
            ],
            True,
        ),
        # target allows the required marks, but not the marks field, denied
        (
            ["void", "decision"],
            [{"scope": "All", "permission": "update"}],
            [
                {"scope": "All", "permission": "create"},
                {
                    "scope": "All",
                    "fields": ["title"],
                    "marks": ["void", "decision"],
                    "permission": "update",
                },
            ],
            False,
        ),
    ],
)
def test_has_alexandria_move_permission_v1(
    db,
    alexandria_category_factory,
    alexandria_document_factory,
    alexandria_mark_factory,
    alexandria_settings,
    fake_request,
    instance,
    marks,
    from_permission,
    to_permission,
    expected,
):
    alexandria_settings["USE_V2_PERMISSIONS"] = False

    for mark in marks:
        alexandria_mark_factory(pk=mark)

    from_category = alexandria_category_factory(
        metainfo={
            "access": {
                "Municipality": {"visibility": "all", "permissions": from_permission}
            }
        }
    )
    move_target_category = alexandria_category_factory(
        metainfo={
            "access": {
                "Municipality": {"visibility": "all", "permissions": to_permission}
            }
        }
    )
    document = alexandria_document_factory(
        metainfo={"camac-instance-id": instance.pk},
        category=from_category,
    )
    for mark in marks:
        document.marks.add(mark)

    assert (
        has_alexandria_move_permission(
            fake_request, instance, document, move_target_category
        )
        is expected
    )


def test_has_alexandria_permission_v2(
    db,
    access_level_factory,
    alexandria_category_factory,
    alexandria_document_factory,
    alexandria_settings,
    fake_request,
    instance,
    permissions_settings,
    service,
    settings,
):
    alexandria_settings["USE_V2_PERMISSIONS"] = True
    permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.FULL

    access_level = access_level_factory()
    allowed_category = alexandria_category_factory()
    disallowed_category = alexandria_category_factory()
    allowed_document = alexandria_document_factory(
        metainfo={"camac-instance-id": instance.pk},
        category=allowed_category,
    )
    disallowed_document = alexandria_document_factory(
        metainfo={"camac-instance-id": instance.pk},
        category=disallowed_category,
    )

    settings.PERMISSIONS_ALEXANDRIA["ACCESS_LEVELS"] = {
        access_level.pk: [
            (f"{allowed_category.pk}:create", Always()),
            (f"{allowed_category.pk}:delete", Always()),
            (f"{allowed_category.pk}:mark:void", Always()),
            (f"{disallowed_category.pk}:create", Never()),
            (f"{disallowed_category.pk}:delete", Never()),
            (f"{disallowed_category.pk}:mark:void", Never()),
        ]
    }

    # allowed category / document, but permission not granted yet
    assert (
        has_alexandria_create_permission(fake_request, instance, allowed_category)
        is False
    )
    assert has_alexandria_delete_permission(fake_request, allowed_document) is False
    assert (
        has_alexandria_mark_permission(fake_request, allowed_document, "void") is False
    )

    grant(
        instance,
        grant_type=GRANT_CHOICES.SERVICE.value,
        access_level=access_level,
        service=service,
    )

    # allowed category / document, now permission is granted
    assert (
        has_alexandria_create_permission(fake_request, instance, allowed_category)
        is True
    )
    assert has_alexandria_delete_permission(fake_request, allowed_document) is True
    assert (
        has_alexandria_mark_permission(fake_request, allowed_document, "void") is True
    )

    # disallowed category / document
    assert (
        has_alexandria_create_permission(fake_request, instance, disallowed_category)
        is False
    )
    assert has_alexandria_delete_permission(fake_request, disallowed_document) is False
    assert (
        has_alexandria_mark_permission(fake_request, disallowed_document, "void")
        is False
    )


@pytest.mark.parametrize(
    ("configured_permissions", "expected"),
    [
        ([], False),
        ([("from-category:move", Always())], False),
        ([("from-category:move", Always()), ("to-category:move", Always())], False),
        # only when source allows move, and target allows create, the move is allowed
        (
            [("from-category:move", Always()), ("to-category:create", Always())],
            True,
        ),
        (
            [("from-category:all", Always()), ("to-category:all", Always())],
            True,
        ),
    ],
)
def test_has_alexandria_move_permission_v2(
    db,
    access_level_factory,
    alexandria_category_factory,
    alexandria_document_factory,
    alexandria_settings,
    fake_request,
    instance,
    configured_permissions,
    expected,
    permissions_settings,
    service,
    settings,
):
    alexandria_settings["USE_V2_PERMISSIONS"] = True
    permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.FULL

    access_level = access_level_factory()
    from_category = alexandria_category_factory(pk="from-category")
    move_target_category = alexandria_category_factory(pk="to-category")
    document = alexandria_document_factory(
        metainfo={"camac-instance-id": instance.pk},
        category=from_category,
    )

    settings.PERMISSIONS_ALEXANDRIA["ACCESS_LEVELS"] = {
        access_level.pk: configured_permissions
    }

    # permission not granted yet
    assert (
        has_alexandria_move_permission(
            fake_request,
            instance,
            document,
            move_target_category,
        )
        is False
    )

    grant(
        instance,
        grant_type=GRANT_CHOICES.SERVICE.value,
        access_level=access_level,
        service=service,
    )

    # permission is granted
    assert (
        has_alexandria_move_permission(
            fake_request,
            instance,
            document,
            move_target_category,
        )
        is expected
    )
