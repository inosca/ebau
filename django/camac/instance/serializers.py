import itertools
import json
import re
from collections import namedtuple
from io import StringIO
from logging import getLogger

from alexandria.core import models as alexandria_models
from alexandria.core.storage_clients import Minio
from caluma.caluma_form import models as form_models
from caluma.caluma_form.validators import CustomValidationError, DocumentValidator
from caluma.caluma_workflow import api as workflow_api, models as workflow_models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext as _, gettext_noop
from rest_framework import exceptions
from rest_framework_json_api import relations, serializers

from camac.caluma.api import CalumaApi
from camac.constants import kt_uri as uri_constants
from camac.core.models import (
    Answer,
    AuthorityLocation,
    HistoryActionConfig,
    InstanceLocation,
    InstanceService,
    WorkflowEntry,
)
from camac.core.serializers import MultilingualField, MultilingualSerializer
from camac.core.utils import create_history_entry, generate_ebau_nr, generate_sort_key
from camac.document.models import AttachmentSection
from camac.ech0211.signals import (
    change_responsibility,
    instance_submitted,
    sb1_submitted,
    sb2_submitted,
)
from camac.instance.domain_logic import link_instances
from camac.instance.master_data import MasterData
from camac.instance.mixins import InstanceEditableMixin, InstanceQuerysetMixin
from camac.instance.utils import copy_instance, fill_ebau_number
from camac.notification.utils import send_mail, send_mail_without_request
from camac.permissions import api as permissions_api
from camac.responsible.models import ResponsibleService
from camac.responsible.serializers import reassign_work_items
from camac.tags.models import Keyword
from camac.user.models import Group, Location, Service
from camac.user.permissions import permission_aware
from camac.user.relations import (
    CurrentUserResourceRelatedField,
    FormDataResourceRelatedField,
    GroupResourceRelatedField,
    ServiceResourceRelatedField,
)
from camac.user.serializers import CurrentGroupDefault, CurrentServiceDefault

from ..utils import clean_join, get_paper_settings
from . import document_merge_service, domain_logic, models, validators

SUBMIT_DATE_CHAPTER = 100001
SUBMIT_DATE_QUESTION_ID = 20036
SUBMIT_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
COMPLETE_PRELIMINARY_CLARIFICATION_SLUGS_BE = [
    "vorabklaerung-vollstaendig",
    "vorabklaerung-vollstaendig-v2",
]

request_logger = getLogger("django.request")

caluma_api = CalumaApi()


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
    # TODO once more than one Camac-NG project uses Caluma as a form
    # this serializer needs to be split up into what is actually
    # Caluma and what is project specific
    permissions = serializers.SerializerMethodField()

    editable = serializers.SerializerMethodField()
    access_type = serializers.SerializerMethodField()
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

    keywords = serializers.ResourceRelatedField(
        queryset=Keyword.objects, required=False, many=True
    )

    involved_services = relations.SerializerMethodResourceRelatedField(
        source="get_involved_services", model=Service, read_only=True, many=True
    )

    linked_instances = relations.SerializerMethodResourceRelatedField(
        source="get_linked_instances", model=models.Instance, read_only=True, many=True
    )

    circulation_initializer_services = relations.SerializerMethodResourceRelatedField(
        source="get_circulation_initializer_services",
        model=Service,
        read_only=True,
        many=True,
    )

    active_service = relations.SerializerMethodResourceRelatedField(
        source="get_active_service", model=Service, read_only=True
    )

    def get_permissions(self, instance):
        return {}

    @permission_aware
    def get_access_type(self, obj):
        access_type = None

        if obj.involved_applicants.filter(
            invitee=self.context["request"].user
        ).exists():
            access_type = "applicant"

        return access_type

    def get_access_type_for_public_reader(self, obj):
        return "public"

    def get_access_type_for_municipality(self, obj):
        return "municipality"

    def get_access_type_for_service(self, obj):
        return "service"

    def get_linked_instances(self, obj):
        queryset = self.context["view"].get_queryset()
        if not obj.instance_group or queryset.model is not models.Instance:
            return models.Instance.objects.none()

        return queryset.filter(instance_group=obj.instance_group).exclude(pk=obj.pk)

    def get_circulation_initializer_services(self, obj):
        return Service.objects.filter(
            pk__in=obj.circulations.filter(
                activations__service=self.context["request"].group.service_id
            ).values("service")
        )

    def get_involved_services(self, obj):
        # TODO: Involved services should be extended to allow manual
        # work-items to be assigned to services involved through the
        # permissions module
        if not settings.DISTRIBUTION:
            return Service.objects.none()

        filters = Q(
            pk__in=list(
                itertools.chain(
                    *workflow_models.WorkItem.objects.filter(
                        task_id=settings.DISTRIBUTION["INQUIRY_TASK"],
                        case__family=obj.case,
                    )
                    .exclude(
                        status__in=[
                            workflow_models.WorkItem.STATUS_CANCELED,
                            workflow_models.WorkItem.STATUS_SUSPENDED,
                        ]
                    )
                    .values_list("addressed_groups", flat=True)
                )
            )
        )

        # If permission module has ACLs for some services, they are
        # considered as "involved" as well
        filters |= Q(
            pk__in=permissions_api.PermissionManager.from_request(
                self.context["request"]
            ).involved_services(obj)
        )

        if settings.APPLICATION.get("USE_INSTANCE_SERVICE"):
            filters |= Q(pk__in=obj.services.values("pk"))
        elif obj.group and obj.group.service:
            filters |= Q(pk=obj.group.service.pk)

        return Service.objects.filter(filters).distinct()

    def get_active_service(self, instance):
        return instance.responsible_service(filter_type="municipality")

    included_serializers = {
        "location": "camac.user.serializers.LocationSerializer",
        "user": "camac.user.serializers.UserSerializer",
        "group": "camac.user.serializers.GroupSerializer",
        "form": FormSerializer,
        "instance_state": InstanceStateSerializer,
        "previous_instance_state": InstanceStateSerializer,
        "circulations": "camac.circulation.serializers.CirculationSerializer",
        "services": "camac.user.serializers.ServiceSerializer",
        "involved_services": "camac.user.serializers.ServiceSerializer",
        "linked_instances": "camac.instance.serializers.InstanceSerializer",
        "circulation_initializer_services": "camac.user.serializers.ServiceSerializer",
        "active_service": "camac.user.serializers.PublicServiceSerializer",
        "keywords": "camac.tags.serializers.KeywordSerializer",
    }

    @transaction.atomic
    def create(self, validated_data):
        instance = super().create(validated_data)

        instance.involved_applicants.create(
            user=self.context["request"].user,
            invitee=self.context["request"].user,
            created=timezone.now(),
            email=self.context["request"].user.email,
        )

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
        meta_fields = ("editable", "access_type", "permissions")
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
            "services",
            "involved_services",
            "linked_instances",
            "circulation_initializer_services",
            "active_service",
            "keywords",
        )
        read_only_fields = (
            "circulations",
            "creation_date",
            "identifier",
            "modification_date",
            "services",
            "involved_services",
            "linked_instances",
            "circulation_initializer_services",
            "active_service",
        )


class SchwyzInstanceSerializer(InstanceSerializer):
    caluma_form = serializers.SerializerMethodField()
    caluma_workflow = serializers.SerializerMethodField()

    @permission_aware
    def validate(self, data):
        return data

    def _validate_internal(self, data):
        if settings.APPLICATION["CALUMA"].get("CREATE_IN_PROCESS"):
            data["instance_state"] = models.InstanceState.objects.get(name="internal")
        return data

    def validate_for_municipality(self, data):
        return self._validate_internal(data)

    def validate_for_service(self, data):
        return self._validate_internal(data)

    def validate_for_canton(self, data):
        return self._validate_internal(data)

    @transaction.atomic
    def create(self, validated_data):
        instance = super().create(validated_data)

        caluma_form = self.initial_data.get("caluma_form", "baugesuch")
        caluma_workflow = self.initial_data.get("caluma_workflow", "building-permit")

        case = workflow_api.start_case(
            workflow=workflow_models.Workflow.objects.get(pk=caluma_workflow),
            form=form_models.Form.objects.get(pk=caluma_form),
            user=self.context["request"].caluma_info.context.user,
            meta={"camac-instance-id": instance.pk},
            # necessary for resolving dynamic groups
            context={"instance": instance.pk},
        )

        instance.case = case

        # Creation logic for caluma based forms
        if caluma_workflow != "building-permit":
            identifier = domain_logic.CreateInstanceLogic.generate_identifier(instance)
            instance.case.meta["dossier-number"] = identifier
            instance.case.meta["dossier-number-sort"] = generate_sort_key(identifier)
            instance.case.meta["form-backend"] = "caluma"
            instance.case.save()
            instance.identifier = identifier

        instance.save()
        return instance

    @permission_aware
    def get_permissions(self, instance):
        return {}

    def get_permissions_for_municipality(self, instance):
        if instance.instance_state.name in ["new", "subm", "arch"]:
            return {"bauverwaltung": {"read"}, "main": {"read"}}
        elif instance.instance_state.name in ["comm", "circ", "nfd"]:
            return {
                "bauverwaltung": {"read", "write"},
                "main": {"read", "write"},
                "inquiry": {"read", "write"},
                "inquiry-answer": {"read", "write"},
            }
        else:
            return {"bauverwaltung": {"read", "write"}, "main": {"read", "write"}}

    def get_permissions_for_service(self, instance):
        if instance.instance_state.name in ["internal"]:
            return {"bauverwaltung": {"read"}, "main": {"read", "write"}}

        elif instance.instance_state.name in ["circ", "nfd"]:
            return {
                "bauverwaltung": {"read", "write"},
                "main": {"read", "write"},
                "inquiry": {"read", "write"},
                "inquiry-answer": {"read", "write"},
            }

        return {"bauverwaltung": {"read"}}

    def get_permissions_for_support(self, instance):
        return {"bauverwaltung": {"read", "write"}, "main": {"read", "write"}}

    def get_caluma_form(self, instance):
        return CalumaApi().get_form_slug(instance)

    def get_caluma_workflow(self, instance):
        return CalumaApi().get_workflow_slug(instance)

    class Meta(InstanceSerializer.Meta):
        fields = InstanceSerializer.Meta.fields + ("caluma_form", "caluma_workflow")
        read_only_fields = InstanceSerializer.Meta.read_only_fields + (
            "caluma_form",
            "caluma-workflow",
        )
        meta_fields = InstanceSerializer.Meta.meta_fields


