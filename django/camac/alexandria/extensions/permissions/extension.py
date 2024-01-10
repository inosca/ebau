import datetime
from typing import Union

from alexandria.core.models import BaseModel, Category, Document, File, Tag
from django.conf import settings
from django.core.validators import EMPTY_VALUES
from generic_permissions.permissions import object_permission_for, permission_for
from localized_fields.value import LocalizedStringValue

from camac.alexandria.extensions.common import get_role
from camac.alexandria.extensions.permissions import conditions, scopes
from camac.instance.models import Instance
from camac.utils import get_dict_item


def resolve_permissions(category, user):
    if category.parent:
        return resolve_permissions(category.parent, user)

    return get_dict_item(category.metainfo, f"access.{get_role(user)}", default=None)


MODE_CREATE = "create"
MODE_UPDATE = "update"
MODE_DELETE = "delete"


class CustomPermission:
    def get_needed_permissions(self, request, document=None) -> set:
        if request.method == "POST":
            used_permissions = {MODE_CREATE}
            for key, value in request.data.items():
                if (
                    key in settings.ALEXANDRIA["RESTRICTED_FIELDS"]
                    and value not in EMPTY_VALUES
                ):
                    used_permissions.add(f"{MODE_CREATE}-{key}")

            return used_permissions
        elif request.method == "PATCH":
            return self.get_needed_patch_permissions(request, document)
        elif request.method == "DELETE":
            return {MODE_DELETE}

        return set()  # pragma: no cover

    def get_needed_patch_permissions(self, request, document) -> set:  # noqa: C901
        used_permissions = {MODE_UPDATE}
        for key in settings.ALEXANDRIA["RESTRICTED_FIELDS"]:
            if key not in request.data:
                continue

            old_value = getattr(document, key)
            new_value = request.data.get(key)

            # LocalizedTextField
            if isinstance(old_value, LocalizedStringValue):
                new_value = LocalizedStringValue(new_value)
            # DateField
            elif isinstance(old_value, datetime.date):
                new_value = datetime.datetime.fromisoformat(new_value).date()
            # ForeignKey
            elif isinstance(old_value, Category):
                old_value = old_value.pk
                new_value = new_value["id"]
            # ManyToManyField
            elif hasattr(old_value, "values_list"):
                old_value = [str(v) for v in old_value.values_list("pk", flat=True)]
                new_value = [item["id"] for item in new_value]

            if old_value != new_value:
                used_permissions.add(f"{MODE_UPDATE}-{key}")

        return used_permissions

    def get_available_permissions(
        self,
        request,
        instance: Instance,
        category: Category,
        document: Union[Document, None] = None,
    ) -> set:
        user = request.caluma_info.context.user
        category_permissions = resolve_permissions(category, user)

        if not category_permissions or "permissions" not in category_permissions:
            return set()

        available_permissions = set()

        for permission in category_permissions["permissions"]:
            all_checks_met = True

            if document and permission["permission"] != "create":
                all_checks_met &= getattr(scopes, permission["scope"])(
                    user, document
                ).evaluate()

            required_conditions = permission.get("condition")
            if required_conditions and all_checks_met:
                for condition, value in required_conditions.items():
                    negated = condition.startswith("~")
                    result = getattr(conditions, condition.lstrip("~"))(
                        value, instance, request, document
                    ).evaluate()
                    all_checks_met = not result if negated else result

                    if not all_checks_met:
                        break

            if all_checks_met:
                fields = permission.get(
                    "fields", settings.ALEXANDRIA["RESTRICTED_FIELDS"]
                )

                available_permissions.add(permission["permission"])
                for field in fields:
                    available_permissions.add(f"{permission['permission']}-{field}")

        return available_permissions

    @permission_for(BaseModel)
    @object_permission_for(BaseModel)
    def has_permission_default(self, request, document=None):  # pragma: no cover
        return get_role(request.caluma_info.context.user) == "support"

    @permission_for(Document)
    @object_permission_for(Document)
    def has_permission_for_document(self, request, document=None):
        if request.method == "POST":
            # On creation we don't have an data in the database yet. Therefore
            # we need to get the needed data from the request.
            instance = Instance.objects.get(
                pk=request.data["metainfo"]["camac-instance-id"]
            )
            category = Category.objects.get(pk=request.data["category"]["id"])
        elif document is not None:
            # On update and delete we can get the needed data from the database
            instance = document.instance_document.instance
            category = document.category
        else:
            # If there is no document, we called `permission_for` which can be
            # ignored for update and delete requests as `object_permission_for`
            # will be called afterwards and will execute the branch above.
            return True

        # analyze category to figure out available permissions
        available_permissions = self.get_available_permissions(
            request, instance, category, document
        )

        # short circuit if no permissions are available
        if not available_permissions:
            return False

        # analyze request to figure out needed permissions
        needed_permissions = self.get_needed_permissions(request, document)

        # if the category changed, we need to check whether we are allowed to
        # create a document in the new category as well
        new_category_id = get_dict_item(request.data, "category.id", default=None)
        if new_category_id and category.pk != new_category_id:
            new_category = Category.objects.get(pk=new_category_id)

            available_permissions_new_category = self.get_available_permissions(
                request, instance, new_category, document
            )
            needed_permissions_new_category = {MODE_CREATE}

            # if the document already has marks, we need to make sure that the
            # new category allows marks
            if document.marks.exists():
                needed_permissions_new_category.add(f"{MODE_UPDATE}-marks")

            if not needed_permissions_new_category.issubset(
                available_permissions_new_category
            ):
                return False

        # check if needed permissions are subset of available permissions
        return needed_permissions.issubset(available_permissions)

    @permission_for(File)
    @object_permission_for(File)
    def has_permission_for_file(self, request, file=None):
        if file is None:
            document = Document.objects.get(pk=request.data["document"]["id"])
        else:
            document = file.document

        available_permissions = self.get_available_permissions(
            request, document.instance_document.instance, document.category, document
        )

        if not available_permissions:
            return False

        needed_permissions = {"create-files"}
        return needed_permissions.issubset(available_permissions)

    @permission_for(Tag)
    @object_permission_for(Tag)
    def has_permission_for_tag(self, request, tag=None):
        role = get_role(request.caluma_info.context.user)

        if role == "support":
            # Support can create, edit and delete tags
            return True
        elif role not in ["public", "applicant"] and tag is None:
            # Internal roles can create tags
            return True
        elif role not in ["public", "applicant"] and tag is not None:
            # Internal roles can only edit and delete own tags
            return tag.created_by_group == str(request.group.service_id)

        return False
