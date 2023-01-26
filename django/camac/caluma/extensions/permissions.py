import json
from functools import wraps
from logging import getLogger

import requests
from caluma.caluma_core.mutation import Mutation
from caluma.caluma_core.permissions import (
    BasePermission,
    object_permission_for,
    permission_for,
)
from caluma.caluma_form.models import Document
from caluma.caluma_form.schema import (
    CopyDocument,
    RemoveAnswer,
    RemoveDocument,
    SaveDocument,
    SaveDocumentAnswer,
)
from caluma.caluma_workflow.models import Case, WorkItem
from caluma.caluma_workflow.schema import (
    CancelWorkItem,
    CompleteWorkItem,
    CreateWorkItem,
    RedoWorkItem,
    ResumeCase,
    ResumeWorkItem,
    SaveCase,
    SaveWorkItem,
    SkipWorkItem,
    SuspendCase,
)
from django.conf import settings
from inflection import underscore

from camac.caluma.utils import CamacRequest
from camac.constants.kt_bern import DASHBOARD_FORM_SLUG
from camac.user.permissions import permission_aware
from camac.utils import build_url, headers

log = getLogger()


def is_addressed_to_service(work_item, service_id):
    return str(service_id) in work_item.addressed_groups


def is_controlled_by_service(work_item, service_id):
    return str(service_id) in work_item.controlling_groups


def is_created_by_service(work_item, service_id):
    return work_item.created_by_group == str(service_id)


def is_addressed_to_applicant(work_item):  # pragma: todo cover
    if settings.APPLICATION_NAME == "kt_schwyz":
        return "applicant" in work_item.addressed_groups
    return len(work_item.addressed_groups) == 0


def get_current_service_id(info):
    return info.context.user.group


def resolve_savedocumentanswer_document(mutation, info, answer=None):
    return (
        answer.document
        if answer
        else Document.objects.filter(
            pk=mutation.get_params(info)["input"]["document"]
        ).first()
    )


def distribution_permission_for(
    configured_mutation, configured_values, configured_resolve_fn=None
):
    def decorate(func):
        @wraps(func)
        def wrapper(permission, mutation, info, value=None, *args, **kwargs):
            wrapped_has_permission = (
                func(permission, mutation, info, value, *args, **kwargs)
                if value
                else func(permission, mutation, info, *args, **kwargs)
            )

            # Include distribution permissions, short-circuit if
            # wrapped permission method isn't fulfilled
            if settings.DISTRIBUTION and wrapped_has_permission:
                configured_mutation_name = configured_mutation.__name__

                if configured_resolve_fn:
                    value = configured_resolve_fn(mutation, info, value)

                attribute = (
                    value.task_id
                    if type(value) == WorkItem
                    else value.form_id
                    if type(value) == Document
                    else None
                )
                configured_value_name = next(
                    (
                        configured_value
                        for configured_value in configured_values
                        if attribute == settings.DISTRIBUTION.get(configured_value)
                    ),
                    None,
                )

                if configured_value_name and issubclass(mutation, configured_mutation):
                    permissions_predicate = (
                        settings.DISTRIBUTION["PERMISSIONS"]
                        .get(configured_mutation_name, {})
                        .get(configured_value_name, lambda *_: True)
                    )

                    group = CamacRequest(info).request.group
                    return permissions_predicate(group, value, mutation, info)

            return wrapped_has_permission

        return wrapper

    return decorate


