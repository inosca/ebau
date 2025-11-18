import datetime
import json
from typing import Literal

from alexandria.core.models import BaseModel, Category, Document, File, Tag
from django.conf import settings
from django.db.models.fields.related_descriptors import (
    ForwardManyToOneDescriptor,
    ManyToManyDescriptor,
)
from generic_permissions.permissions import object_permission_for, permission_for
from rest_framework.request import Request

from camac.alexandria.permissions import AlexandriaPermissionManager
from camac.instance.models import Instance
from camac.permissions.api import P, PermissionScope
from camac.request_cache import cache_on_request
from camac.user.permissions import get_role_name


def get_data_from_multipart_request(request: Request) -> dict:
    """Extract JSON data from an alexandria multipart request."""

    return json.loads(request.data["data"].read().decode("utf-8"))


def get_changed_fields(request: Request, document: Document) -> dict[str, tuple]:
    """Extract changed fields on a document from a request."""

    changed_fields = {}

    for key, new_value in request.data.items():
        if key not in settings.ALEXANDRIA["RESTRICTED_FIELDS"]:
            continue

        old_value = getattr(document, key)
        descriptor = getattr(document._meta.model, key)

        # DateField (date)
        if isinstance(old_value, datetime.date):
            new_value = datetime.datetime.fromisoformat(new_value).date()
        # ForeignKey (category)
        elif isinstance(descriptor, ForwardManyToOneDescriptor):
            old_value = old_value.pk
            new_value = new_value["id"]
        # ManyToManyField (marks, tags)
        elif isinstance(descriptor, ManyToManyDescriptor):
            old_value = {str(pk) for pk in old_value.values_list("pk", flat=True)}
            new_value = {str(item["id"]) for item in new_value}

        if old_value != new_value:
            changed_fields[key] = (old_value, new_value)

    return changed_fields


