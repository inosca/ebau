import json
from logging import getLogger

import requests
from caluma.caluma_core.mutation import Mutation
from caluma.caluma_core.permissions import (
    BasePermission,
    object_permission_for,
    permission_for,
)
from caluma.caluma_form.models import Document
from caluma.caluma_form.schema import RemoveAnswer, SaveDocument, SaveDocumentAnswer
from caluma.caluma_workflow.models import Case
from caluma.caluma_workflow.schema import (
    CancelCase,
    CompleteWorkItem,
    SaveCase,
    SkipWorkItem,
)
from django.conf import settings
from django.db.models import Q

from camac.constants.kt_bern import (
    CAMAC_ADMIN_GROUP,
    CAMAC_SUPPORT_GROUP,
    DASHBOARD_FORM_SLUG,
)
from camac.utils import build_url, headers

log = getLogger()


class CustomPermission(BasePermission):
    @object_permission_for(Mutation)
    def has_object_permission_default(self, mutation, info, instance):
        log.debug(
            f"ACL: fallback object permission: allowing "
            f"mutation '{mutation.__name__}' on {instance} for admin users"
        )

        return self.has_camac_group_permission(info, CAMAC_ADMIN_GROUP)

    @permission_for(Mutation)
    def has_permission_default(self, mutation, info):
        log.debug(
            f"ACL: fallback permission: allow mutation '{mutation.__name__}' for admins"
        )

        return self.has_camac_group_permission(info, CAMAC_ADMIN_GROUP)

    # Case
    @permission_for(SaveCase)
    def has_permission_for_savecase(self, mutation, info):
        return True

    @object_permission_for(SaveCase)
    def has_object_permission_for_savecase(self, mutation, info, case):
        return self.has_camac_edit_permission(case.family, info, "write")

    @permission_for(CompleteWorkItem)
    @permission_for(SkipWorkItem)
    @permission_for(CancelCase)
    @object_permission_for(CompleteWorkItem)
    @object_permission_for(SkipWorkItem)
    @object_permission_for(CancelCase)
    def has_permission_for_workflow(self, mutation, info, target=None):
        # TODO: This must be addressed as soon as proper assigned groups / users are implemented
        return True

    # Document
    @permission_for(SaveDocument)
    def has_permission_for_savedocument(self, mutation, info):
        if mutation.get_params(info).get("form") == DASHBOARD_FORM_SLUG:
            # There should only be one dashboard document which has to be
            # created by a support user
            return (
                self.has_camac_group_permission(info, CAMAC_SUPPORT_GROUP)
                and Document.objects.filter(form__slug=DASHBOARD_FORM_SLUG).count() == 0
            )

        return True

    @object_permission_for(SaveDocument)
    def has_object_permission_for_savedocument(self, mutation, info, document):
        if document.form.slug == DASHBOARD_FORM_SLUG:
            return self.has_camac_group_permission(info, CAMAC_SUPPORT_GROUP)

        return self.has_camac_edit_permission(document.family, info, "write")

    # Answer
    @permission_for(SaveDocumentAnswer)
    def has_permission_for_savedocumentanswer(self, mutation, info):
        try:
            document = Document.objects.get(
                pk=mutation.get_params(info)["input"]["document"]
            )
        except (Document.DoesNotExist, KeyError):
            log.error(
                f"{mutation.__name__}: unable not find document: {json.dumps(mutation.get_params(info))}"
            )
            return False

        if document.form.slug == DASHBOARD_FORM_SLUG:
            return self.has_camac_group_permission(info, CAMAC_SUPPORT_GROUP)

        return self.has_camac_edit_permission(document.family, info)

    @object_permission_for(SaveDocumentAnswer)
    def has_object_permission_for_savedocumentanswer(self, mutation, info, answer):
        if answer.document.form.slug == DASHBOARD_FORM_SLUG:
            return self.has_camac_group_permission(info, CAMAC_SUPPORT_GROUP)

        return self.has_camac_edit_permission(answer.document.family, info)

    @permission_for(RemoveAnswer)
    def has_permission_for_removeanswer(self, mutation, info):
        answer = json.loads(info.context.body)["variables"]["input"]["answer"]
        document = Document.objects.get(answers__pk=answer)

        return self.has_camac_edit_permission(document.family, info)

    @object_permission_for(RemoveAnswer)
    def has_object_permission_for_removeanswer(self, mutation, info, answer):
        return self.has_camac_edit_permission(answer.document.family, info)

    def has_camac_group_permission(self, info, required_group):
        response = requests.get(
            build_url(settings.INTERNAL_BASE_URL, "/api/v1/me"), headers=headers(info)
        )

        response.raise_for_status()

        admin_groups = [
            group
            for group in response.json()["data"]["relationships"]["groups"]["data"]
            if int(group["id"]) == int(required_group)
        ]

        return len(admin_groups) > 0

    def has_camac_edit_permission(self, target, info, required_permission="write"):
        if isinstance(target, Case):
            case = target
            permission_key = "case-meta"
        elif isinstance(target, Document):
            case = Case.objects.filter(
                Q(work_items__document_id=target.pk) | Q(document_id=target.pk)
            ).first()

            if not case:
                # if the document is unlinked, allow changing it this is used for
                # new table rows
                return True

            permission_key = "main" if target == case.document else target.form.slug
        else:
            return False

        instance_id = case.meta.get("camac-instance-id")

        resp = requests.get(
            build_url(settings.INTERNAL_BASE_URL, f"/api/v1/instances/{instance_id}"),
            headers=headers(info),
        )

        resp.raise_for_status()

        try:
            jsondata = resp.json()
            if "error" in jsondata:
                raise RuntimeError("Error from NG API: %s" % jsondata["error"])

            permissions = jsondata["data"]["meta"]["permissions"]

            return required_permission in permissions.get(permission_key, [])

        except KeyError:
            raise RuntimeError(
                f"NG API returned unexpected data structure (no data key) {jsondata}"
            )