class CamacInstanceChangeFormSerializer(serializers.Serializer):
    """Handle changing the form of an instance."""

    form = serializers.CharField()

    def validate_form(self, value):
        if value not in settings.APPLICATION.get("INTERCHANGEABLE_FORMS", []):
            raise exceptions.ValidationError(
                _("'%(form)s' is not a valid form type") % {"form": value}
            )

        return value

    def validate(self, data):
        if self.instance.form.name not in settings.APPLICATION.get(
            "INTERCHANGEABLE_FORMS", []
        ):
            raise exceptions.ValidationError(
                _("The current form '%(form)s' can't be changed")
                % {"form": self.instance.form.name}
            )
        elif self.instance.form.name == data["form"]:
            raise exceptions.ValidationError(
                _("Form is already of type '%(form)s'") % {"form": data["form"]}
            )

        return data

    @transaction.atomic
    def update(self, instance, validated_data):
        previous_form = instance.form
        instance.form = models.Form.objects.get(name=validated_data["form"])

        instance.save()

        meta, _ = models.FormField.objects.get_or_create(
            instance=instance, name="meta", defaults={"value": json.dumps({})}
        )
        meta_value = json.loads(meta.value)
        meta_value["formChange"] = {"name": previous_form.name, "id": previous_form.pk}
        meta.value = json.dumps(meta_value)
        meta.save()

        work_item = instance.case.work_items.get(
            task_id=settings.APPLICATION["CALUMA"]["REJECTION_TASK"],
            status=workflow_models.WorkItem.STATUS_READY,
        )

        workflow_api.complete_work_item(
            work_item=work_item,
            user=self.context["request"].caluma_info.context.user,
            context={
                "notification-body": f'Die Leitbehörde hat ihr Gesuch von "{previous_form.description}" zu "{instance.form.description}" umgewandelt, da der vorherige Gesuchstyp inkorrekt war. Ergänzen Sie bitte die fehlenden Angaben und reichen das Gesuch nochmals ein. - Besten Dank für Ihr Verständnis.'
            },
        )

        create_history_entry(
            instance,
            self.context["request"].user,
            f'Dossier wurde von "{previous_form.description}" zu "{instance.form.description}" umgewandelt',
        )

        return instance

    class Meta:
        resource_name = "instance-change-forms"


