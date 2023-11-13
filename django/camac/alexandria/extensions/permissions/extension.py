from alexandria.core.models import BaseModel, Category, Document, File, Tag
from alexandria.core.permissions import (
    BasePermission,
    object_permission_for,
    permission_for,
)
from django.conf import settings
from django.core.validators import EMPTY_VALUES
from localized_fields.value import LocalizedStringValue

from camac.alexandria.extensions.common import get_role
from camac.alexandria.extensions.permissions import conditions, scopes
from camac.instance.models import Instance


def resolve_permissions(category, user):
    if category.parent:
        return resolve_permissions(category.parent, user)

    return category.metainfo["access"].get(get_role(user))


MODE_CREATE = "create"
MODE_UPDATE = "update"
MODE_DELETE = "delete"


class CustomPermission(BasePermission):
    def get_needed_permissions(self, request) -> set:
        if request.method == "POST":
            used_permissions = {MODE_CREATE}
            for key, value in request.data.items():
                # TODO temporary case for marks, while they are tags
                if key == "tags" and len(
                    set([v["id"] for v in value]).intersection(
                        set(settings.ALEXANDRIA["MARKS"]["ALL"])
                    )
                ):
                    used_permissions.add(f"{MODE_CREATE}-marks")
                elif (
                    key in settings.ALEXANDRIA["RESTRICTED_FIELDS"]
                    and value not in EMPTY_VALUES
                ):
                    used_permissions.add(f"{MODE_CREATE}-{key}")

            return used_permissions
        elif request.method == "PATCH":
            return {MODE_UPDATE}
        elif request.method == "DELETE":
            return {MODE_DELETE}

        return set()  # pragma: no cover

    # TODO noqa can probably removed after marks model
    def get_needed_object_permissions(self, request, document) -> set:  # noqa: C901
        if request.method == "DELETE":
            return {MODE_DELETE}
        elif request.method == "PATCH":
            used_permissions = {MODE_UPDATE}
            for key in settings.ALEXANDRIA["RESTRICTED_FIELDS"]:
                # TODO temporary case for marks, while they are tags
                if key not in request.data and not (
                    key == "marks" and "tags" in request.data
                ):
                    continue

                was_marks = False
                if key == "marks":
                    was_marks = True
                    key = "tags"

                old_value = getattr(document, key)
                new_value = request.data.get(key)

                if isinstance(old_value, LocalizedStringValue):
                    new_value = LocalizedStringValue(new_value)
                elif isinstance(old_value, Category):
                    old_value = old_value.pk
                    new_value = new_value["id"]
                elif hasattr(old_value, "values_list") and new_value:
                    old_value = [str(v) for v in old_value.values_list("pk", flat=True)]
                    new_value = [item["id"] for item in new_value]

                    # TODO temporary case for marks, while they are tags
                    if key == "tags":
                        filter_list = settings.ALEXANDRIA["MARKS"]["ALL"]
                        filter_func = (
                            (lambda v: v in filter_list)
                            if was_marks
                            else (lambda v: v not in filter_list)
                        )
                        old_value = list(filter(filter_func, old_value))
                        new_value = list(filter(filter_func, new_value))

                if old_value != new_value:
                    if was_marks:
                        key = "marks"
                    used_permissions.add(f"{MODE_UPDATE}-{key}")

            return used_permissions

        # Fallback, never assign this permission anywhere!
        return {"FORBIDDEN_METHOD"}  # pragma: no cover

    def get_available_permissions(
        self, request, instance: Instance, category: Category, document: Document = None
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
                    all_checks_met &= getattr(conditions, condition)(
                        value, instance, request, document
                    ).evaluate()
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
    def has_permission_default(self, request):  # pragma: no cover
        if get_role(request.caluma_info.context.user) == "support":
            return True

        return False

    @permission_for(Document)
    def has_permission_for_document(self, request):
        if request.method == "POST":
            instance = Instance.objects.get(
                pk=request.data["metainfo"]["camac-instance-id"]
            )
            category = Category.objects.get(pk=request.data["category"]["id"])
        elif request.method == "PATCH":
            document = Document.objects.get(pk=request.data["id"])
            instance = document.instance_document.instance
            category = document.category
        elif request.method == "DELETE":
            document = Document.objects.get(pk=request.path.split("/")[-1])
            instance = document.instance_document.instance
            category = document.category

        # analyze category to figure out available permissions
        available_permissions = self.get_available_permissions(
            request, instance, category
        )

        # short circuit if no permissions are available
        if not available_permissions:
            return False

        # analyze request to figure out needed permissions
        needed_permissions = self.get_needed_permissions(request)

        # check if needed permissions are subset of available permissions
        return needed_permissions.issubset(available_permissions)

    @object_permission_for(Document)
    def has_object_permission_for_document(self, request, document):
        available_permissions = self.get_available_permissions(
            request, document.instance_document.instance, document.category, document
        )

        if not available_permissions:
            return False

        needed_permissions = self.get_needed_object_permissions(request, document)

        return needed_permissions.issubset(available_permissions)

    @permission_for(File)
    def has_permission_for_file(self, request):
        document = Document.objects.get(pk=request.data["document"]["id"])
        available_permissions = self.get_available_permissions(
            request, document.instance_document.instance, document.category, document
        )

        if not available_permissions:
            return False

        needed_permissions = {"create-files"}
        return needed_permissions.issubset(available_permissions)

    @permission_for(Tag)
    def has_permission_for_tag(self, request):
        if get_role(request.caluma_info.context.user) not in ["public", "applicant"]:
            return True

        return False

    @object_permission_for(Tag)
    def has_object_permission_for_tag(self, request, tag):
        if get_role(request.caluma_info.context.user) == "support":
            return True

        if get_role(request.caluma_info.context.user) not in ["public", "applicant"]:
            return tag.created_by_group == str(request.caluma_info.context.user.group)