class CustomPermission(BasePermission):
    def __init__(self):
        super().__init__()

        self.request = None

    # Override has_permission of BasePermission to only allow authenticated
    # users, which also adhere to the permission methods defined by the
    # CustomPermission class, to execute mutations.
    # The caluma permission class IsAuthenticated isn't used, because it overrides
    # has_permission without calling the super has_permission method of its parent
    # class BasePermission.
    def has_permission(self, mutation, info):
        self.request = info.context.camac_request

        return info.context.user.is_authenticated and super().has_permission(
            mutation, info
        )

    def has_object_permission(self, mutation, info, instance):
        self.request = info.context.camac_request

        return super().has_object_permission(mutation, info, instance)

    @permission_for(Mutation)
    def has_permission_default(self, mutation, info):  # pragma: todo cover
        log.debug(
            f"ACL: fallback permission: allow mutation '{mutation.__name__}' for support users"
        )

        return self.has_camac_role("support")

    @object_permission_for(Mutation)
    def has_object_permission_default(
        self, mutation, info, instance
    ):  # pragma: todo cover
        log.debug(
            f"ACL: fallback object permission: allowing "
            f"mutation '{mutation.__name__}' on {instance} for support users"
        )

        return self.has_camac_role("support")

    # Case
    @permission_for(SaveCase)
    @object_permission_for(SaveCase)
    def has_permission_for_save_case(
        self, mutation, info, case=None
    ):  # pragma: todo cover
        # Visibilty handles whether the user has access to the case
        return True

    @permission_for(SuspendCase)
    @permission_for(ResumeCase)
    @object_permission_for(ResumeCase)
    @object_permission_for(SuspendCase)
    def has_permission_for_suspend_resume_case(
        self, mutation, info, case=None
    ):  # pragma: todo cover
        if not case:
            return True

        return case.instance.responsible_service(
            filter_type="municipality"
        ).pk == get_current_service_id(info)

    # Work Item
    @permission_for(CreateWorkItem)
    def has_permission_for_create_work_item(self, mutation, info):  # pragma: todo cover
        # Visibilty handles whether the user has access to the case on which
        # the work item is created
        return True

    @permission_for(SaveWorkItem)
    @object_permission_for(SaveWorkItem)
    def has_permission_for_save_work_item(self, mutation, info, work_item=None):
        if not work_item:
            # Same as has_permission_for_create_work_item
            return True

        service = get_current_service_id(info)

        # The creator of a manual work item can change all properties
        if work_item.task_id == settings.APPLICATION["CALUMA"].get(
            "MANUAL_WORK_ITEM_TASK", None
        ) and is_created_by_service(work_item, service):
            return True

        serialized_input = {
            underscore(key): value
            for key, value in mutation.get_params(info)["input"].items()
        }

        changed_keys = [
            key
            for key, value in serialized_input.items()
            if hasattr(work_item, key) and getattr(work_item, key) != value
        ]

        is_addressed = is_addressed_to_service(work_item, service)
        is_controller = is_controlled_by_service(work_item, service)

        permissions_for_key = {
            "description": is_controller,
            "assigned_users": is_addressed,
            "deadline": is_controller,
            "meta": is_addressed or is_controller,
        }

        return all(
            [
                permissions_for_key.get(changed_key, False)
                for changed_key in changed_keys
            ]
        )

    @distribution_permission_for(
        CompleteWorkItem,
        [
            "INQUIRY_CREATE_TASK",
            "INQUIRY_CHECK_TASK",
            "DISTRIBUTION_COMPLETE_TASK",
            "DISTRIBUTION_CHECK_TASK",
            "INQUIRY_ANSWER_FILL_TASK",
            "INQUIRY_ANSWER_CHECK_TASK",
            "INQUIRY_ANSWER_REVISE_TASK",
        ],
    )
    @permission_for(CompleteWorkItem)
    @permission_for(SkipWorkItem)
    @object_permission_for(CompleteWorkItem)
    @object_permission_for(SkipWorkItem)
    def has_permission_for_process_work_item(self, mutation, info, work_item=None):
        if not work_item or self.has_camac_role("support"):
            # Always allow for support group since our PHP action uses that group
            return True

        return is_addressed_to_service(
            work_item, get_current_service_id(info)
        ) or is_addressed_to_applicant(work_item)

    @distribution_permission_for(CancelWorkItem, ["INQUIRY_TASK"])
    @permission_for(CancelWorkItem)
    @object_permission_for(CancelWorkItem)
    def has_permission_for_cancel_work_item(self, mutation, info, work_item=None):
        if not work_item or self.has_camac_role("support"):
            # Always allow for support group since our PHP action uses that group
            return True

        service_id = get_current_service_id(info)
        return (
            is_addressed_to_service(work_item, service_id)
            or is_controlled_by_service(work_item, service_id)
            or is_addressed_to_applicant(work_item)
        )

    @distribution_permission_for(ResumeWorkItem, ["INQUIRY_TASK"])
    @permission_for(ResumeWorkItem)
    @object_permission_for(ResumeWorkItem)
    def has_permission_for_resume_work_item(self, mutation, info, work_item=None):
        if not work_item:
            return True

        return is_controlled_by_service(work_item, get_current_service_id(info))

    @distribution_permission_for(RedoWorkItem, ["DISTRIBUTION_TASK", "INQUIRY_TASK"])
    @permission_for(RedoWorkItem)
    @object_permission_for(RedoWorkItem)
    def has_permission_for_redo_work_item(self, mutation, info, work_item=None):
        if not work_item:
            return True

        service = get_current_service_id(info)

        if work_item.task_id == settings.DISTRIBUTION["INQUIRY_TASK"]:
            return is_controlled_by_service(work_item, service)

        return is_addressed_to_service(work_item, service)

    # Document
    @permission_for(RemoveDocument)
    @permission_for(SaveDocument)
    def has_permission_for_savedocument(self, mutation, info):  # pragma: todo cover
        if mutation.get_params(info).get("form") == DASHBOARD_FORM_SLUG:
            # There should only be one dashboard document which has to be
            # created by a support user
            return (
                self.has_camac_role("support")
                and Document.objects.filter(form__slug=DASHBOARD_FORM_SLUG).count() == 0
            )

        return True

    @object_permission_for(RemoveDocument)
    @object_permission_for(SaveDocument)
    def has_object_permission_for_savedocument(
        self, mutation, info, document
    ):  # pragma: todo cover
        if document.form.slug == DASHBOARD_FORM_SLUG:
            return self.has_camac_role("support")

        return self.has_camac_edit_permission(document.family, info)

    @permission_for(CopyDocument)
    def has_permission_for_copydocument(self, mutation, info):  # pragma: todo cover
        source = Document.objects.get(pk=mutation.get_params(info)["input"]["source"])

        return self.has_camac_edit_permission(source, info)

    # Answer
    @distribution_permission_for(
        SaveDocumentAnswer,
        ["INQUIRY_FORM", "INQUIRY_ANSWER_FORM"],
        resolve_savedocumentanswer_document,
    )
    @permission_for(SaveDocumentAnswer)
    def has_permission_for_savedocumentanswer(self, mutation, info):
        try:
            document = Document.objects.get(
                pk=mutation.get_params(info)["input"]["document"]
            )
        except (Document.DoesNotExist, KeyError):  # pragma: no cover
            log.error(
                f"{mutation.__name__}: unable not find document: {json.dumps(mutation.get_params(info))}"
            )
            return False

        if document.form.slug == DASHBOARD_FORM_SLUG:  # pragma: todo cover
            return self.has_camac_role("support")

        return self.has_camac_edit_permission(document.family, info)

    @distribution_permission_for(
        SaveDocumentAnswer,
        ["INQUIRY_FORM", "INQUIRY_ANSWER_FORM"],
        resolve_savedocumentanswer_document,
    )
    @object_permission_for(SaveDocumentAnswer)
    def has_object_permission_for_savedocumentanswer(self, mutation, info, answer):
        if answer.document.form.slug == DASHBOARD_FORM_SLUG:  # pragma: todo cover
            return self.has_camac_role("support")

        return self.has_camac_edit_permission(answer.document.family, info)

    @permission_for(RemoveAnswer)
    def has_permission_for_removeanswer(self, mutation, info):  # pragma: todo cover
        answer = mutation.get_params(info)["input"]["answer"]

        return self.has_camac_edit_permission(answer.document.family, info)

    @object_permission_for(RemoveAnswer)
    def has_object_permission_for_removeanswer(
        self, mutation, info, answer
    ):  # pragma: todo cover
        return self.has_camac_edit_permission(answer.document.family, info)

    def has_camac_role(self, required_permission):
        role_name = self.request.group.role.name
        role_permissions = settings.APPLICATION.get("ROLE_PERMISSIONS", {})

        return role_permissions.get(role_name) == required_permission

    def has_camac_edit_permission(self, target, info, required_permission="write"):
        if isinstance(target, Case):  # pragma: todo cover
            case = target
            permission_key = "case-meta"
        elif isinstance(target, Document):
            case = (
                target.work_item.case
                if getattr(target, "work_item", None)
                else getattr(target, "case", None)
            )

            if not case:  # pragma: todo cover
                # if the document is unlinked, allow changing it this is used for
                # new table rows
                return True

            permission_key = (
                "main"
                if target == case.document
                and not (hasattr(case, "parent_work_item") and case.parent_work_item)
                else target.form.slug
            )

            if (
                permission_key != "main"
                and target.family.form_id
                not in settings.APPLICATION["CALUMA"].get("FORM_PERMISSIONS", [])
            ):
                # If the form of the current document is not using custom
                # permissions defined in the instance serializer, we shall use
                # basic caluma permissions.
                return self.has_caluma_form_edit_permission(target, info)

        else:  # pragma: no cover
            return False

        resp = requests.get(
            build_url(
                settings.API_HOST, f"/api/v1/instances/{case.family.instance.pk}"
            ),
            headers=headers(info),
        )

        resp.raise_for_status()

        try:
            jsondata = resp.json()
            if "error" in jsondata:  # pragma: no cover
                raise RuntimeError("Error from NG API: %s" % jsondata["error"])

            permissions = jsondata["data"]["meta"]["permissions"]

            return required_permission in permissions.get(permission_key, [])

        except KeyError:  # pragma: no cover
            raise RuntimeError(
                f"NG API returned unexpected data structure (no data key) {jsondata}"
            )

    @permission_aware
    def has_caluma_form_edit_permission(self, document, info):
        return False

    def has_caluma_form_edit_permission_for_municipality(self, document, info):
        work_item = document.family.work_item

        return (
            is_addressed_to_service(work_item, get_current_service_id(info))
            and work_item.status == WorkItem.STATUS_READY
        )

    def has_caluma_form_edit_permission_for_support(self, document, info):
        return True