class CalumaInstanceSerializer(InstanceSerializer, InstanceQuerysetMixin):
    instance_state = serializers.ResourceRelatedField(
        queryset=models.InstanceState.objects.filter(name="new"),
        default=NewInstanceStateDefault(),
    )

    previous_instance_state = serializers.ResourceRelatedField(
        queryset=models.InstanceState.objects.filter(name="new"),
        default=NewInstanceStateDefault(),
    )

    form = serializers.ResourceRelatedField(
        queryset=models.Form.objects.all(), default=lambda: models.Form.objects.first()
    )

    caluma_form = serializers.SerializerMethodField()
    dossier_number = serializers.SerializerMethodField()
    ebau_number = serializers.SerializerMethodField()

    is_paper = serializers.SerializerMethodField()  # "Papierdossier
    is_modification = serializers.SerializerMethodField()  # "Projektänderung"
    copy_source = serializers.CharField(required=False, write_only=True)
    extend_validity_for = serializers.IntegerField(required=False, write_only=True)
    generate_identifier = serializers.BooleanField(required=False, write_only=True)
    year = serializers.IntegerField(required=False, write_only=True)

    public_status = serializers.SerializerMethodField()

    responsible_service_users = relations.SerializerMethodResourceRelatedField(
        source="get_responsible_service_users",
        model=get_user_model(),
        many=True,
        read_only=True,
    )
    name = serializers.SerializerMethodField()
    decision_date = serializers.SerializerMethodField()
    decision = serializers.SerializerMethodField()
    involved_at = serializers.SerializerMethodField()
    is_after_decision = serializers.SerializerMethodField()

    def get_is_paper(self, instance):
        return CalumaApi().is_paper(instance)

    def get_is_modification(self, instance):
        return CalumaApi().is_modification(instance)

    def get_caluma_form(self, instance):
        return CalumaApi().get_form_slug(instance)

    def get_dossier_number(self, instance):
        return CalumaApi().get_dossier_number(instance)

    def get_ebau_number(self, instance):
        return instance.case.meta.get("ebau-number")

    def get_decision(self, instance):
        if not settings.DECISION:  # pragma: no cover
            return None

        answer = (
            form_models.Answer.objects.filter(
                question_id=settings.DECISION["QUESTIONS"]["DECISION"],
                document__work_item__task_id=settings.DECISION["TASK"],
                document__work_item__status__in=[
                    workflow_models.WorkItem.STATUS_COMPLETED,
                    workflow_models.WorkItem.STATUS_SKIPPED,
                ],
                document__work_item__case__family__instance=instance,
            )
            .order_by("-document__work_item__closed_at")
            .first()
        )

        if not answer or not answer.selected_options:
            return None

        return str(answer.selected_options[0].label)

    def get_decision_date(self, instance):
        if not settings.DECISION:  # pragma: no cover
            return None

        return (
            form_models.Answer.objects.filter(
                question_id=settings.DECISION["QUESTIONS"]["DATE"],
                document__work_item__task_id=settings.DECISION["TASK"],
                document__work_item__status__in=[
                    workflow_models.WorkItem.STATUS_COMPLETED,
                    workflow_models.WorkItem.STATUS_SKIPPED,
                ],
                document__work_item__case__family__instance=instance,
            )
            .order_by("-document__work_item__closed_at")
            .values_list("date", flat=True)
            .first()
        )

    def get_involved_at(self, instance):
        service_id = self.context["request"].group.service_id

        if not settings.DISTRIBUTION or not service_id:
            return None

        return (
            workflow_models.WorkItem.objects.filter(
                case__family__instance=instance,
                task_id=settings.DISTRIBUTION["INQUIRY_TASK"],
                status__in=[
                    workflow_models.WorkItem.STATUS_READY,
                    workflow_models.WorkItem.STATUS_COMPLETED,
                    workflow_models.WorkItem.STATUS_SKIPPED,
                ],
                addressed_groups=[str(service_id)],
            )
            .order_by("child_case__created_at")
            .values_list("child_case__created_at", flat=True)
            .first()
        )

    def get_responsible_service_users(self, instance):
        return get_user_model().objects.filter(
            pk__in=instance.responsible_services.filter(
                service=self.context["request"].group.service
            ).values("responsible_user")
        )

    def get_public_status(self, instance):
        config = settings.APPLICATION["CALUMA"].get("PUBLIC_STATUS")
        if not config:
            return instance.instance_state.name

        identifier = (
            instance.instance_state.name
            if config.get("USE_SLUGS", False)
            else instance.instance_state_id
        )

        return config.get("MAP", {}).get(identifier, config.get("DEFAULT", ""))

    def get_is_after_decision(self, instance):
        return instance.instance_state.name in settings.APPLICATION.get(
            "ATTACHMENT_AFTER_DECISION_STATES", []
        )

    included_serializers = {
        **InstanceSerializer.included_serializers,
        "responsible_service_users": "camac.user.serializers.UserSerializer",
        "involved_applicants": "camac.applicants.serializers.ApplicantSerializer",
        "linked_instances": "camac.instance.serializers.CalumaInstanceSerializer",
    }

    def _is_read_only(self):
        group = self.context["request"].group

        return group.role.name.endswith("-readonly") if group else False

    @permission_aware
    def _get_main_form_permissions(self, instance):
        permissions = set(["read"])

        if instance.instance_state.name == "new":
            permissions.add("write")

        return permissions

    def _get_main_form_permissions_for_coordination(self, instance):
        return set(["read", "write"])

    def _get_main_form_permissions_for_service(self, instance):
        if instance.instance_state.name == "new":
            return set()

        return set(["read"])

    def _get_main_form_permissions_for_municipality(self, instance):
        state = instance.instance_state.name
        is_paper = CalumaApi().is_paper(instance)
        service_group = self.context["request"].group.service.service_group.pk
        role = self.context["request"].group.role.pk
        permissions = set()

        if state != "new":
            permissions.add("read")

        if (
            state
            in settings.APPLICATION.get("INSTANCE_PERMISSIONS", {}).get(
                "MUNICIPALITY_WRITE", []
            )
            and not self._is_read_only()
        ):
            permissions.add("write")

        if (
            is_paper
            and service_group in get_paper_settings()["ALLOWED_SERVICE_GROUPS"]
            and role in get_paper_settings()["ALLOWED_ROLES"]
            and state == "new"
        ):
            permissions.update(["read", "write"])

        return permissions

    def _get_main_form_permissions_for_support(self, instance):
        return set(["read", "write"])

    @permission_aware
    def _get_sb1_form_permissions(self, instance):
        state = instance.instance_state.name
        permissions = set()

        if state in ["sb1", "sb2", "conclusion"]:
            permissions.add("read")

        if state == "sb1":
            permissions.add("write")

        return permissions

    def _get_sb1_form_permissions_for_service(self, instance):
        if instance.instance_state.name in ["sb2", "conclusion"]:
            return set(["read"])

        return set()

    def _get_sb1_form_permissions_for_municipality(self, instance):
        state = instance.instance_state.name
        is_paper = CalumaApi().is_paper(instance)
        service_group = self.context["request"].group.service.service_group
        role = self.context["request"].group.role

        permissions = set()

        if state in ["sb1", "sb2", "conclusion"]:
            permissions.add("read")

        if (
            state == "sb1"
            and is_paper
            and service_group.pk in get_paper_settings("sb1")["ALLOWED_SERVICE_GROUPS"]
            and role.pk in get_paper_settings("sb1")["ALLOWED_ROLES"]
        ):
            permissions.add("write")

        return permissions

    def _get_sb1_form_permissions_for_support(self, instance):
        return ["read", "write"]

    @permission_aware
    def _get_sb2_form_permissions(self, instance):
        state = instance.instance_state.name
        permissions = set()

        if state in ["sb2", "conclusion"]:
            permissions.add("read")

        if state == "sb2":
            permissions.add("write")

        return permissions

    def _get_sb2_form_permissions_for_service(self, instance):
        if instance.instance_state.name == "conclusion":
            return set(["read"])

        return set()

    def _get_sb2_form_permissions_for_municipality(self, instance):
        state = instance.instance_state.name
        is_paper = CalumaApi().is_paper(instance)
        service_group = self.context["request"].group.service.service_group
        role = self.context["request"].group.role.pk

        permissions = set()

        if state in ["sb2", "conclusion"]:
            permissions.add("read")

        if (
            state == "sb2"
            and is_paper
            and service_group.pk in get_paper_settings("sb2")["ALLOWED_SERVICE_GROUPS"]
            and role in get_paper_settings("sb2")["ALLOWED_ROLES"]
        ):
            permissions.update(["read", "write"])

        return permissions

    def _get_sb2_form_permissions_for_support(self, instance):
        return ["read", "write"]

    @permission_aware
    def _get_nfd_form_permissions(self, instance):
        return CalumaApi().get_nfd_form_permissions(instance)

    def _get_nfd_form_permissions_for_service(self, instance):
        return set()

    def _get_nfd_form_permissions_for_municipality(self, instance):
        permissions = set(["read"])

        if (
            instance.instance_state.name
            in [
                "subm",
                "circulation_init",
                "circulation",
                "coordination",
                "in_progress_internal",
            ]
            and not self._is_read_only()
        ):
            permissions.add("write")

        return permissions

    def _get_nfd_form_permissions_for_support(self, instance):
        return set(["read", "write"])

    @permission_aware
    def _get_dossierpruefung_form_permissions(self, instance):
        return set()

    def _get_dossierpruefung_form_permissions_for_service(self, instance):
        if instance.instance_state.name in ["new", "subm", "correction"]:
            return set()

        return set(["read"])

    def _get_dossierpruefung_form_permissions_for_municipality(self, instance):
        permissions = set(["read"])

        if (
            instance.instance_state.name
            in [
                "circulation_init",
                "circulation",
                "coordination",
                "in_progress_internal",
            ]
            and not self._is_read_only()
        ):
            permissions.add("write")

        return permissions

    def _get_dossierpruefung_form_permissions_for_support(self, instance):
        return set(["read", "write"])

    @permission_aware
    def _get_ebau_number_form_permissions(self, instance):
        return set()

    def _get_ebau_number_form_permissions_for_municipality(self, instance):
        if instance.instance_state.name in ["subm", "in_progress_internal"]:
            return set(["read", "write"])

        return set(["read"])

    @permission_aware
    def _get_decision_form_permissions(self, instance):
        return set()

    def _get_decision_form_permissions_for_municipality(self, instance):
        if (
            instance.instance_state.name
            in ["coordination", "in_progress", "in_progress_internal"]
            and not self._is_read_only()
        ):
            return set(["read", "write"])

        return set(["read"])

    @permission_aware
    def _get_publikation_form_permissions(self, instance):
        return set()

    def _get_publikation_form_permissions_for_service(self, instance):
        if instance.instance_state.name in ["new", "subm", "correction"]:
            return set()

        return set(["read"])

    def _get_publikation_form_permissions_for_municipality(self, instance):
        permissions = set()

        if instance.instance_state.name not in ["new", "subm", "correction"]:
            permissions.add("read")

        if (
            "read" in permissions
            and instance.instance_state.name
            not in ["evaluated", "finished", "finished_internal"]
            and not self._is_read_only()
        ):
            permissions.add("write")

        return permissions

    def _get_publikation_form_permissions_for_support(self, instance):
        return set(["read", "write"])

    def _get_information_of_neighbors_form_permissions(self, instance):
        return self._get_publikation_form_permissions(instance)

    @permission_aware
    def _get_case_meta_permissions(self, instance):
        return set(["read"])

    def _get_case_meta_permissions_for_service(self, instance):
        return set(["read"])

    def _get_case_meta_permissions_for_municipality(self, instance):
        permissions = set(["read"])

        if instance.instance_state.name != "new" and not self._is_read_only():
            permissions.add("write")

        return permissions

    def _get_case_meta_permissions_for_support(self, instance):
        return set(["read", "write"])

    @permission_aware
    def _get_inquiry_form_permissions(self, instance):
        return set(["read", "write"])

    @permission_aware
    def _get_inquiry_answer_form_permissions(self, instance):
        return set(["read", "write"])

    @permission_aware
    def _get_geometer_form_permissions(self, instance):
        return set()

    def _get_geometer_form_permissions_for_geometer(self, instance):
        # TODO: Are the form permissions too lenient?
        return set(["read", "write"])

    def get_permissions(self, instance):
        return {
            "case-meta": self._get_case_meta_permissions(instance),
            **{
                form: sorted(
                    getattr(self, f"_get_{form.replace('-','_')}_form_permissions")(
                        instance
                    )
                )
                for form in settings.APPLICATION.get("CALUMA", {}).get(
                    "FORM_PERMISSIONS", set()
                )
            },
        }

    def get_name(self, instance):
        api = CalumaApi()
        name = api.get_form_name(instance)
        parts = []

        migrated = api.is_migrated(instance)  # from RSTA migration
        imported = api.is_imported(instance)  # from dossier import
        paper = api.is_paper(instance)
        modification = api.is_modification(instance)
        is_kog = instance.instance_services.filter(
            service__service_group__name="lead-service", active=1
        )

        if migrated:
            name = api.get_migration_type(instance)[1]
            parts.append(_("migrated"))

        if imported:
            _type = api.get_import_type(instance)
            if _type:
                name = _type
                parts.append(_("migrated"))

        if not migrated and paper:
            parts.append(_("paper"))

        if not migrated and modification:
            parts.append(_("modification"))

        if not migrated and is_kog:
            parts.append(_("coordinated"))

        if not migrated and instance.case.meta.get("is-appeal"):
            parts.append(_("appeal"))

        parts = [f"({part})" for part in parts]

        return " ".join([str(name), *parts])

    @permission_aware
    def validate(self, data):
        if settings.APPLICATION_NAME == "kt_uri":
            request = self.context.get("request")
            if (
                request.data
                and "caluma_form" in request.data
                and "camac-form-id"
                not in form_models.Form.objects.get(
                    slug=request.data["caluma_form"]
                ).meta
            ):
                raise exceptions.ValidationError(
                    _(
                        "There is no camac form mapped on the caluma form '%(caluma_form)s'!"
                        % {"caluma_form": request.data["caluma_form"]}
                    )
                )

        return domain_logic.CreateInstanceLogic.validate(
            data, group=self.context.get("request").group
        )

    instance_field = None

    def get_base_queryset(self):
        """Overridden from InstanceQuerysetMixin to avoid the super().get_queryset() call."""
        instance_state_expr = self._get_instance_filter_expr("instance_state")
        return models.Instance.objects.all().select_related(instance_state_expr)

    def create(self, validated_data):
        group = self.context.get("request").group
        visible_instances = super().get_queryset(group)

        copy_source = validated_data.pop("copy_source", None)
        is_modification = self.initial_data.get("is_modification", False)

        source_instance = None
        if copy_source:
            try:
                source_instance = visible_instances.get(pk=copy_source)
            except models.Instance.DoesNotExist:
                raise exceptions.ValidationError(_("Source instance not found"))

            caluma_form = caluma_api.get_form_slug(source_instance)
            if (
                caluma_form in COMPLETE_PRELIMINARY_CLARIFICATION_SLUGS_BE
                and self.initial_data.get("caluma_form")
            ):
                # Conversion from preliminary clarification to building permit
                caluma_form = self.initial_data.get("caluma_form")

            is_paper = caluma_api.is_paper(source_instance)

            # If the source instance is a project modification, the new
            # instance must be one as well
            is_modification = is_modification or caluma_api.is_modification(
                source_instance
            )

            # when making copies, the form ID remains the same
            validated_data["form"] = source_instance.form
        else:
            is_modification = False
            caluma_form = self.initial_data.get("caluma_form", None)
            is_paper = (
                group.service  # group needs to have a service
                and group.service.service_group.pk
                in get_paper_settings()["ALLOWED_SERVICE_GROUPS"]
                and group.role.pk in get_paper_settings()["ALLOWED_ROLES"]
            )

        if (
            caluma_form in settings.APPLICATION["CALUMA"].get("INTERNAL_FORMS", [])
            and not is_paper
        ):
            raise exceptions.ValidationError(
                _(
                    "The form '%(form)s' can only be used by an internal role"
                    % {"form": caluma_form}
                )
            )

        if is_modification and (
            caluma_form
            not in settings.APPLICATION["CALUMA"].get("MODIFICATION_ALLOW_FORMS", [])
            or source_instance.instance_state.name
            in settings.APPLICATION["CALUMA"].get("MODIFICATION_DISALLOW_STATES", [])
        ):
            raise exceptions.ValidationError(_("Project modification is not allowed"))

        return domain_logic.CreateInstanceLogic.create(
            validated_data,
            caluma_user=self.context["request"].caluma_info.context.user,
            camac_user=self.context["request"].user,
            group=group,
            lead=self.initial_data.get("lead", None),
            is_modification=is_modification,
            is_paper=is_paper,
            caluma_form=caluma_form,
            source_instance=source_instance,
        )

    class Meta(InstanceSerializer.Meta):
        fields = InstanceSerializer.Meta.fields + (
            "caluma_form",
            "is_paper",
            "is_modification",
            "copy_source",
            "extend_validity_for",
            "year",
            "public_status",
            "responsible_service_users",
            "involved_applicants",
            "rejection_feedback",
            "name",
            "generate_identifier",
            "dossier_number",
            "ebau_number",
            "decision",
            "decision_date",
            "involved_at",
            "is_after_decision",
        )
        read_only_fields = InstanceSerializer.Meta.read_only_fields + (
            "caluma_form",
            "is_paper",
            "is_modification",
            "public_status",
            "responsible_service_users",
            "involved_applicants",
            "rejection_feedback",
            "name",
            "dossier_number",
            "ebau_number",
            "decision",
            "decision_date",
            "involved_at",
            "is_after_decision",
        )


