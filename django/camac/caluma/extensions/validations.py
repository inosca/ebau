#!/usr/bin/env python3

# This file will contain custom validations for CALUMA-BE.
#
# Currently, this is only a sketch of what needs to be done, and is only here
# so it doesn't get forgotten.


import json

import requests
from caluma.caluma_core.validations import BaseValidation, validation_for
from caluma.caluma_form.models import Answer, Document
from caluma.caluma_form.schema import SaveDocumentStringAnswer, SaveDocumentTableAnswer

from . import common
from .utils import build_url

CLAIM_QUESTION = "nfd-tabelle-table"
CLAIM_STATUS_QUESTION = "nfd-tabelle-status"
CLAIM_STATUS_IN_PROGRESS = "nfd-tabelle-status-in-bearbeitung"
CLAIM_STATUS_ANSWERED = "nfd-tabelle-status-beantwortet"

NOTIFICATION_CLAIM_IN_PROGRESS = 31
NOTIFICATION_CLAIM_ANSWERED = 32
ECH_EVENT_CLAIM_ANSWERED = "FileSubsequently"


class CustomValidation(BaseValidation):
    def _send_claim_notification(self, info, instance_id, template_id, recipient_types):
        requests.post(
            build_url(
                common.CAMAC_NG_URL,
                f"/api/v1/notification-templates/{template_id}/sendmail",
            ),
            headers={
                "content-type": "application/vnd.api+json",
                **common.headers(info),
            },
            data=json.dumps(
                {
                    "data": {
                        "type": "notification-template-sendmails",
                        "attributes": {"recipient_types": recipient_types},
                        "relationships": {
                            "instance": {
                                "data": {"type": "instances", "id": instance_id}
                            }
                        },
                    }
                }
            ),
        )

    def _send_claim_ech_event(self, info, instance_id, event):
        if common.ECH_API:
            requests.post(
                build_url(
                    common.CAMAC_NG_URL,
                    f"/ech/v1/event/{instance_id}/{event}",
                    trailing=True,
                ),
                headers={"authorization": f"Bearer {common.get_admin_token()}"},
            )

    def _validate_claim_status(self, info, instance_id, status, old_status=None):
        if old_status and status == old_status:
            # the status did not change, no further action
            return

        if status == CLAIM_STATUS_IN_PROGRESS:
            self._send_claim_notification(
                info, instance_id, NOTIFICATION_CLAIM_IN_PROGRESS, ["applicant"]
            )

        if status == CLAIM_STATUS_ANSWERED:
            self._send_claim_notification(
                info, instance_id, NOTIFICATION_CLAIM_ANSWERED, ["leitbehoerde"]
            )
            self._send_claim_ech_event(info, instance_id, ECH_EVENT_CLAIM_ANSWERED)

    @validation_for(SaveDocumentTableAnswer)
    def validate_save_document_table_answer(self, mutation, data, info):
        if data["question"].slug == CLAIM_QUESTION:
            try:
                instance_id = data["document"].meta["camac-instance-id"]

                try:
                    old_documents = (
                        data["document"]
                        .answers.get(question=CLAIM_QUESTION)
                        .documents.all()
                    )
                except Answer.DoesNotExist:
                    # this is the first added document
                    old_documents = []

                new_document = (set(data["documents"]) - set(old_documents)).pop()

                self._validate_claim_status(
                    info,
                    instance_id,
                    new_document.answers.get(question=CLAIM_STATUS_QUESTION).value,
                )
            except KeyError:
                # no new documents added
                pass

        return data

    @validation_for(SaveDocumentStringAnswer)
    def validate_save_document_string_answer(self, mutation, data, info):
        if data["question"].slug == CLAIM_STATUS_QUESTION:
            try:
                self._validate_claim_status(
                    info,
                    Document.objects.get(pk=data["document"].family).meta[
                        "camac-instance-id"
                    ],
                    data["value"],
                    data["document"].answers.get(question=CLAIM_STATUS_QUESTION).value,
                )
            except KeyError:
                # the document is not linked yet (no camac-instance-id)
                pass

        return data
