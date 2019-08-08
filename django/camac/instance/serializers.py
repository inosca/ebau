import json
from logging import getLogger

import requests
from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from django.db.models import Max
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header
from rest_framework_json_api import relations, serializers

from camac.constants import kt_bern as constants
from camac.core.models import Answer, InstanceLocation, InstanceService
from camac.core.serializers import MultilingualSerializer
from camac.instance.mixins import InstanceEditableMixin
from camac.notification.serializers import NotificationTemplateSendmailSerializer
from camac.user.models import Group
from camac.user.permissions import permission_aware
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
    # TODO once more than one Camac-NG project uses Caluma as a form
    # this serializer needs to be split up into what is actually
    # Caluma and what is project specific
    readable_forms = serializers.SerializerMethodField()
    editable_forms = serializers.SerializerMethodField()

    instance_state = serializers.ResourceRelatedField(
        queryset=models.InstanceState.objects.filter(name="new"),
        default=NewInstanceStateDefault(),
    )

    previous_instance_state = serializers.ResourceRelatedField(
        queryset=models.InstanceState.objects.filter(name="new"),
        default=NewInstanceStateDefault(),
    )

    caluma_form = serializers.CharField(required=True, write_only=True)

    public_status = serializers.SerializerMethodField()

    @permission_aware
    def get_editable_forms(self, instance):
        state = instance.instance_state.name

        if state in ["new", "rejected"]:
            return self._get_caluma_main_forms()

        if state in ["sb1", "sb2"]:
            return [state]

        return []

    def get_editable_forms_for_municipality(self, instance):
        if instance.instance_state.name == "correction":
            return self._get_caluma_main_forms()

        return []

    def get_editable_forms_for_service(self, instance):
        return []

    def get_editable_forms_for_canton(self, instance):
        return []

    @permission_aware
    def get_readable_forms(self, instance):
        state = instance.instance_state.name
        forms = self._get_caluma_main_forms()

        if state == "sb1":
            return forms + ["sb1"]

        if state in ["sb2", "conclusion"]:
            return forms + ["sb1", "sb2"]

        return forms

    def get_readable_forms_for_municipality(self, instance):
        state = instance.instance_state.name
        forms = self._get_caluma_main_forms()

        if state == "sb2":
            return forms + ["sb1"]

        if state == "conclusion":
            return forms + ["sb1", "sb2"]

        return forms

    def get_readable_forms_for_service(self, instance):
        return self.get_readable_forms_for_municipality(instance)

    def get_readable_forms_for_canton(self, instance):
        return self.get_readable_forms_for_municipality(instance)

    def _get_caluma_main_forms(self):
        cache_key = "caluma_main_forms"
        resp = cache.get(cache_key)

        if resp is None:
            raw = self.query_caluma(
                """
                query {
                    allForms(metaValue: [{key: "is-main-form", value: true}]) {
                        edges {
                            node {
                                slug
                            }
                        }
                    }
                }
            """
            )

            resp = [edge["node"]["slug"] for edge in raw["data"]["allForms"]["edges"]]
            cache.set(cache_key, resp, 3600)

        return resp

    def query_caluma(self, query, variables={}):
        # TODO: move this to a more general location

        response = requests.post(
            settings.CALUMA_URL,
            json={"query": query, "variables": variables},
            headers={
                "Authorization": get_authorization_header(self.context["request"])
            },
        )

        response.raise_for_status()
        result = response.json()
        if result.get("errors"):  # pragma: no cover
            raise exceptions.ValidationError(
                f"Error while querying caluma: {result.get('errors')}"
            )

        return result

    def get_public_status(self, instance):
        # TODO Instead of a new field, we should actually modify the values of instance_state
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

    def validate(self, data):
        form = data.get("caluma_form")
        caluma_resp = self.query_caluma(
            """
                query GetMainForm($slug: String!) {
                    allForms(slug: $slug, metaValue: [{key: "is-main-form", value: true}]) {
                        edges {
                            node {
                                slug
                                meta
                            }
                        }
                    }
                }
            """,
            {"slug": form},
        )

        if len(caluma_resp["data"]["allForms"]["edges"]) != 1:  # pragma: no cover
            raise exceptions.ValidationError(
                f"Passed caluma form is not a main form: {form}"
            )

        return data

    def create(self, validated_data):
        form = validated_data.pop("caluma_form")
        created = super().create(validated_data)

        created.involved_applicants.create(
            user=self.context["request"].user,
            invitee=self.context["request"].user,
            created=timezone.now(),
        )

        self.query_caluma(
            """
            mutation CreateDocument($input: SaveDocumentInput!) {
                saveDocument(input: $input) {
                    clientMutationId
                }
            }
            """,
            {
                "input": {
                    "form": form,
                    "meta": json.dumps({"camac-instance-id": created.instance_id}),
                }
            },
        )

        return created

    class Meta(InstanceSerializer.Meta):
        fields = InstanceSerializer.Meta.fields + ("caluma_form", "public_status")
        read_only_fields = InstanceSerializer.Meta.read_only_fields + ("public_status",)
        meta_fields = InstanceSerializer.Meta.meta_fields + (
            "readable_forms",
            "editable_forms",
        )