class CalumaInstanceSubmitSerializer(CalumaInstanceSerializer):
    _master_data_cache = {}

    def get_master_data(self, case):
        if case.pk not in self._master_data_cache:
            self._master_data_cache[case.pk] = MasterData(case)

        return self._master_data_cache[case.pk]

    def _create_history_entry(self, text):
        create_history_entry(self.instance, self.context["request"].user, text)

    def _send_notification(self, template_slug, recipient_types):
        """Send notification email."""
        send_mail(
            template_slug,
            self.context,
            recipient_types=recipient_types,
            instance={"type": "instances", "id": self.instance.pk},
        )

    def _set_submit_date(self, case, instance):
        if "submit-date" in case.meta:  # pragma: no cover
            # instance was already submitted, this is probably a re-submit
            # after correction.
            return

        submit_date = timezone.now().strftime(SUBMIT_DATE_FORMAT)

        case.meta = {
            **case.meta,
            # Caluma date is formatted yyyy-mm-dd so it can be sorted
            "submit-date": submit_date,
        }
        case.save()

        if settings.APPLICATION.get("SET_SUBMIT_DATE_CAMAC_ANSWER"):
            # Set submit date in Camac first...
            # TODO drop this after this is not used anymore in Camac
            Answer.objects.get_or_create(
                instance=instance,
                question_id=SUBMIT_DATE_QUESTION_ID,
                item=1,
                chapter_id=SUBMIT_DATE_CHAPTER,
                # CAMAC date is formatted in "dd.mm.yyyy"
                defaults={"answer": submit_date},
            )
        elif settings.APPLICATION.get("SET_SUBMIT_DATE_CAMAC_WORKFLOW"):
            WorkflowEntry.objects.create(
                workflow_date=submit_date,
                instance=instance,
                workflow_item_id=uri_constants.WORKFLOW_ITEM_DOSSIER_ERFASST,
                group=1,
            )

    def _get_pdf_section(self, instance, form_slug):
        form_name = form_slug.upper() if form_slug else "MAIN"
        section_type = "PAPER" if CalumaApi().is_paper(instance) else "DEFAULT"
        return settings.APPLICATION["STORE_PDF"]["SECTION"][form_name][section_type]

    def _generate_and_store_pdf(self, instance, form_slug=None):
        if not settings.APPLICATION.get("STORE_PDF", False):  # pragma: no cover
            return

        request = self.context["request"]

        pdf = document_merge_service.DMSHandler().generate_pdf(
            instance.pk, request, form_slug
        )

        target_lookup = self._get_pdf_section(instance, form_slug)
        if settings.APPLICATION["DOCUMENT_BACKEND"] == "alexandria":
            document = alexandria_models.Document.objects.create(
                title=pdf.name,
                category=alexandria_models.Category.objects.get(pk=target_lookup),
                metainfo={
                    "camac-instance-id": str(instance.pk),
                    "system-generated": True,
                },
            )
            file = alexandria_models.File.objects.create(
                name=pdf.name, document=document
            )
            minio = Minio()
            minio.client.put_object(
                minio.bucket, f"{file.pk}_{pdf.name}", pdf, pdf.size
            )
            file.upload_status = alexandria_models.File.COMPLETED
            file.save()
        else:
            attachment_section = AttachmentSection.objects.get(pk=target_lookup)
            attachment_section.attachments.create(
                instance=instance,
                path=pdf,
                name=pdf.name,
                size=pdf.size,
                mime_type=pdf.content_type,
                user=request.user,
                group=request.group,
                question="dokument-weitere-gesuchsunterlagen",
            )

    def _update_rejected_instance(self, instance):
        caluma_api = CalumaApi()

        source_case = caluma_api.get_source_document_value(
            caluma_api.get_main_document(instance), "case"
        )
        source_instance = source_case.instance if source_case else None

        if (
            settings.REJECTION
            and source_instance
            and source_instance.instance_state.name
            == settings.REJECTION["INSTANCE_STATE"]
            and not caluma_api.is_modification(instance)
        ):
            if settings.REJECTION["INSTANCE_STATE_REJECTION_COMPLETE"]:
                source_instance.set_instance_state(
                    settings.REJECTION["INSTANCE_STATE_REJECTION_COMPLETE"],
                    self.context["request"].user,
                )

            workflow_api.cancel_case(
                case=source_case,
                user=self.context["request"].caluma_info.context.user,
            )

            history_text_data = {
                "dossier_number": MasterData(instance.case).dossier_number
            }

            create_history_entry(
                source_instance,
                self.context["request"].user,
                settings.REJECTION["HISTORY_ENTRIES"]["COMPLETE"],
                lambda _: history_text_data,
            )

    def _be_copy_responsible_person(self, instance):
        try:
            source_instance = instance.case.document.source.case.instance
        except AttributeError:
            return

        if (
            settings.APPLICATION.get("COPY_RESPONSIBLE_PERSON_ON_SUBMIT")
            and source_instance
        ):
            target_active_service = instance.responsible_service(
                filter_type="municipality"
            )
            source_responsible_service = source_instance.responsible_services.filter(
                service=target_active_service
            ).first()

            if source_responsible_service:
                target_responsible_service = ResponsibleService.objects.create(
                    instance=instance,
                    service=target_active_service,
                    responsible_user=source_responsible_service.responsible_user,
                )
                reassign_work_items(target_responsible_service)

    def _complete_submit_work_item(self, instance):
        work_item = instance.case.work_items.filter(
            task_id__in=settings.APPLICATION["CALUMA"]["SUBMIT_TASKS"],
            status=workflow_models.WorkItem.STATUS_READY,
        ).first()

        if work_item:
            workflow_api.complete_work_item(
                work_item=work_item,
                user=self.context["request"].caluma_info.context.user,
                context={"data_source_context": {"instanceId": instance.pk}},
            )

    def _be_extend_validity_skip_ebau_number(self, case):
        if case.document.form.slug == settings.APPLICATION["CALUMA"].get(
            "EXTEND_VALIDITY_FORM"
        ):
            workflow_api.skip_work_item(
                work_item=case.work_items.get(task_id="ebau-number"),
                user=self.context["request"].caluma_info.context.user,
            )

    def _be_handle_internal_workflow(self, case, instance):
        if case.workflow.slug == "internal":
            instance.instance_state = models.InstanceState.objects.get(
                name="in_progress_internal"
            )

    def _handle_extend_validity_form(self, case, instance):
        if case.document.form.slug == settings.APPLICATION["CALUMA"].get(
            "EXTEND_VALIDITY_FORM"
        ):
            instance.instance_state = models.InstanceState.objects.get(
                name="circulation_init"
            )

    def _set_location_for_municipality(self, case, instance):
        if not settings.APPLICATION["CALUMA"].get("USE_LOCATION"):
            return

        instance.location = Location.objects.get(
            communal_federal_number=case.document.answers.get(
                question_id="municipality"
            ).value
        )
        self._update_instance_location(instance)

    @permission_aware
    def _ur_internal_submission(self, instance, group):
        """Run side effects when instance is submitted by internal role."""
        pass

    def _ur_internal_submission_for_municipality(self, instance, group):
        if settings.APPLICATION_NAME == "kt_uri":
            instance.instance_state = models.InstanceState.objects.get(name="comm")

    def _ur_internal_submission_for_coordination(self, instance, group):
        # This is not possible for other cantons because this service group only exists in uri
        if settings.APPLICATION_NAME != "kt_uri":  # pragma: no cover
            return

        is_federal = group.service.pk == uri_constants.BUNDESSTELLE_SERVICE_ID
        instance.instance_state = models.InstanceState.objects.get(
            name="comm" if is_federal else "ext"
        )
        instance.group = group

    def _ur_prepare_cantonal_instances(self, instance):
        if settings.APPLICATION_NAME != "kt_uri":
            return

        if instance.case.document.form.slug == "cantonal-territory-usage":
            event_type_answer = self.get_master_data(instance.case).veranstaltung_art

            if event_type_answer in settings.APPLICATION["CALUMA"].get("KOOR_SD_SLUGS"):
                instance.group = Group.objects.get(pk=uri_constants.KOOR_SD_GROUP_ID)
            else:
                instance.group = Group.objects.get(pk=uri_constants.KOOR_BD_GROUP_ID)

        elif instance.case.document.form.slug in [
            "konzession-waermeentnahme",
            "bohrbewilligung-waermeentnahme",
        ]:
            instance.group = Group.objects.get(pk=uri_constants.KOOR_AFE_GROUP_ID)
        elif instance.case.document.form.slug == "pgv-gemeindestrasse":
            instance.group = Group.objects.get(pk=uri_constants.KOOR_BD_GROUP_ID)
        else:
            return

        instance.instance_state = models.InstanceState.objects.get(name="ext")

        self._update_instance_location(instance)

    def _ur_copy_oereb_instance_for_koor_afj(self, instance):
        """In Kt. UR, for specific ÖREB instances a copy for KOOR AFJ is created."""
        if not settings.APPLICATION_NAME == "kt_uri":
            return

        if instance.case.document.form.slug in [
            "oereb",
            "oereb-verfahren-gemeinde",
        ] and instance.case.document.answers.filter(
            value__in=[
                "waldfeststellung-mit-statischen-waldgrenzen-kanton-ja",
                "waldfeststellung-mit-statischen-waldgrenzen-gemeinde-ja",
            ]
        ):
            caluma_form = caluma_api.get_form_slug(instance)

            data = {
                "generate_identifier": True,
                "form": models.Form.objects.get(form_id=instance.form_id),
                "group": self.context.get("request").group,
                "instance_state": instance.instance_state,
                "previous_instance_state": instance.previous_instance_state,
                "user": self.context["request"].user,
            }

            koor_afj_instance = domain_logic.CreateInstanceLogic.create(
                data,
                caluma_user=self.context["request"].caluma_info.context.user,
                camac_user=self.context["request"].user,
                group=self.context.get("request").group,
                lead=self.initial_data.get("lead", None),
                is_modification=False,
                is_paper=True,
                caluma_form=caluma_form,
                source_instance=instance,
                skip_exported_form_attachment=True,
            )
            koor_afj_instance.case.meta["oereb_copy"] = True
            koor_afj_instance.case.save()
            koor_afj_instance.group = Group.objects.get(
                pk=uri_constants.KOOR_AFJ_GROUP_ID
            )
            koor_afj_instance.instance_state = models.InstanceState.objects.get(
                name="ext"
            )
            self._update_instance_location(koor_afj_instance)
            koor_afj_instance.save()
            self._set_submit_date(koor_afj_instance.case, koor_afj_instance)
            self._generate_and_store_pdf(koor_afj_instance)
            self._set_authority(koor_afj_instance)
            self._send_notifications(koor_afj_instance.case)

    def _send_notifications(self, case):
        notification_key = "SUBMIT"
        if case.workflow_id == "preliminary-clarification":  # pragma: no cover
            notification_key = "SUBMIT_PRELIMINARY_CLARIFICATION"
        if case.document.form_id == "cantonal-territory-usage":
            if case.instance.group_id == uri_constants.KOOR_SD_GROUP_ID:
                notification_key = "SUBMIT_KOOR_SD"
            else:
                notification_key = "SUBMIT_KOOR_BD"
        if case.document.form_id == "heat-generator":  # pragma: no cover
            notification_key = "SUBMIT_HEAT_GENERATOR"
        if case.document.form_id in [
            "konzession-waermeentnahme",
            "bohrbewilligung-waermeentnahme",
        ]:
            notification_key = "SUBMIT_KOOR_AFE"
        if case.document.form_id == "pgv-gemeindestrasse":
            notification_key = "SUBMIT_KOOR_BD"
        if case.document.form_id == "oereb":
            notification_key = "SUBMIT_KOOR_NP"
        if case.document.form_id == "mitbericht-kanton":
            return

        # send out emails upon submission
        for notification_config in settings.APPLICATION["NOTIFICATIONS"][
            notification_key
        ]:
            self._send_notification(**notification_config)

    def _ur_link_technische_bewilligung(self, instance):
        if settings.APPLICATION_NAME != "kt_uri":
            return

        if instance.case.document.form.slug != "technische-bewilligung":
            return

        existing_instance_id = CalumaApi().get_answer_value(
            "dossier-id-laufendes-verfahren", instance
        )

        if existing_instance_id:
            existing_instance = models.Instance.objects.get(pk=existing_instance_id)
            link_instances(instance, existing_instance)

    def _set_instance_service(self, case, instance):
        if settings.APPLICATION.get(
            "USE_INSTANCE_SERVICE"
        ) and not instance.responsible_service(filter_type="municipality"):
            municipality = case.document.answers.get(question_id="gemeinde").value
            InstanceService.objects.create(
                instance=self.instance,
                service_id=int(municipality),
                active=1,
                activation_date=None,
            )

    def _generate_identifier(self, case, instance):
        if settings.APPLICATION["CALUMA"].get("GENERATE_IDENTIFIER"):
            # Give dossier a unique dossier number
            identifier = domain_logic.CreateInstanceLogic.generate_identifier(instance)
            case.meta["dossier-number"] = identifier
            case.meta["dossier-number-sort"] = generate_sort_key(identifier)
            case.save()

    def _get_authority_pk_for_forest_dossiers(self, instance):
        forest_answer = instance.case.document.answers.filter(
            question_id__in=[
                "waldfeststellung-mit-statischen-waldgrenzen-kanton",
                "waldfeststellung-mit-statischen-waldgrenzen-gemeinde",
            ]
        ).first()
        if (
            forest_answer
            and instance.case.meta.get("oereb_copy", False)
            and forest_answer.value
            in [
                "waldfeststellung-mit-statischen-waldgrenzen-kanton-ja",
                "waldfeststellung-mit-statischen-waldgrenzen-gemeinde-ja",
            ]
        ):
            return str(uri_constants.AMT_FUER_FORST_UND_JAGD_AUTHORITY_ID)

        return None

    def _get_authority_pk_for_special_locations(self, instance):
        municipality = instance.case.document.answers.get(
            question_id="municipality"
        ).value

        if municipality in [
            str(uri_constants.BFS_NR_DIVERSE_GEMEINDEN),
            str(uri_constants.BFS_NR_ALLE_GEMEINDEN),
        ]:
            if instance.case.document.form.slug in [
                "oereb",
                "oereb-verfahren-gemeinde",
            ]:
                return str(uri_constants.KOOR_NP_AUTHORITY_ID)

            # if non-oereb dossiers are submitted at alle/diverse gemeinden,
            # send them to the submitting municipality
            return AuthorityLocation.objects.get(
                location=self.context["request"].group.locations.first()
            ).authority_id

        return None

    def _get_authority_pk(self, instance):
        if instance.case.document.form.slug == "pgv-gemeindestrasse":
            return str(uri_constants.BAUDIREKTION_AUTHORITY_ID)
        if instance.case.document.form.slug in [
            "konzession-waermeentnahme",
            "bohrbewilligung-waermeentnahme",
        ]:
            return str(uri_constants.AMT_FUER_ENERGIE_AUTHORITY_ID)
        if (
            instance.case.document.form.slug == "bgbb"
            and instance.group.pk == uri_constants.KOOR_AFG_GROUP_ID
        ):
            return str(uri_constants.KOOR_AFG_AUTHORITY_ID)
        if internal_authority := self.get_master_data(
            instance.case
        ).leitbehoerde_internal_form:
            # in internal forms, KOORs can set a custom authority by answering a specific question
            # this takes precedence over the default authority given by the location
            return internal_authority
        if forest_authority := self._get_authority_pk_for_forest_dossiers(instance):
            return forest_authority
        if special_location_authority := self._get_authority_pk_for_special_locations(
            instance
        ):
            return special_location_authority

        # Fallback: Location-based authority
        return (
            AuthorityLocation.objects.filter(location_id=instance.location_id)
            .first()
            .authority_id
        )

    def _set_authority(self, instance):
        """Fill the answer to the question 'leitbehorde' (only used in UR)."""
        if not settings.APPLICATION["CALUMA"].get("USE_LOCATION", False):
            return

        if authority := self._get_authority_pk(instance):
            caluma_api.update_or_create_answer(
                instance.case.document,
                "leitbehoerde",
                str(authority),
                user=self.context["request"].caluma_info.context.user,
            )

    @transaction.atomic
    def update(self, instance, validated_data):
        request_logger.info(f"Submitting instance {instance.pk}")

        case = self.instance.case
        group = self.context["request"].group

        instance.previous_instance_state = instance.instance_state
        instance.instance_state = models.InstanceState.objects.get(name="subm")

        self._be_handle_internal_workflow(case, instance)
        self._handle_extend_validity_form(case, instance)
        self._set_location_for_municipality(case, instance)
        self._ur_internal_submission(instance, group)
        self._ur_prepare_cantonal_instances(instance)

        instance.save()

        self._ur_link_technische_bewilligung(instance)
        self._set_instance_service(case, instance)
        self._generate_identifier(case, instance)
        self._set_authority(instance)
        self._set_submit_date(case, instance)
        self._generate_and_store_pdf(instance)
        self._create_history_entry(gettext_noop("Dossier submitted"))
        self._update_rejected_instance(instance)
        self._complete_submit_work_item(instance)
        self._be_extend_validity_skip_ebau_number(case)
        self._be_copy_responsible_person(instance)
        self._ur_copy_oereb_instance_for_koor_afj(instance)
        self._send_notifications(case)

        instance_submitted.send(
            sender=self.__class__,
            instance=instance,
            user_pk=self.context["request"].user.pk,
            group_pk=group.pk,
        )

        return instance


