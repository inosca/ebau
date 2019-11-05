#!/usr/bin/env python3

# This file will contain custom validations for CALUMA-BE.
#
# Currently, this is only a sketch of what needs to be done, and is only here
# so it doesn't get forgotten.


import requests

from caluma.core.validations import BaseValidation, validation_for
from caluma.form.models import Document
from caluma.form.schema import SaveDocumentAnswer

from . import common


def _send_notification_to_ng(instance_id, event_name, info):
    requests.post(
        f"{common.CAMAC_NG_URL}/ech/v1/event/{instance_id}/{event_name}",
        headers={"Authorization": f"Bearer {common.get_admin_token()}"},
    )
    pass


class CustomValidation(BaseValidation):
    @validation_for(SaveDocumentAnswer)
    def validate_answer_mutation(self, mutation, data, info):
        # TODO (validation SaveAnswer mutation): check if "gesuchsteller" email
        # question. If yes, validate email exists in NG user database

        if (
            data["question"].slug == "nfd-tabelle-status"
            and data["value"] == "nfd-tabelle-status-beantwortet"
        ):
            main_doc = Document.objects.get(pk=data["document"].family)
            print(main_doc.meta)
            _send_notification_to_ng(
                main_doc.meta["camac-instance-id"], "FileSubsequently", info
            )
        return data
