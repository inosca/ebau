import json
from logging import getLogger

import requests
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from rest_framework.authentication import get_authorization_header
from rest_framework.serializers import ValidationError
from rest_framework_json_api import serializers

from .. import models
from ...core import models as core_models
from .common import InstanceSerializer

request_logger = getLogger("django.request")

INSTANCE_STATE_SUBMITTED = 20000
INSTANCE_STATE_NEW = 1


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

    def validate_instance_state(self, value):
        if not self.instance:  # pragma: no cover
            request_logger.info("Creating new instance, overriding %s" % value)
            return models.InstanceState.objects.get(pk=INSTANCE_STATE_NEW)
        return value

    def _is_submit(self, data):
        if self.instance:
            old_version = models.Instance.objects.get(pk=self.instance.pk)
            return (
                old_version.instance_state_id != data.get("instance_state").pk
                and data.get("instance_state").pk == INSTANCE_STATE_SUBMITTED
            )

    def validate(self, data):
        request_logger.info(f"validating instance {data.keys()}")
        case_id = data.get("caluma_case_id")

        # Fetch case data and meta information. Validate that the case doesn't
        # have another instance assigned already, and at the same time store
        # the data we need to update the case later on.
        request_logger.info("Fetching Caluma case info to validate instance creation")
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
                          document {
                            id
                            form {
                              slug
                            }
                            answers(questions: ["gemeinde", "3-grundstueck"]) {
                              edges {
                                node {
                                  id
                                  question {
                                    slug
                                  }
                                  ... on StringAnswer {
                                    stringValue: value
                                  }
                                  ...on FormAnswer {
                                    formValue: value {
                                      id
                                      answers(question: "allgemeine-angaben") {
                                        edges {
                                          node {
                                            id
                                            ...on FormAnswer {
                                              formValue: value {
                                                id
                                                answers(question: "gemeinde") {
                                                  edges {
                                                    node {
                                                      id
                                                      ... on StringAnswer {
                                                        stringValue: value
                                                      }
                                                      question {
                                                        slug
                                                      }
                                                    }
                                                  }
                                                }
                                              }
                                            }
                                          }
                                        }
                                      }
                                    }
                                  }
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
        request_logger.info("Caluma case information: %s", data["caluma_case_data"])

        if not self._is_submit(data):
            case_meta = data["caluma_case_data"]["meta"]
            if "camac-instance-id" in case_meta:  # pragma: no cover
                # Already linked. this should not be, as we just
                # created a new Camac instance for a caluma case that
                # has already an instance assigned
                raise ValidationError(
                    f"Caluma case already has an instance id "
                    f"assigned: {case_meta['camac-instance-id']}"
                )
        else:
            work_items = data["caluma_case_data"]["workItems"]["edges"]
            # Ensure case is actually completely filled
            for item in work_items:
                task_slug = item["node"]["task"]["slug"]
                item_status = item["node"]["status"]
                if task_slug == "fill-form" and item_status != "COMPLETED":
                    raise ValidationError(
                        "Cannot create instance before form is filled correctly"
                    )

        return data

    def create(self, validated_data):  # pragma: no cover
        case_id = validated_data.pop("caluma_case_id")
        case_data = validated_data.pop("caluma_case_data")
        case_meta = case_data["meta"]

        created = super().create(validated_data)

        created.involved_applicants.create(
            user=self.context["request"].user,
            invitee=self.context["request"].user,
            created=timezone.now(),
        )

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

        return created

    @transaction.atomic
    def update(self, instance, validated_data):
        request_logger.info("Updating instance %s" % instance.pk)

        if not self._is_submit(validated_data):
            raise ValidationError(f"Updating cases is only allowed for submitting")

        validated_data["modification_date"] = timezone.now()
        self.instance.instance_state = models.InstanceState.objects.get(
            pk=INSTANCE_STATE_SUBMITTED
        )
        form = validated_data.get("caluma_case_data")["document"]["form"]["slug"]
        first_answer = validated_data.get("caluma_case_data")["document"]["answers"][
            "edges"
        ][0]["node"]

        service_id = None
        try:
            if form == "vorabklaerung-einfach":
                service_id = int(first_answer["stringValue"])
            else:  # pragma: no cover
                service_id = first_answer["formValue"]["answers"]["edges"][0]["node"][
                    "formValue"
                ]["answers"]["edges"][0]["node"]["stringValue"]
        except (KeyError, IndexError):  # pragma: no cover
            pass

        if not service_id:  # pragma: no cover
            request_logger.error("!!!Municipality not found!!!")
            service_id = 2  # default to Burgdorf

        core_models.InstanceService.objects.get_or_create(
            instance=self.instance,
            service_id=service_id,
            active=1,
            defaults={"activation_date": None},
        )

        self.instance.save()

        return instance

    class Meta(InstanceSerializer.Meta):
        fields = InstanceSerializer.Meta.fields + ("caluma_case_id",)