class CalumaInstanceReportSerializer(CalumaInstanceSubmitSerializer):
    """Handle submission of "SB1" form."""

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.previous_instance_state = instance.instance_state
        instance.instance_state = models.InstanceState.objects.get(name="sb2")

        instance.save()

        work_item = self.instance.case.work_items.filter(
            task_id=settings.APPLICATION["CALUMA"]["REPORT_TASK"],
            status=workflow_models.WorkItem.STATUS_READY,
        ).first()

        if work_item:
            workflow_api.complete_work_item(
                work_item=work_item,
                user=self.context["request"].caluma_info.context.user,
            )

        # generate and submit pdf
        self._generate_and_store_pdf(instance, "sb1")

        self._create_history_entry(gettext_noop("SB1 submitted"))

        sb1_submitted.send(
            sender=self.__class__,
            instance=instance,
            user_pk=self.context["request"].user.pk,
            group_pk=self.context["request"].group.pk,
        )

        # send out emails upon submission
        for notification_config in settings.APPLICATION["NOTIFICATIONS"]["REPORT"]:
            self._send_notification(**notification_config)

        return instance


class CalumaInstanceArchiveSerializer(serializers.Serializer):
    """Handle archiving of an instance."""

    @transaction.atomic
    def update(self, instance, validated_data):
        # update the instance state
        instance.previous_instance_state = instance.instance_state
        instance.instance_state = models.InstanceState.objects.get(name="archived")
        instance.save()

        case = instance.case

        # cancel the caluma case if it's still running or suspended (rejected)
        if case.status in [
            workflow_models.Case.STATUS_RUNNING,
            workflow_models.Case.STATUS_SUSPENDED,
        ]:
            workflow_api.cancel_case(
                case, self.context["request"].caluma_info.context.user
            )

        # create a history entry
        create_history_entry(
            self.instance, self.context["request"].user, gettext_noop("Archived")
        )

        return instance

    class Meta:
        resource_name = "instance-archives"


