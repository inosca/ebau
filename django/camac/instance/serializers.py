import json
from logging import getLogger

import requests
from django.conf import settings
from django.db import transaction
from django.db.models import Max
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header
from rest_framework_json_api import relations, serializers

from camac.constants import kt_bern as constants
from camac.core.models import Answer, InstanceLocation, InstanceService, Question
from camac.core.serializers import MultilingualSerializer
from camac.instance.mixins import InstanceEditableMixin
from camac.notification.serializers import NotificationTemplateSendmailSerializer
from camac.user.models import Group
from camac.user.relations import (
    CurrentUserResourceRelatedField,
    FormDataResourceRelatedField,
    GroupResourceRelatedField,
    ServiceResourceRelatedField,
)
from camac.user.serializers import CurrentGroupDefault, CurrentServiceDefault

from . import models, validators

SUBMIT_DATE_CHAPTER = 100001
SUBMIT_DATE_QUESTION_ID = 20036

request_logger = getLogger("django.request")


class NewInstanceStateDefault(object):
    def __call__(self):
        return models.InstanceState.objects.get(name="new")


class InstanceStateSerializer(MultilingualSerializer, serializers.ModelSerializer):
    class Meta:
        model = models.InstanceState
        fields = ("name", "description")


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Form
        fields = ("name", "description")


class InstanceSerializer(InstanceEditableMixin, serializers.ModelSerializer):
    editable = serializers.SerializerMethodField()
    user = CurrentUserResourceRelatedField()
    group = GroupResourceRelatedField(default=CurrentGroupDefault())

    instance_state = serializers.ResourceRelatedField(
        queryset=models.InstanceState.objects.filter(name="new"),
        default=NewInstanceStateDefault(),
    )

    previous_instance_state = serializers.ResourceRelatedField(
        queryset=models.InstanceState.objects.filter(name="new"),
        default=NewInstanceStateDefault(),
    )

    included_serializers = {
        "location": "camac.user.serializers.LocationSerializer",
        "user": "camac.user.serializers.UserSerializer",
        "group": "camac.user.serializers.GroupSerializer",
        "form": FormSerializer,
        "instance_state": InstanceStateSerializer,
        "previous_instance_state": InstanceStateSerializer,
        "circulations": "camac.circulation.serializers.CirculationSerializer",
    }

    def validate_location(self, location):
        if self.instance and self.instance.identifier:
            if self.instance.location != location:
                raise exceptions.ValidationError(_("Location may not be changed."))

        return location

    def validate_form(self, form):
        if self.instance and self.instance.identifier:
            if self.instance.form != form:
                raise exceptions.ValidationError(_("Form may not be changed."))

        return form

    @transaction.atomic
    def create(self, validated_data):
        validated_data["modification_date"] = timezone.now()
        validated_data["creation_date"] = timezone.now()
        instance = super().create(validated_data)

        if instance.location_id is not None:
            self._update_instance_location(instance)

        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        validated_data["modification_date"] = timezone.now()
        old_location_id = instance.location_id
        instance = super().update(instance, validated_data)

        if instance.location_id != old_location_id:
            self._update_instance_location(instance)

        return instance

    def _update_instance_location(self, instance):
        """
        Set the location also in the InstanceLocation table.

        The API uses the location directly on the instance,
        but some Camac core functions need the location in
        the InstanceLocation table.
        """
        InstanceLocation.objects.filter(instance=instance).delete()
        if instance.location_id is not None:
            InstanceLocation.objects.create(
                instance=instance, location_id=instance.location_id
            )

    class Meta:
        model = models.Instance
        meta_fields = ("editable",)
        fields = (
            "instance_id",
            "instance_state",
            "identifier",
            "location",
            "form",
            "user",
            "group",
            "creation_date",
            "modification_date",
            "previous_instance_state",
            "circulations",
        )
        read_only_fields = (
            "circulations",
            "creation_date",
            "identifier",
            "modification_date",
        )