class AlexandriaPermissions:
    def scope(self, request: Request, obj: Document | Instance) -> PermissionScope:
        """Get permission scope for the current request and object."""

        return AlexandriaPermissionManager.from_request(request).scoped_for(obj)

    def prefix(self, obj: str | Document) -> str:
        """Get category prefix for requested permissions.

        This must always return a category slug. As child categories cannot have
        their own permissions they need to use the permissions of the parent
        category.
        """

        match obj:
            case str():
                category = Category.objects.get(pk=obj)
            case Document():
                category = obj.category
            case _:  # pragma: no cover
                raise RuntimeError()

        if category.parent_id is not None:
            return category.parent_id

        return category.pk

    @permission_for(BaseModel)
    def has_permission_default(self, *args, **kwargs) -> Literal[False]:
        """Fallback permission for unhandled models - don't allow anything."""

        return False

    @permission_for(Document)
    def has_permission_for_document(
        self,
        request: Request,
        action: str,
        *args,
        **kwargs,
    ) -> bool:
        """Check permission for documents.

        This method only checks the permission for creating documents. All other
        actions are explicitly skipped as they're checked in
        `has_object_permission_for_document` where we have the affected document
        as context.
        """

        if action != "create":
            # Already handled in the object permissions
            return True

        data = get_data_from_multipart_request(request)

        prefix = self.prefix(data["category"])
        instance = Instance.objects.get(pk=data["metainfo"]["camac-instance-id"])

        return self.scope(request, instance).has(
            P.any(
                f"{prefix}:all",
                f"{prefix}:create",
            )
        )

    @object_permission_for(Document)
    @cache_on_request
    def has_object_permission_for_document(
        self,
        request: Request,
        document: Document,
        action: str,
        *args,
        **kwargs,
    ) -> bool:
        """Check object permission for documents.

        The required permissions depend on the DRF action being called (HTTP
        method & URL).
        """

        permissions_fn_map = {
            "destroy": self.get_required_permissions_for_document_delete,
            "convert": self.get_required_permissions_for_document_convert,
            "copy": self.get_required_permissions_for_document_copy,
            "partial_update": self.get_required_permissions_for_document_update,
        }

        permissions_fn = permissions_fn_map.get(action)

        if permissions_fn is None:  # pragma: no cover
            raise NotImplementedError(
                f"{self.__class__.__name__}: missing function to get required permissions for action {action}"
            )

        required_permissions = permissions_fn(document, request, self.prefix(document))

        if required_permissions is None:
            return True

        return self.scope(request, document).has(required_permissions)

    def get_required_permissions_for_document_delete(
        self,
        document: Document,
        request: Request,
        prefix: str,
    ) -> P:
        """Get required permissions for the destroy action."""

        return P.any(
            f"{prefix}:all",
            f"{prefix}:delete",
        )

    def get_required_permissions_for_document_convert(
        self,
        document: Document,
        request: Request,
        prefix: str,
    ) -> P:
        """Get required permissions for the convert action.

        As converting a document to a PDF creates a new document, this action
        requires the same permission as creating a document does.
        """

        return P.any(
            f"{prefix}:all",
            f"{prefix}:create",
        )

    def get_required_permissions_for_document_copy(
        self,
        document: Document,
        request: Request,
        prefix: str,
    ) -> P:
        """Get required permissions for the copy action.

        Copying a document creates a new document. Therefore, this action
        requires the same permission as creating a document does. Since the
        target category can optionally be passed, we need to require the create
        permission in the given category or fallback to the current category.
        """

        changed_fields = get_changed_fields(request, document)

        if "category" in changed_fields:
            # If the document is copied into another category, we need to check
            # permissions for the target category instead of the current
            # category.
            prefix = self.prefix(changed_fields["category"][1])

        return P.any(
            f"{prefix}:all",
            f"{prefix}:create",
        )

    def get_required_permissions_for_document_update(
        self,
        document: Document,
        request: Request,
        prefix: str,
    ) -> P | None:
        """Get required permissions for the update action.

        Resulting permissions depend on what fields are being changed in the
        request:

        - `title`, `description`, `date` or `metainfo` require the default
          "update" permission
        - `tags` require the "tag" permission
        - `marks` require the "mark" permission. As permissions may differ
          depending on the mark that is changed, the mark permission is scoped
          to the actual mark (e.g mark:decision or mark:all to allow changes to
          all marks)
        - `category` requires the "move" permission as well as the "create"
          permission in the target category
        """

        action_permissions = []
        extra_permission = None

        changed_fields = get_changed_fields(request, document)

        if {"title", "description", "date", "metainfo"}.intersection(
            set(changed_fields.keys())
        ):
            action_permissions.append(P(f"{prefix}:update"))

        if "tags" in changed_fields:
            action_permissions.append(P(f"{prefix}:tag"))

        if "category" in changed_fields:
            action_permissions.append(P(f"{prefix}:move"))

            # If we move a document to another category we need to check that we
            # have creation permission in the target category as well as move
            # permissions in the current category.
            new_category = self.prefix(changed_fields["category"][1])
            extra_permission = P.any(f"{new_category}:all", f"{new_category}:create")

        if "marks" in changed_fields:
            old, new = changed_fields["marks"]
            added = new - old
            removed = old - new
            changed = added.union(removed)

            # Each mark may have different permissions (e.g. a service is
            # allowed to mark as void but not any other mark) so we need to
            # check permission for every mark that was either added or removed.
            action_permissions.append(
                P.any(
                    f"{prefix}:mark:all",
                    P.all(*[f"{prefix}:mark:{slug}" for slug in changed]),
                )
            )

        if not action_permissions:
            # If nothing changed we allow it
            return None

        permissions = P(f"{prefix}:all") | P.all(*action_permissions)

        if extra_permission:
            permissions &= extra_permission

        return permissions

    @permission_for(File)
    def has_permission_for_file(
        self,
        request: Request,
        action: str,
        *args,
        **kwargs,
    ) -> bool:
        """Check permission for files (document versions).

        This explicitly only checks the permission for creating files as the UI
        does not allow any other actions (e.g. update or delete). As such
        actions are not expected, we don't allow them.
        """

        if action != "create":
            # No other action allowed via API
            return False

        document = Document.objects.get(pk=request.data["document"])
        prefix = self.prefix(document)

        return self.scope(request, document).has(
            P.any(
                f"{prefix}:all",
                f"{prefix}:replace",
            )
        )

    @permission_for(Tag)
    def has_permission_for_tag(
        self,
        request: Request,
        action: str,
        *args,
        **kwargs,
    ) -> bool:
        """Check permission for tags.

        This explicitly only checks the permission for creating tags as the UI
        does not allow any other actions (e.g. update or delete). As such
        actions are not expected, we don't allow them.

        Adding and removing tags from a document are handled in the permission
        for the document as those actions are updates to the document model.
        """

        if action != "create":
            # No other action allowed via API
            return False

        # As tags are not related to an instance in any way, we can't use the
        # permission module but depend on the role.
        role = get_role_name(request.group)
        return role is not None and role not in ["public", "applicant"]