class CalumaInstanceChangeFormSerializer(serializers.Serializer):
    """Handle changing the form of an instance."""

    interchangeable_forms = [
        ["baugesuch", "baugesuch-generell", "baugesuch-mit-uvp"],
        ["baugesuch-v2", "baugesuch-generell-v2", "baugesuch-mit-uvp-v2"],
        ["baugesuch-v3", "baugesuch-generell-v3", "baugesuch-mit-uvp-v3"],
    ]

    form = serializers.CharField()

    def validate_form(self, value):
        current_form = CalumaApi().get_form_slug(self.instance)
        valid_forms = next(
            filter(lambda f: current_form in f, self.interchangeable_forms), None
        )

        if not valid_forms:
            raise exceptions.ValidationError(
                _("The current form '%(form)s' can't be changed")
                % {"form": current_form}
            )

        if value not in valid_forms:
            raise exceptions.ValidationError(
                _("'%(form)s' is not a valid form type") % {"form": value}
            )

        return value

    @transaction.atomic
    def update(self, instance, validated_data):
        case = instance.case

        case.document.form_id = validated_data["form"]
        case.document.save()

        # create a history entry
        create_history_entry(
            self.instance,
            self.context["request"].user,
            gettext_noop("Changed form type"),
        )

        return instance

    class Meta:
        resource_name = "instance-change-forms"


class CalumaInstanceSetEbauNumberSerializer(serializers.Serializer):
    """Handle setting of the ebau-number."""

    ebau_number = serializers.CharField(required=False, allow_blank=True)

    def validate_ebau_number(self, value):
        """Validate the ebau number field.

        This field expects a string of the format "[year]-[number]" (e.g.
        2020-12) or an empty string if the number should be generated
        automatically.

        If a number is passed, there must be an instance with the same number
        in the same municipality but there mustn't be an instance with the
        same number in a different municipality.
        """

        if not value:
            return generate_ebau_nr(timezone.now().year)

        if not re.search(r"\d{4}-\d+", value):
            raise exceptions.ValidationError(_("Invalid format"))

        municipality = self.instance.responsible_service(filter_type="municipality")

        instances = models.Instance.objects.filter(**{"case__meta__ebau-number": value})

        if not instances.exists():
            raise exceptions.ValidationError(_("This eBau number doesn't exist"))

        if not instances.filter(instance_services__service=municipality).exists():
            raise exceptions.ValidationError(
                _("This eBau number is already in use by a different municipality")
            )

        return value

    @permission_aware
    def _update_workflow(self, instance, case):
        # The workflow should only be updated if the municipality sets the ebau number
        pass

    def _update_workflow_for_municipality(self, instance, case):
        work_item = case.work_items.filter(
            task_id="ebau-number", status=workflow_models.WorkItem.STATUS_READY
        ).first()

        if work_item:
            workflow_api.complete_work_item(
                work_item=work_item,
                user=self.context["request"].caluma_info.context.user,
            )

    @transaction.atomic
    def update(self, instance, validated_data):
        ebau_number = validated_data.get("ebau_number")
        instance.case.meta["ebau-number"] = ebau_number
        if ebau_number:
            instance.case.meta["ebau-number-sort"] = generate_sort_key(ebau_number)
        instance.case.save()

        self._update_workflow(instance, instance.case)

        return instance

    class Meta:
        resource_name = "instance-set-ebau-numbers"