class CalumaInstanceSerializer(InstanceSerializer):
    # TODO once more than Camac-NG project uses Caluma as a form
    # this serializer needs to be split up into what is actually
    # Caluma and what is project specific
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

    public_status = serializers.SerializerMethodField()

    def get_public_status(self, instance):
        STATUS_MAP = {
            constants.INSTANCE_STATE_NEW: constants.PUBLIC_INSTANCE_STATE_CREATING,
            constants.INSTANCE_STATE_EBAU_NUMMER_VERGEBEN: constants.PUBLIC_INSTANCE_STATE_RECEIVING,
            constants.INSTANCE_STATE_FORMELLE_PRUEFUNG: constants.PUBLIC_INSTANCE_STATE_COMMUNAL,
            constants.INSTANCE_STATE_MATERIELLE_PRUEFUNG: constants.PUBLIC_INSTANCE_STATE_COMMUNAL,
            constants.INSTANCE_STATE_DOSSIERPRUEFUNG: constants.PUBLIC_INSTANCE_STATE_COMMUNAL,
            constants.INSTANCE_STATE_CORRECTION_IN_PROGRESS: constants.PUBLIC_INSTANCE_STATE_COMMUNAL,
            constants.INSTANCE_STATE_KOORDINATION: constants.PUBLIC_INSTANCE_STATE_INIT_PROGRAM,
            constants.INSTANCE_STATE_VERFAHRENSPROGRAMM_INIT: constants.PUBLIC_INSTANCE_STATE_INIT_PROGRAM,
            constants.INSTANCE_STATE_ZIRKULATION: constants.PUBLIC_INSTANCE_STATE_INIT_PROGRAM,
            constants.INSTANCE_STATE_REJECTED: constants.PUBLIC_INSTANCE_STATE_REJECTED,
            constants.INSTANCE_STATE_CORRECTED: constants.PUBLIC_INSTANCE_STATE_CORRECTED,
            constants.INSTANCE_STATE_SELBSTDEKLARATION_AUSSTEHEND: constants.PUBLIC_INSTANCE_STATE_SELBSTDEKLARATION,
            constants.INSTANCE_STATE_SELBSTDEKLARATION_FREIGABEQUITTUNG: constants.PUBLIC_INSTANCE_STATE_SELBSTDEKLARATION,
            constants.INSTANCE_STATE_ABSCHLUSS_AUSSTEHEND: constants.PUBLIC_INSTANCE_STATE_ABSCHLUSS,
            constants.INSTANCE_STATE_ABSCHLUSS_DOKUMENTE: constants.PUBLIC_INSTANCE_STATE_ABSCHLUSS,
            constants.INSTANCE_STATE_ABSCHLUSS_FREIGABEQUITTUNG: constants.PUBLIC_INSTANCE_STATE_ABSCHLUSS,
            constants.INSTANCE_STATE_TO_BE_FINISHED: constants.PUBLIC_INSTANCE_STATE_FINISHED,
            constants.INSTANCE_STATE_FINISHED: constants.PUBLIC_INSTANCE_STATE_FINISHED,
        }

        return STATUS_MAP.get(
            instance.instance_state_id, constants.PUBLIC_INSTANCE_STATE_CREATING
        )

    def validate_instance_state(self, value):
        if not self.instance:  # pragma: no cover
            request_logger.info("Creating new instance, overriding %s" % value)
            return models.InstanceState.objects.get(trans__name="Neu")
        return value

    def _is_submit(self, data):
        if self.instance:
            old_version = models.Instance.objects.get(pk=self.instance.pk)
            return (
                old_version.instance_state_id != data.get("instance_state").pk
                and old_version.instance_state.get_name() in ["Neu", "Zurückgewiesen"]
                and data.get("instance_state").get_name() == "eBau-Nummer zu vergeben"
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
                          document {
                            id
                            form {
                              slug
                            }
                            answers(questions: ["gemeinde"]) {
                              edges {
                                node {
                                  id
                                  question {
                                    slug
                                  }
                                  ... on StringAnswer {
                                    stringValue: value
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
                raise exceptions.ValidationError(
                    f"Caluma case already has an instance id "
                    f"assigned: {case_meta['camac-instance-id']}"
                )
        else:
            # TODO ask caluma if case is actually valid
            pass

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

        caluma_resp = self._save_case(case_id, case_meta, case_data["workflow"]["id"])
        if caluma_resp.status_code not in (200, 201):  # pragma: no cover
            raise exceptions.ValidationError("Error while linking case and instance")

        return created

    def _save_case(self, case_id, case_meta, workflow_id):
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
                        "workflow": workflow_id,
                    }
                },
            },
            headers={
                "Authorization": get_authorization_header(self.context["request"])
            },
        )
        return caluma_resp

    @transaction.atomic
    def update(self, instance, validated_data):
        request_logger.info("Updating instance %s" % instance.pk)

        if not self._is_submit(validated_data):
            raise exceptions.ValidationError(
                f"Updating cases is only allowed for submitting"
            )

        validated_data["modification_date"] = timezone.now()

        if instance.instance_state.get_name() == "Zurückgewiesen":
            self.instance.instance_state = instance.previous_instance_state
        else:
            self.instance.instance_state = models.InstanceState.objects.get(
                trans__name="eBau-Nummer zu vergeben"
            )
        form = validated_data.get("caluma_case_data")["document"]["form"]["slug"]

        service_id = None
        try:
            first_answer = validated_data.get("caluma_case_data")["document"][
                "answers"
            ]["edges"][0]["node"]

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

        InstanceService.objects.get_or_create(
            instance=self.instance,
            service_id=service_id,
            active=1,
            defaults={"activation_date": None},
        )

        self.instance.save()

        self._set_submit_date(validated_data)

        # send out emails upon submission
        for notification_config in settings.APPLICATION["NOTIFICATIONS"]["SUBMIT"]:
            self.notify_submit(**notification_config)

        return instance

    def _set_submit_date(self, validated_data):
        case_data = validated_data["caluma_case_data"]

        if "submit-date" in case_data["meta"]:  # pragma: no cover
            # instance was already submitted, this is probably a re-submit
            # after correction.
            return

        # Set submit date in Camac first...
        subm_question = Question.objects.get(pk=SUBMIT_DATE_QUESTION_ID)
        subm_ans, _ = Answer.objects.get_or_create(
            instance=self.instance,
            question=subm_question,
            item=1,
            chapter_id=SUBMIT_DATE_CHAPTER,
            # CAMAC date is formatted in "dd.mm.yyyy"
            defaults={"answer": timezone.now().strftime("%d.%m.%Y")},
        )
        new_meta = {
            **case_data["meta"],
            # Caluma date is formatted yyyy-mm-dd so it can be sorted
            "submit-date": timezone.now().strftime("%Y-%m-%d"),
        }
        self._save_case(case_data["id"], new_meta, case_data["workflow"]["id"])

    def notify_submit(self, template_id, recipient_types):
        """Send notification email."""

        # fake jsonapi request for notification serializer
        mail_data = {
            "instance": {"type": "instances", "id": self.instance.pk},
            "notification_template": {
                "type": "notification-templates",
                "id": template_id,
            },
            "recipient_types": recipient_types,
        }

        mail_serializer = NotificationTemplateSendmailSerializer(
            self.instance, mail_data, context=self.context
        )

        if not mail_serializer.is_valid():  # pragma: no cover
            errors = "; ".join(
                [f"{field}: {msg}" for field, msg in mail_serializer.errors.items()]
            )
            message = f"Cannot send email: {errors}"
            request_logger.error(message)
            raise exceptions.ValidationError(message)

        mail_serializer.create(mail_serializer.validated_data)

    class Meta(InstanceSerializer.Meta):
        fields = InstanceSerializer.Meta.fields + ("caluma_case_id", "public_status")
        read_only_fields = InstanceSerializer.Meta.read_only_fields + ("public_status",)


class InstanceResponsibilitySerializer(
    InstanceEditableMixin, serializers.ModelSerializer
):
    instance_editable_permission = None
    service = ServiceResourceRelatedField(default=CurrentServiceDefault())

    def validate(self, data):
        user = data.get("user", self.instance and self.instance.user)
        service = data.get("service", self.instance and self.instance.service)

        if service.pk not in user.groups.values_list("service_id", flat=True):
            raise exceptions.ValidationError(
                _("User %(user)s does not belong to service %(service)s.")
                % {"user": user.username, "service": service.name}
            )

        return data

    class Meta:
        model = models.InstanceResponsibility
        fields = ("user", "service", "instance")

        included_serializers = {
            "instance": InstanceSerializer,
            "service": "camac.user.serializers.ServiceSerializer",
            "user": "camac.user.serializers.UserSerializer",
        }


class InstanceSubmitSerializer(InstanceSerializer):
    instance_state = FormDataResourceRelatedField(queryset=models.InstanceState.objects)
    previous_instance_state = FormDataResourceRelatedField(
        queryset=models.InstanceState.objects
    )

    def generate_identifier(self):
        """
        Build identifier for instance.

        Format:
        two last digits of communal location number
        year in two digits
        unique sequence

        Example: 11-18-001
        """
        identifier = self.instance.identifier
        if not identifier:
            location_nr = self.instance.location.communal_federal_number[-2:]
            year = timezone.now().strftime("%y")

            max_identifier = (
                models.Instance.objects.filter(
                    identifier__startswith="{0}-{1}-".format(location_nr, year)
                ).aggregate(max_identifier=Max("identifier"))["max_identifier"]
                or "00-00-000"
            )
            sequence = int(max_identifier[-3:])

            identifier = "{0}-{1}-{2}".format(
                location_nr, timezone.now().strftime("%y"), str(sequence + 1).zfill(3)
            )

        return identifier

    def validate(self, data):
        location = self.instance.location
        if location is None:
            raise exceptions.ValidationError(_("No location assigned."))

        data["identifier"] = self.generate_identifier()
        form_validator = validators.FormDataValidator(self.instance)
        form_validator.validate()

        # find municipality assigned to location of instance
        role_permissions = settings.APPLICATION.get("ROLE_PERMISSIONS", {})
        municipality_roles = [
            role
            for role, permission in role_permissions.items()
            if permission == "municipality"
        ]

        location_group = Group.objects.filter(
            locations=location, role__name__in=municipality_roles
        ).first()

        if location_group is None:
            raise exceptions.ValidationError(
                _("No group found for location %(name)s.") % {"name": location.name}
            )

        data["group"] = location_group

        return data


class FormFieldSerializer(InstanceEditableMixin, serializers.ModelSerializer):

    included_serializers = {"instance": InstanceSerializer}

    def validate_name(self, name):
        # TODO: check whether question is part of used form

        perms = settings.APPLICATION.get("ROLE_PERMISSIONS", {})
        group = self.context["request"].group
        permission = perms.get(group.role.get_name(), "applicant")

        question = settings.FORM_CONFIG["questions"].get(name)
        if question is None:
            raise exceptions.ValidationError(
                _("invalid question %(question)s.") % {"question": name}
            )

        # per default only applicant may edit a question
        restrict = question.get("restrict", ["applicant"])
        if permission not in restrict:
            raise exceptions.ValidationError(
                _("%(permission)s is not allowed to edit question %(question)s.")
                % {"question": name, "permission": permission}
            )

        return name

    class Meta:
        model = models.FormField
        fields = ("name", "value", "instance")


class JournalEntrySerializer(InstanceEditableMixin, serializers.ModelSerializer):
    included_serializers = {
        "instance": InstanceSerializer,
        "user": "camac.user.serializers.UserSerializer",
    }

    def create(self, validated_data):
        validated_data["modification_date"] = timezone.now()
        validated_data["creation_date"] = timezone.now()
        validated_data["user"] = self.context["request"].user
        validated_data["group"] = self.context["request"].group
        validated_data["service"] = self.context["request"].group.service
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["modification_date"] = timezone.now()
        return super().update(instance, validated_data)

    class Meta:
        model = models.JournalEntry
        fields = (
            "instance",
            "group",
            "service",
            "user",
            "duration",
            "text",
            "creation_date",
            "modification_date",
        )
        read_only_fields = (
            "group",
            "service",
            "user",
            "creation_date",
            "modification_date",
        )


class IssueSerializer(InstanceEditableMixin, serializers.ModelSerializer):
    included_serializers = {
        "instance": InstanceSerializer,
        "user": "camac.user.serializers.UserSerializer",
    }

    def create(self, validated_data):
        validated_data["group"] = self.context["request"].group
        validated_data["service"] = self.context["request"].group.service
        return super().create(validated_data)

    class Meta:
        model = models.Issue
        fields = (
            "instance",
            "group",
            "service",
            "user",
            "deadline_date",
            "text",
            "state",
        )
        read_only_fields = ("group", "service")


class IssueTemplateSerializer(serializers.ModelSerializer):
    included_serializers = {"user": "camac.user.serializers.UserSerializer"}

    def create(self, validated_data):
        validated_data["group"] = self.context["request"].group
        validated_data["service"] = self.context["request"].group.service
        return super().create(validated_data)

    class Meta:
        model = models.IssueTemplate
        fields = ("group", "service", "user", "deadline_length", "text")
        read_only_fields = ("group", "service")


class IssueTemplateSetSerializer(serializers.ModelSerializer):
    included_serializers = {"issue_templates": IssueTemplateSerializer}

    def create(self, validated_data):
        validated_data["group"] = self.context["request"].group
        validated_data["service"] = self.context["request"].group.service
        return super().create(validated_data)

    class Meta:
        model = models.IssueTemplateSet
        fields = ("group", "service", "name", "issue_templates")
        read_only_fields = ("group", "service")


class IssueTemplateSetApplySerializer(InstanceEditableMixin, serializers.Serializer):
    instance = relations.ResourceRelatedField(queryset=models.Instance.objects)

    class Meta:
        resource_name = "issue-template-sets-apply"
