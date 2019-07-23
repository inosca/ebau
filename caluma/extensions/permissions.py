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

from .visibilities import group, role

log = getLogger()

"""Caluma permissions for Kanton Bern"""

INSTANCE_STATES = {
    "gesuchsteller": ["1", "10000"],  # Neu, Zurückgewiesen
    "internal": ["20000", "20007"],  # eBau-Nummer zu vergeben, in Korrektur
}


class CustomPermission(BasePermission):
    @object_permission_for(Mutation)
    def has_object_permission_default(self, mutation, info, instance):
        operation = mutation.__name__
        log.debug(
            f"ACL: fallback object permission: rejecting "
            f"mutation '{operation}' on {instance}"
        )
        return False

    @permission_for(Mutation)
    def has_permission_default(self, mutation, info):
        operation = mutation.__name__
        log.debug(f"fallback permission: rejecting mutation '{operation}'")
        return False

    # Document
    @permission_for(SaveDocument)
    def has_permission_for_savedocument(self, mutation, info):
        log.debug("ACL: SaveDocument permission")
        return True

    @object_permission_for(SaveDocument)
    def has_object_permission_for_savedocument(self, mutation, info, instance):
        log.debug("ACL: SaveDocument object permission")
        return self.has_camac_edit_permission(instance.family, info)

    # Answer
    @permission_for(SaveDocumentAnswer)
    def has_permission_for_savedocumentanswer(self, mutation, info):
        return True

    @object_permission_for(SaveDocumentAnswer)
    def has_object_permission_for_savedocumentanswer(self, mutation, info, instance):
        return self.has_camac_edit_permission(instance.document.family, info)

    @permission_for(RemoveAnswer)
    def has_permission_for_removeanswer(self, mutation, info):
        return True

    @object_permission_for(RemoveAnswer)
    def has_object_permission_for_removeanswer(self, mutation, info, instance):
        return self.has_camac_edit_permission(instance.document.family, info)

    def has_camac_edit_permission(self, document_family, info):
        # find corresponding document
        document = Document.objects.get(id=document_family)

        camac_api = os.environ.get("CAMAC_NG_URL", "http://camac-ng.local").strip("/")
        instance_id = document.meta.get("camac-instance-id")

        if not instance_id:
            # if the document is unlinked, allow changing it
            # this is used for new table rows
            return True

        resp = requests.get(
            f"{camac_api}/api/v1/instances/{instance_id}?include=instance-state",
            # forward role as filter
            {"role": role(info), "group": group(info)},
            # Forward authorization header
            headers={"Authorization": info.context.META.get("HTTP_AUTHORIZATION")},
        )

        resp.raise_for_status()

        try:
            jsondata = resp.json()
            if "error" in jsondata:
                raise RuntimeError("Error from NG API: %s" % jsondata["error"])

            instance_state_id = jsondata["data"]["relationships"]["instance-state"][
                "data"
            ]["id"]

            log.debug(f"ACL: Camac NG instance state: {instance_state_id}")
            return instance_state_id in INSTANCE_STATES[role(info)]

        except KeyError:
            raise RuntimeError(
                f"NG API returned unexpected data structure (no data key) {jsondata}"
            )