class CalumaInstanceChangeResponsibleServiceSerializer(serializers.Serializer):
    """Handle changing of the responsible service."""

    service_type = serializers.CharField()
    to = serializers.ResourceRelatedField(queryset=Service.objects.all())

    def validate_service_type(self, value):
        expected = [
            key.lower()
            for key in settings.APPLICATION.get("ACTIVE_SERVICES", {}).keys()
        ]

        if value not in expected:
            raise exceptions.ValidationError(
                _(
                    "%(value)s is not a valid service type - valid types are: %(expected)s"
                    % {"value": value, "expected": ", ".join(expected)}
                )
            )

        return value

    def validate(self, data):
        # validate audit documents
        try:
            CalumaApi().validate_existing_audit_documents(
                self.instance.pk, self.context["request"].caluma_info.context.user
            )
        except CustomValidationError:
            raise exceptions.ValidationError(_("Invalid audit"))

        return super().validate(data)

    def _sync_with_caluma(self, from_service, to_service):
        CalumaApi().reassign_work_items(
            self.instance,
            from_service.pk,
            to_service.pk,
            self.context["request"].caluma_info.context.user,
        )

    def _send_notification(self):
        config = settings.APPLICATION["NOTIFICATIONS"].get("CHANGE_RESPONSIBLE_SERVICE")

        if config:
            send_mail(
                config["template_slug"],
                self.context,
                recipient_types=config["recipient_types"],
                instance={"type": "instances", "id": self.instance.pk},
            )

    def _trigger_ech_message(self):
        change_responsibility.send(
            sender=self.__class__,
            instance=self.instance,
            user_pk=self.context["request"].user.pk,
            group_pk=self.context["request"].group.pk,
        )

    def _add_history_entry(self, to_service):
        def get_text_data(language):
            service_t = to_service.trans.filter(language=language).first()

            return {"service": service_t.name if service_t else to_service.name}

        create_history_entry(
            self.instance,
            self.context["request"].user,
            gettext_noop("Changed responsible service to: %(service)s"),
            get_text_data,
        )

    @transaction.atomic
    def update(self, instance, validated_data):
        filter_type = validated_data["service_type"]

        from_service = instance.responsible_service(filter_type=filter_type)
        to_service = validated_data["to"]

        instance.instance_services.filter(service=from_service).update(active=0)
        instance.instance_services.update_or_create(
            service=to_service,
            defaults={"active": 1, "activation_date": timezone.now()},
        )

        if (
            instance.responsible_service(filter_type=filter_type) != to_service
        ):  # pragma: no cover
            raise exceptions.ValidationError(
                _(
                    "Responsible service did not change for instance %(instance_id)s"
                    % instance.pk
                )
            )

        # Side effects
        self._sync_with_caluma(from_service, to_service)
        self._send_notification()
        # Changing the active construction control should not trigger an eCH0211 event
        if filter_type != "construction_control":
            self._trigger_ech_message()
        self._add_history_entry(to_service)

        return instance

    class Meta:
        resource_name = "instance-change-responsible-services"


class CalumaInstanceFixWorkItemsSerializer(serializers.Serializer):
    dry = serializers.BooleanField(default=True)
    output = serializers.CharField()

    def update(self, instance, validated_data):
        output = StringIO()

        call_command(
            "fix_work_items",
            instance=instance.pk,
            no_color=True,
            stdout=output,
            **validated_data,
        )

        Response = namedtuple("Response", ("dry", "output", "pk"))

        return Response(**validated_data, output=output.getvalue(), pk=None)

    class Meta:
        resource_name = "instance-fix-work-items"
        fields = ("dry", "output")
        read_only_fields = ("output",)


class CalumaInstanceFinalizeSerializer(CalumaInstanceSubmitSerializer):
    """Handle submission of "SB2" form."""

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.previous_instance_state = instance.instance_state
        instance.instance_state = models.InstanceState.objects.get(name="conclusion")
        user = self.context["request"].caluma_info.context.user

        instance.save()

        work_item = instance.case.work_items.filter(
            task_id=settings.APPLICATION["CALUMA"]["FINALIZE_TASK"],
            status=workflow_models.WorkItem.STATUS_READY,
        ).first()

        workflow_api.complete_work_item(work_item=work_item, user=user)

        # generate and submit pdf
        self._generate_and_store_pdf(instance, "sb2")

        self._create_history_entry(gettext_noop("SB2 submitted"))

        sb2_submitted.send(
            sender=self.__class__,
            instance=instance,
            user_pk=self.context["request"].user.pk,
            group_pk=self.context["request"].group.pk,
        )

        # send out emails upon submission
        for notification_config in settings.APPLICATION["NOTIFICATIONS"]["FINALIZE"]:
            self._send_notification(**notification_config)

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

    def validate(self, data):
        location = self.instance.location
        if location is None:
            raise exceptions.ValidationError(_("No location assigned."))

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

    @transaction.atomic
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)

        # Generate identifier and save it immediately to minimize the
        # possibility of submitting instances with the same identifier
        instance.identifier = domain_logic.CreateInstanceLogic.generate_identifier(
            instance
        )
        instance.save()

        instance_submitted.send(
            sender=self.__class__,
            instance=instance,
            user_pk=self.context["request"].user.pk,
            group_pk=self.context["request"].group.pk,
        )
        return instance


class FormFieldSerializer(InstanceEditableMixin, serializers.ModelSerializer):
    included_serializers = {"instance": InstanceSerializer}

    def validate_name(self, name):
        # TODO: check whether question is part of used form

        perms = settings.APPLICATION.get("ROLE_PERMISSIONS", {})
        group = self.context["request"].group
        permission = perms.get(group.role.name, "applicant")

        question = settings.FORM_CONFIG["questions"].get(name)
        if question is None:
            raise exceptions.ValidationError(
                _("invalid question %(question)s.") % {"question": name}
            )

        # per default only applicant may edit a question
        restrict = question.get("restrict", ["applicant", "support"])
        if permission not in restrict:
            raise exceptions.ValidationError(
                _("%(permission)s is not allowed to edit question %(question)s.")
                % {"question": name, "permission": permission}
            )

        return name

    def validate(self, data):
        validated_data = super().validate(data)

        for history_field in settings.APPLICATION.get("FORM_FIELD_HISTORY_ENTRY", []):
            if not validated_data["name"] == history_field["name"]:  # pragma: no cover
                continue

            if (
                not self.instance
                and validated_data["value"]  # field is new and has a value
            ) or (
                self.instance
                and self.instance.value
                != validated_data["value"]  # field is existing but the value changed
            ):
                models.HistoryEntry.objects.create(
                    instance=validated_data["instance"],
                    created_at=timezone.now(),
                    user=self.context["request"].user,
                    history_type=HistoryActionConfig.HISTORY_TYPE_NOTIFICATION,
                    title=history_field["title"],
                    body=validated_data["value"],
                )

        return validated_data

    class Meta:
        model = models.FormField
        fields = ("name", "value", "instance")


