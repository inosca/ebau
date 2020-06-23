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
from django.conf import settings

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
    def has_object_permission_for_savedocument(self, mutation, info, instance):
        if instance.form.slug == DASHBOARD_FORM_SLUG:
            return self.has_camac_group_permission(info, CAMAC_SUPPORT_GROUP)

        return self.has_camac_edit_permission(instance.family, info, "write-meta")

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
    def has_object_permission_for_savedocumentanswer(self, mutation, info, instance):
        if instance.document.form.slug == DASHBOARD_FORM_SLUG:
            return self.has_camac_group_permission(info, CAMAC_SUPPORT_GROUP)

        return self.has_camac_edit_permission(instance.document.family, info)

    @permission_for(RemoveAnswer)
    def has_permission_for_removeanswer(self, mutation, info):
        answer = json.loads(info.context.body)["variables"]["input"]["answer"]
        document = Document.objects.get(answers__pk=answer)

        return self.has_camac_edit_permission(document.family, info)

    @object_permission_for(RemoveAnswer)
    def has_object_permission_for_removeanswer(self, mutation, info, instance):
        return self.has_camac_edit_permission(instance.document.family, info)

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

    def has_camac_edit_permission(
        self, family_document, info, required_permission="write"
    ):
        # Get the instance ID for the related case. It might happen that the
        # document is not yet linked to a case (table)
        try:
            instance_id = family_document.case.meta.get("camac-instance-id")
        except Document.case.RelatedObjectDoesNotExist:
            # if the document is unlinked, allow changing it this is used for
            # new table rows
            return True

        resp = requests.get(
            build_url(settings.INTERNAL_BASE_URL, f"/api/v1/instances/{instance_id}"),
            headers=headers(info),
        )

        resp.raise_for_status()

        try:
            jsondata = resp.json()
            if "error" in jsondata:
                raise RuntimeError("Error from NG API: %s" % jsondata["error"])

            is_main_form = family_document.form.meta.get("is-main-form", False)

            return required_permission in jsondata["data"]["meta"]["permissions"].get(
                "main" if is_main_form else family_document.form.slug, []
            )

        except KeyError:
            raise RuntimeError(
                f"NG API returned unexpected data structure (no data key) {jsondata}"
            )
