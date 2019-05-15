import json
from logging import getLogger

import requests
from django.conf import settings
from rest_framework.authentication import get_authorization_header
from rest_framework.serializers import ValidationError
from rest_framework_json_api import serializers

from .. import models
from ...core import models as core_models
from .common import InstanceSerializer

log = getLogger()


class BernInstanceSerializer(InstanceSerializer):

    instance_state = serializers.ResourceRelatedField(
        queryset=models.InstanceState.objects.all(),
        default=lambda: models.InstanceState.objects.order_by(
            "instance_state_id"
        ).first(),
    )
    previous_instance_state = serializers.ResourceRelatedField(
        queryset=models.InstanceState.objects.all(),
        default=lambda: models.InstanceState.objects.order_by(
            "instance_state_id"
        ).first(),
    )

    caluma_case_id = serializers.CharField(required=False)

    def validate(self, data):
        case_id = data.get("caluma_case_id")

        # Fetch case data and meta information. Validate that the case doesn't
        # have another instance assigned already, and at the same time store
        # the data we need to update the case later on.
        log.debug("Fetching Caluma case info to validate instance creation")
        caluma_resp = requests.post(
            settings.CALUMA_URL,
            json={
                "query": """
                    query ($case_id: ID!) {
                      node(id:$case_id) {
                        ... on Case {
                          id
                          meta
                          workflow {
                            id
                          }
                          workItems {
                            edges {
                              node {
                                status
                                task {
                                  slug
                                }
                              }
                            }
                          }
                        }
                      }
                    }
                """,
                "variables": {"case_id": case_id},
            },
            headers={
                "Authorization": get_authorization_header(self.context["request"])
            },
        )
        data["caluma_case_data"] = caluma_resp.json()["data"]["node"]
        log.debug("Caluma case information: %s", data["caluma_case_data"])

        # case_meta = data["caluma_case_data"]["meta"]
        # work_items = data["caluma_case_data"]["workItems"]["edges"]

        # Ensure case is actually completely filled
        # for item in work_items:
        #     task_slug = item["node"]["task"]["slug"]
        #     item_status = item["node"]["status"]
        #     if task_slug == "fill-form" and item_status != "COMPLETED":
        #         raise ValidationError(
        #             "Cannot create instance before form is filled correctly"
        #         )

        # if "camac-instance-id" in case_meta:
        #     # Already linked. this should not be, as we just
        #     # created a new Camac instance for a caluma case that
        #     # has already an instance assigned
        #     raise ValidationError(
        #         f"Caluma case already has an instance id "
        #         f"assigned: {case_meta['camac-instance-id']}"
        #     )

        return data

    def create(self, validated_data):
        case_id = validated_data.pop("caluma_case_id")
        case_data = validated_data.pop("caluma_case_data")
        case_meta = case_data["meta"]

        created = super().create(validated_data)

        # Now, add instance id to case
        case_meta["camac-instance-id"] = created.pk

        caluma_resp = requests.post(
            settings.CALUMA_URL,
            json={
                "query": """
                       mutation save_instance_id ($input: SaveCaseInput!) {
                         saveCase (input: $input) {
                           case {
                             id
                             meta
                           }
                         }
                       }
                """,
                "variables": {
                    "input": {
                        "id": case_id,
                        "meta": json.dumps(case_meta),
                        "workflow": case_data["workflow"]["id"],
                    }
                },
            },
            headers={
                "Authorization": get_authorization_header(self.context["request"])
            },
        )
        if caluma_resp.status_code not in (200, 201):  # pragma: no cover
            raise ValidationError("Error while linking case and instance")

        core_models.InstanceService.objects.create(
            instance=created, service_id=2, active=1
        )

        return created

    class Meta(InstanceSerializer.Meta):
        fields = InstanceSerializer.Meta.fields + ("caluma_case_id",)