class DurationField(serializers.DurationField):
    def to_representation(self, value):
        if not value:
            return None

        total_seconds = value.total_seconds()
        total_hours = int(total_seconds // 3600)
        minutes = int((total_seconds // 60) % 60)

        return f"{total_hours:0>2}:{minutes:0>2}"


class JournalEntrySerializer(InstanceEditableMixin, serializers.ModelSerializer):
    included_serializers = {
        "instance": InstanceSerializer,
        "user": "camac.user.serializers.UserSerializer",
    }

    visibility = serializers.ChoiceField(choices=models.JournalEntry.VISIBILITIES)
    duration = DurationField(allow_null=True)

    def create(self, validated_data):
        validated_data["modification_date"] = timezone.now()
        validated_data["creation_date"] = timezone.now()
        validated_data["user"] = self.context["request"].user
        validated_data["service"] = self.context["request"].group.service
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["modification_date"] = timezone.now()
        return super().update(instance, validated_data)

    class Meta:
        model = models.JournalEntry
        fields = (
            "instance",
            "service",
            "user",
            "text",
            "duration",
            "creation_date",
            "modification_date",
            "visibility",
        )
        read_only_fields = ("service", "user", "creation_date", "modification_date")


class HistoryEntrySerializer(
    MultilingualSerializer, InstanceEditableMixin, serializers.ModelSerializer
):
    service = ServiceResourceRelatedField(default=CurrentServiceDefault())
    title = MultilingualField()
    body = MultilingualField(required=False)

    included_serializers = {
        "instance": InstanceSerializer,
        "user": "camac.user.serializers.UserSerializer",
    }

    def create(self, validated_data):
        entry = super().create(validated_data)
        models.HistoryEntryT.objects.create(
            history_entry=entry,
            title=entry.title,
            body=entry.body,
            language=self.context["request"].META["HTTP_CONTENT_LANGUAGE"],
        )
        return entry

    def update(self, instance, validated_data):
        entry = super().update(instance, validated_data)
        translation = models.HistoryEntryT.objects.filter(
            history_entry=instance,
            language=self.context["request"].META["HTTP_CONTENT_LANGUAGE"],
        ).first()
        if not translation:
            models.HistoryEntryT.objects.create(
                history_entry=entry,
                title=entry.title,
                body=entry.body,
                language=self.context["request"].META["HTTP_CONTENT_LANGUAGE"],
            )
        else:
            translation.title = entry.title
            translation.body = entry.body
            translation.save()
        return entry

    class Meta:
        model = models.HistoryEntry
        fields = (
            "instance",
            "service",
            "user",
            "created_at",
            "title",
            "body",
            "history_type",
        )
        read_only_fields = ("service", "created_at")


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


class PublicCalumaInstanceSerializer(serializers.Serializer):  # pragma: no cover
    """Serialize public caluma instances."""

    document_id = serializers.CharField(read_only=True)
    instance_id = serializers.IntegerField(read_only=True)
    publication_date = serializers.DateTimeField(read_only=True)
    publication_end_date = serializers.DateTimeField(read_only=True)
    publication_text = serializers.CharField(read_only=True)

    dossier_nr = serializers.SerializerMethodField()
    municipality = serializers.SerializerMethodField()
    applicant = serializers.SerializerMethodField()
    intent = serializers.SerializerMethodField()
    street = serializers.SerializerMethodField()
    parcels = serializers.SerializerMethodField()
    oereb_topic = serializers.SerializerMethodField()
    legal_state = serializers.SerializerMethodField()
    instance_state = serializers.SerializerMethodField()
    form_type = serializers.SerializerMethodField()
    form_description = serializers.SerializerMethodField()
    authority = serializers.SerializerMethodField()

    _master_data_cache = {}

    def get_master_data(self, case):
        request = self.context["request"]
        if not hasattr(request, "_master_data_cache"):
            request._master_data_cache = {}
        if case.pk not in request._master_data_cache:
            request._master_data_cache[case.pk] = MasterData(case)

        return request._master_data_cache[case.pk]

    def get_municipality(self, case):
        municipality = self.get_master_data(case).municipality
        if not municipality:
            return None

        return municipality.get("label") if "label" in municipality else municipality

    def get_applicant(self, case):
        return clean_join(
            *[
                applicant.get("juristic_name")
                if applicant.get("is_juristic_person")
                else clean_join(applicant.get("first_name"), applicant.get("last_name"))
                for applicant in self.get_master_data(case).applicants
            ],
            separator=", ",
        )

    def get_intent(self, case):
        if settings.APPLICATION_NAME == "kt_uri":
            form_type = self.get_master_data(case).form_type

            if form_type == "form-type-commercial-permit":
                return "Reklamegesuch"
            elif form_type == "form-type-solar-announcement":
                return "Solaranlage"
        return self.get_master_data(case).proposal

    def get_street(self, case):
        if settings.APPLICATION_NAME == "kt_schwyz":
            return clean_join(
                self.get_master_data(case).street,
                self.get_master_data(case).street_addition,
                self.get_master_data(case).city,
                separator=", ",
            )

        return clean_join(
            self.get_master_data(case).street,
            self.get_master_data(case).street_number,
        )

    def get_parcels(self, case):
        return clean_join(
            *[plot.get("plot_number") for plot in self.get_master_data(case).plot_data],
            separator=", ",
        )

    def get_oereb_topic(self, case):
        if settings.APPLICATION.get("USE_OEREB_FIELDS_FOR_PUBLIC_ENDPOINT"):
            return self.get_master_data(case).oereb_topic
        return ""

    def get_legal_state(self, case):
        if settings.APPLICATION.get("USE_OEREB_FIELDS_FOR_PUBLIC_ENDPOINT"):
            return self.get_master_data(case).legal_state
        return ""

    def get_instance_state(self, case):
        if settings.APPLICATION.get("USE_OEREB_FIELDS_FOR_PUBLIC_ENDPOINT"):
            return case.instance.instance_state.name
        elif settings.APPLICATION_NAME == "kt_schwyz":
            return case.instance.instance_state.name
        return ""

    def get_form_type(self, case):
        if settings.APPLICATION.get("USE_OEREB_FIELDS_FOR_PUBLIC_ENDPOINT"):
            return self.get_master_data(case).form_type
        elif settings.APPLICATION_NAME == "kt_schwyz":
            return case.instance.form.name
        return ""

    def get_form_description(self, case):
        if settings.APPLICATION_NAME == "kt_schwyz":
            return case.instance.form.description
        return ""

    def get_authority(self, case):
        if settings.APPLICATION.get("USE_OEREB_FIELDS_FOR_PUBLIC_ENDPOINT"):
            authority = self.get_master_data(case).authority
            return authority.get("label") if authority else None
        return ""

    def get_dossier_nr(self, case):
        return self.get_master_data(case).dossier_number

    class Meta:
        model = workflow_models.Case
        resource_name = "public-caluma-instances"


class CalumaInstanceConvertModificationSerializer(serializers.Serializer):
    content = serializers.CharField(write_only=True)

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.case.document.answers.filter(
            question_id="beschreibung-bauvorhaben"
        ).update(value=validated_data["content"])

        instance.case.document.answers.filter(
            question_id="beschreibung-projektaenderung"
        ).delete()

        instance.case.document.answers.filter(question_id="projektaenderung").update(
            value="projektaenderung-nein"
        )

        instance.case.document.source = None
        instance.case.document.save()

        return instance

    class Meta:
        resource_name = "instance-convert-modifications"


class CalumaInstanceAppealSerializer(serializers.Serializer):
    @transaction.atomic
    def update(self, instance, validated_data):
        user = self.context["request"].user
        caluma_user = self.context["request"].caluma_info.context.user

        new_instance = copy_instance(
            instance=instance,
            group=self.context["request"].group,
            user=user,
            caluma_user=caluma_user,
            skip_submit=True,
            # Mark the new instance as appeal so we can determine whether to
            # show the appeal module in the navigation and mark it in the name.
            # Also, we mark the old instance as "has-appeal" so we can prevent
            # another appeal from that instance.
            new_meta={"is-appeal": True},
            old_meta={"has-appeal": True},
        )

        fill_ebau_number(
            instance=new_instance,
            ebau_number=instance.case.meta["ebau-number"],
            caluma_user=caluma_user,
        )

        # Set the status of the old instance to finished if current status is sb1
        if instance.instance_state.name == "sb1":
            for task, fn in [
                ("sb1", workflow_api.skip_work_item),
                ("sb2", workflow_api.skip_work_item),
                ("complete", workflow_api.complete_work_item),
            ]:
                fn(
                    work_item=instance.case.work_items.get(task_id=task),
                    user=caluma_user,
                )

            instance.set_instance_state("finished", user)

        # Add history entry to source instance
        create_history_entry(instance, user, gettext_noop("Appeal received"))

        # Send notifications
        for config in settings.APPEAL["NOTIFICATIONS"].get("APPEAL_SUBMITTED", []):
            send_mail(
                config["template_slug"],
                self.context,
                recipient_types=config["recipient_types"],
                instance={"type": "instances", "id": instance.pk},
            )

        return new_instance

    class Meta:
        resource_name = "instance-appeals"


class CalumaInstanceCorrectionSerializer(serializers.Serializer):
    def validate(self, data):
        if workflow_models.WorkItem.objects.filter(
            task_id=settings.DISTRIBUTION["INQUIRY_TASK"],
            status=workflow_models.WorkItem.STATUS_READY,
            case__family__instance=self.instance,
        ).exists():
            raise exceptions.ValidationError(
                _("The Dossier can't be correct because there are running inquiries.")
            )

        return data

    @transaction.atomic
    def update(self, instance, validated_data):
        caluma_user = self.context["request"].caluma_info.context.user
        camac_user = self.context["request"].user

        if (
            instance.instance_state.name
            in settings.CORRECTION["ALLOWED_INSTANCE_STATES"]
        ):
            workflow_api.suspend_case(instance.case, caluma_user)
            instance.set_instance_state(
                settings.CORRECTION["INSTANCE_STATE"], camac_user
            )
        elif instance.instance_state.name == settings.CORRECTION["INSTANCE_STATE"]:
            DocumentValidator().validate(instance.case.document, caluma_user)

            workflow_api.resume_case(instance.case, caluma_user)
            instance.set_instance_state(
                instance.previous_instance_state.name, camac_user
            )

            for config in settings.APPLICATION["NOTIFICATIONS"].get(
                "DOSSIERKORREKTUR", []
            ):  # pragma: no cover
                send_mail_without_request(
                    config["template_slug"],
                    caluma_user.username,
                    caluma_user.camac_group,
                    instance={"id": instance.pk, "type": "instances"},
                    recipient_types=config["recipient_types"],
                )

            create_history_entry(
                instance, camac_user, settings.CORRECTION["HISTORY_ENTRY"]
            )

        return instance

    class Meta:
        resource_name = "instance-corrections"


class CalumaInstanceRejectionSerializer(serializers.Serializer):
    rejection_feedback = serializers.CharField(write_only=True)

    def validate(self, data):
        domain_logic.RejectionLogic.validate_for_rejection(self.instance)

        return super().validate(data)

    @transaction.atomic
    def update(self, instance, validated_data):
        caluma_user = self.context["request"].caluma_info.context.user
        camac_user = self.context["request"].user
        camac_group = self.context["request"].group

        if instance.instance_state.name == settings.REJECTION["INSTANCE_STATE"]:
            instance = domain_logic.RejectionLogic.revert_instance_rejection(
                instance,
                camac_user,
                camac_group,
                caluma_user,
            )
        else:
            instance = domain_logic.RejectionLogic.reject_instance(
                instance,
                camac_user,
                camac_group,
                caluma_user,
                validated_data["rejection_feedback"],
            )

        return instance

    class Meta:
        resource_name = "instance-rejections"
