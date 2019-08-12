import json
import os
from logging import getLogger

import requests
from django.core.exceptions import ObjectDoesNotExist

from caluma.core.mutation import Mutation
from caluma.core.permissions import (
    BasePermission,
    object_permission_for,
    permission_for,
)
from caluma.form.schema import RemoveAnswer, SaveDocument, SaveDocumentAnswer
from caluma.form.models import Document

from .visibilities import group

log = getLogger()

CAMAC_NG_URL = os.environ.get("CAMAC_NG_URL", "http://camac-ng.local").strip("/")

CAMAC_ADMIN_GROUPS = ["1"]  # Admin


class CustomPermission(BasePermission):
    @object_permission_for(Mutation)
    def has_object_permission_default(self, mutation, info, instance):
        log.debug(
            f"ACL: fallback object permission: allowing "
            f"mutation '{mutation.__name__}' on {instance} for admin users"
        )

        return self.has_camac_admin_permission(info)

    @permission_for(Mutation)
    def has_permission_default(self, mutation, info):
        log.debug(
            f"ACL: fallback permission: allow mutation '{mutation.__name__}' for admins"
        )

        return self.has_camac_admin_permission(info)

    # Document
    @permission_for(SaveDocument)
    def has_permission_for_savedocument(self, mutation, info):
        return True

    @object_permission_for(SaveDocument)
    def has_object_permission_for_savedocument(self, mutation, info, instance):
        return self.has_camac_edit_permission(instance.family, info, "write-meta")

    # Answer
    @permission_for(SaveDocumentAnswer)
    def has_permission_for_savedocumentanswer(self, mutation, info):
        document = Document.objects.get(
            pk=json.loads(info.context.body)["variables"]["input"]["document"]
        )

        return self.has_camac_edit_permission(document.family, info)

    @object_permission_for(SaveDocumentAnswer)
    def has_object_permission_for_savedocumentanswer(self, mutation, info, instance):
        return self.has_camac_edit_permission(instance.document.family, info)

    @permission_for(RemoveAnswer)
    def has_permission_for_removeanswer(self, mutation, info):
        answer = json.loads(info.context.body)["variables"]["input"]["answer"]
        document = Document.objects.get(answers__pk=answer)

        return self.has_camac_edit_permission(document.family, info)

    @object_permission_for(RemoveAnswer)
    def has_object_permission_for_removeanswer(self, mutation, info, instance):
        return self.has_camac_edit_permission(instance.document.family, info)

    def has_camac_admin_permission(self, info):
        response = requests.get(
            f"{CAMAC_NG_URL}/api/v1/me",
            headers={"Authorization": info.context.META.get("HTTP_AUTHORIZATION")},
        )

        response.raise_for_status()

        admin_groups = [
            group
            for group in response.json()["data"]["relationships"]["groups"]
            if group["id"] in CAMAC_ADMIN_GROUPS
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
            f"{CAMAC_NG_URL}/api/v1/instances/{instance_id}",
            # forward group as filter
            {"group": group(info)},
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