class CalumaInstanceSubmitSerializer(CalumaInstanceSerializer):
    def _notify_submit(self, template_id, recipient_types):
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

    def _set_submit_date(self, validated_data):
        document = validated_data["caluma_document"]

        if "submit-date" in document["meta"]:  # pragma: no cover
            # instance was already submitted, this is probably a re-submit
            # after correction.
            return

        # Set submit date in Camac first...
        # TODO drop this after this is not used anymore in Camac
        Answer.objects.get_or_create(
            instance=self.instance,
            question_id=SUBMIT_DATE_QUESTION_ID,
            item=1,
            chapter_id=SUBMIT_DATE_CHAPTER,
            # CAMAC date is formatted in "dd.mm.yyyy"
            defaults={"answer": timezone.now().strftime("%d.%m.%Y")},
        )

        new_meta = {
            **document["meta"],
            # Caluma date is formatted yyyy-mm-dd so it can be sorted
            "submit-date": timezone.now().strftime("%Y-%m-%d"),
        }

        self.query_caluma(
            """
                mutation SaveDocumentMeta($input: SaveDocumentInput!) {
                    saveDocument(input: $input) {
                        clientMutationId
                    }
                }
            """,
            {
                "input": {
                    "id": document["id"],
                    "form": document["form"]["slug"],
                    "meta": json.dumps(new_meta),
                }
            },
        )

    def _validate_document_validity(self, document_id):
        # TODO: reenable this when caluma document validity is fixed
        # validity = self.query_caluma(
        #     """
        #         query GetDocumentValidity($id: ID!) {
        #             documentValidity(id: $id) {
        #                 edges {
        #                     node {
        #                         id
        #                         isValid
        #                         errors {
        #                             slug
        #                             errorMsg
        #                         }
        #                     }
        #                 }
        #             }
        #         }
        #     """,
        #     {"id": document_id},
        # )

        # if not validity["edges"]["node"][0]["isValid"]:
        #     errors = ", ".join(map(lambda e: e["errorMsg"], validity["edges"]["node"][0]["errors"]))
        #     raise exceptions.ValidationError(
        #         f"Error while validating caluma document: {errors}"
        #     )

        pass

    def validate(self, data):
        caluma_resp = self.query_caluma(
            """
            query GetDocument($instanceId: GenericScalar!) {
                allDocuments(metaValue: [{key: "camac-instance-id", value: $instanceId}]) {
                    edges {
                        node {
                            id
                            meta
                            form {
                                slug
                                meta
                            }
                            answers(questions: ["gemeinde"]) {
                                edges {
                                    node {
                                        id
                                        question {
                                            slug
                                        }
                                        ...on StringAnswer {
                                            value
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            """,
            {"instanceId": self.instance.pk},
        )

        documents = caluma_resp["data"]["allDocuments"]["edges"]

        data["caluma_document"] = next(
            (
                document["node"]
                for document in documents
                if document["node"]["form"]["meta"].get("is-main-form", False)
            ),
            None,
        )

        if not data["caluma_document"]:  # pragma: no cover
            raise exceptions.ValidationError(
                f"Could not find caluma main document for instance {self.instance.pk}"
            )

        data["caluma_municipality"] = next(
            (
                answer["node"]["value"]
                for answer in data["caluma_document"]["answers"]["edges"]
                if answer["node"]["question"]["slug"] == "gemeinde"
            ),
            None,
        )

        if not data["caluma_municipality"]:  # pragma: no cover
            raise exceptions.ValidationError(
                f"Could not find municipality in caluma document for instance {self.instance.pk}"
            )

        self._validate_document_validity(data["caluma_document"]["id"])

        return data

    @transaction.atomic
    def update(self, instance, validated_data):
        request_logger.info(f"Submitting instance {instance.pk}")

        previous_instance_state = instance.previous_instance_state

        instance.previous_instance_state = instance.instance_state
        instance.instance_state = (
            models.InstanceState.objects.get(name="subm")
            if instance.instance_state.name == "new"
            # BE: If a rejected instancere is resubmitted, the process continues where it left off
            else previous_instance_state
        )

        instance.save()

        InstanceService.objects.get_or_create(
            instance=self.instance,
            service_id=int(validated_data.get("caluma_municipality")),
            active=1,
            defaults={"activation_date": None},
        )

        self._set_submit_date(validated_data)

        # send out emails upon submission
        for notification_config in settings.APPLICATION["NOTIFICATIONS"]["SUBMIT"]:
            self._notify_submit(**notification_config)

        return instance


