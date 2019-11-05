import json
from logging import getLogger

import requests

from caluma.core.mutation import Mutation
from caluma.core.permissions import (
    BasePermission,
    object_permission_for,
    permission_for,
)
from caluma.form.models import Document
from caluma.form.schema import RemoveAnswer, SaveDocument, SaveDocumentAnswer

from . import common

log = getLogger()


class CustomPermission(BasePermission):
    @object_permission_for(Mutation)
    def has_object_permission_default(self, mutation, info, instance):
        log.debug(
            f"ACL: fallback object permission: allowing "
            f"mutation '{mutation.__name__}' on {instance} for admin users"
        )

        return self.has_camac_group_permission(info, common.CAMAC_ADMIN_GROUP)

    @permission_for(Mutation)
    def has_permission_default(self, mutation, info):
        log.debug(
            f"ACL: fallback permission: allow mutation '{mutation.__name__}' for admins"
        )

        return self.has_camac_group_permission(info, common.CAMAC_ADMIN_GROUP)

    # Document
    @permission_for(SaveDocument)
    def has_permission_for_savedocument(self, mutation, info):
        if self.get_input_variables(info).get("form") == common.DASHBOARD_FORM_SLUG:
            # There should only be one dashboard document which has to be
            # created by a support user
            return (
                self.has_camac_group_permission(info, common.CAMAC_SUPPORT_GROUP)
                and Document.objects.filter(
                    form__slug=common.DASHBOARD_FORM_SLUG
                ).count()
                == 0
            )

        return True

    @object_permission_for(SaveDocument)
    def has_object_permission_for_savedocument(self, mutation, info, instance):
        if instance.form.slug == common.DASHBOARD_FORM_SLUG:
            return self.has_camac_group_permission(info, common.CAMAC_SUPPORT_GROUP)

        return self.has_camac_edit_permission(instance.family, info, "write-meta")

    # Answer
    @permission_for(SaveDocumentAnswer)
    def has_permission_for_savedocumentanswer(self, mutation, info):
        document = Document.objects.get(
            pk=self.get_input_variables(info)["input"]["document"]
        )

        if document.form.slug == common.DASHBOARD_FORM_SLUG:
            return self.has_camac_group_permission(info, common.CAMAC_SUPPORT_GROUP)

        return self.has_camac_edit_permission(document.family, info)

    @object_permission_for(SaveDocumentAnswer)
    def has_object_permission_for_savedocumentanswer(self, mutation, info, instance):
        if instance.document.form.slug == common.DASHBOARD_FORM_SLUG:
            return self.has_camac_group_permission(info, common.CAMAC_SUPPORT_GROUP)

        return self.has_camac_edit_permission(instance.document.family, info)

    @permission_for(RemoveAnswer)
    def has_permission_for_removeanswer(self, mutation, info):
        answer = json.loads(info.context.body)["variables"]["input"]["answer"]
        document = Document.objects.get(answers__pk=answer)

        return self.has_camac_edit_permission(document.family, info)

    @object_permission_for(RemoveAnswer)
    def has_object_permission_for_removeanswer(self, mutation, info, instance):
        return self.has_camac_edit_permission(instance.document.family, info)

    def get_input_variables(self, info):
        body = json.loads(info.context.body)

        return body.get("variables", {})

    def has_camac_group_permission(self, info, required_group):
        response = requests.get(
            f"{common.CAMAC_NG_URL}/api/v1/me",
            headers={"Authorization": info.context.META.get("HTTP_AUTHORIZATION")},
        )

        response.raise_for_status()

        admin_groups = [
            group
            for group in response.json()["data"]["relationships"]["groups"]["data"]
            if int(group["id"]) == int(required_group)
        ]

        return len(admin_groups) > 0

    def has_camac_edit_permission(
        self, document_family, info, required_permission="write"
    ):
        # find corresponding document
        document = Document.objects.get(id=document_family)
        instance_id = document.meta.get("camac-instance-id")

        if not instance_id:
            # if the document is unlinked, allow changing it
            # this is used for new table rows
            return True

        resp = requests.get(
            f"{common.CAMAC_NG_URL}/api/v1/instances/{instance_id}",
            # forward group as filter
            {"group": common.group(info)},
            # Forward authorization header
            headers={"Authorization": info.context.META.get("HTTP_AUTHORIZATION")},
        )

        resp.raise_for_status()

        try:
            jsondata = resp.json()
            if "error" in jsondata:
                raise RuntimeError("Error from NG API: %s" % jsondata["error"])

            is_main_form = document.form.meta.get("is-main-form", False)

            return required_permission in jsondata["data"]["meta"]["permissions"].get(
                "main" if is_main_form else document.form.slug, []
            )

        except KeyError:
            raise RuntimeError(
                f"NG API returned unexpected data structure (no data key) {jsondata}"
            )