class CalumaInstanceReportSerializer(CalumaInstanceSubmitSerializer):
    """Handle submission of "SB1" form."""

    def validate(self, data):
        caluma_resp = self.query_caluma(
            """
            query GetDocument($instanceId: GenericScalar!) {
                allDocuments(
                    metaValue: [{key: "camac-instance-id", value: $instanceId}]
                    form: "sb1"
                ) {
                    edges {
                        node {
                            id
                            meta
                            form {
                                slug
                                meta
                            }
                        }
                    }
                }
            }
            """,
            {"instanceId": self.instance.pk},
        )

        data["caluma_document"] = next(
            (
                document["node"]
                for document in caluma_resp["data"]["allDocuments"]["edges"]
                if document["node"]["form"]["slug"] == "sb1"
            ),
            None,
        )

        if not data["caluma_document"]:  # pragma: no cover
            raise exceptions.ValidationError(
                f"Could not find caluma `sb1` document for instance {self.instance.pk}"
            )

        self._validate_document_validity(data["caluma_document"]["id"])

        return data

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.previous_instance_state = instance.instance_state
        instance.instance_state = models.InstanceState.objects.get(name="sb2")

        instance.save()

        # send out emails upon submission
        for notification_config in settings.APPLICATION["NOTIFICATIONS"]["REPORT"]:
            self._notify_submit(**notification_config)

        return instance


class CalumaInstanceFinalizeSerializer(CalumaInstanceSubmitSerializer):
    """Handle submission of "SB2" form."""

    def validate(self, data):
        caluma_resp = self.query_caluma(
            """
            query GetDocument($instanceId: GenericScalar!) {
                allDocuments(
                    metaValue: [{key: "camac-instance-id", value: $instanceId}]
                    form: "sb2"
                ) {
                    edges {
                        node {
                            id
                            meta
                            form {
                                slug
                                meta
                            }
                        }
                    }
                }
            }
            """,
            {"instanceId": self.instance.pk},
        )

        data["caluma_document"] = next(
            (
                document["node"]
                for document in caluma_resp["data"]["allDocuments"]["edges"]
                if document["node"]["form"]["slug"] == "sb2"
            ),
            None,
        )

        if not data["caluma_document"]:  # pragma: no cover
            raise exceptions.ValidationError(
                f"Could not find caluma `sb2` document for instance {self.instance.pk}"
            )

        self._validate_document_validity(data["caluma_document"]["id"])

        return data

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.previous_instance_state = instance.instance_state
        instance.instance_state = models.InstanceState.objects.get(name="conclusion")

        instance.save()

        # send out emails upon submission
        for notification_config in settings.APPLICATION["NOTIFICATIONS"]["FINALIZE"]:
            self._notify_submit(**notification_config)

        return instance


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
