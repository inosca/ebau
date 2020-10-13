import json
from logging import getLogger
from uuid import uuid4

from caluma.caluma_form.models import Form
from caluma.caluma_workflow import api as workflow_api, models as workflow_models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields.jsonb import KeyTextTransform
from django.core.files.base import ContentFile
from django.db import transaction
from django.db.models import Max, Q
from django.utils import timezone
from django.utils.translation import gettext as _, gettext_noop
from rest_framework import exceptions
from rest_framework_json_api import relations, serializers

from camac.caluma.api import CalumaApi
from camac.caluma.extensions.data_sources import Municipalities
from camac.constants import kt_bern as be_constants
from camac.core.models import (
    Answer,
    HistoryActionConfig,
    InstanceLocation,
    InstanceService,
    ProposalActivation,
)
from camac.core.serializers import MultilingualField, MultilingualSerializer
from camac.core.translations import get_translations
from camac.document.models import AttachmentSection
from camac.echbern.signals import (
    change_responsibility,
    instance_submitted,
    sb1_submitted,
    sb2_submitted,
)
from camac.instance.mixins import InstanceEditableMixin
from camac.notification.views import send_mail
from camac.user.models import Group, Service
from camac.user.permissions import permission_aware
from camac.user.relations import (
    CurrentUserResourceRelatedField,
    FormDataResourceRelatedField,
    GroupResourceRelatedField,
    ServiceResourceRelatedField,
)
from camac.user.serializers import CurrentGroupDefault, CurrentServiceDefault

from ..utils import get_paper_settings
from . import document_merge_service, models, validators

SUBMIT_DATE_CHAPTER = 100001
SUBMIT_DATE_QUESTION_ID = 20036
SUBMIT_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"

request_logger = getLogger("django.request")


def get_caluma_form_from_camac(camac_form):
    mapping = settings.APPLICATION.get("FORM_MAPPING", {})
    for caluma_form, form_ids in mapping.items():
        if camac_form in form_ids:
            return caluma_form

    raise exceptions.ValidationError(
        _(f"No form mapping found for form ID {camac_form}.")
    )


def generate_identifier(instance):
    """
    Build identifier for instance.

    Format for normal forms:
    two last digits of communal location number
    year in two digits
    unique sequence
    Example: 11-18-001

    Format for special forms:
    two letter abbreviation of form
    year in two digits
    unique sequence
    Example: AV-20-014
    """
    identifier = instance.identifier
    if not identifier:
        year = timezone.now().strftime("%y")

        name = instance.form.name
        abbreviations = settings.APPLICATION.get("INSTANCE_IDENTIFIER_FORM_ABBR", {})
        meta = models.FormField.objects.filter(instance=instance, name="meta").first()
        if meta:
            meta_value = json.loads(meta.value)
            name = meta_value["formType"]

        if name in abbreviations.keys():
            identifier_start = abbreviations[name]
        elif settings.APPLICATION.get("SHORT_DOSSIER_NUMBER", False):
            identifier_start = instance.location.communal_federal_number[-2:]
        else:
            identifier_start = instance.location.communal_federal_number

        start = "{0}-{1}-".format(identifier_start, year)

        if settings.APPLICATION["CALUMA"].get("SAVE_DOSSIER_NUMBER_IN_CALUMA"):
            max_identifier = (
                workflow_models.Case.objects.filter(
                    **{"meta__dossier-number__startswith": start}
                )
                .annotate(dossier_nr=KeyTextTransform("dossier-number", "meta"))
                .aggregate(max_identifier=Max("dossier_nr"))["max_identifier"]
                or "00-00-000"
            )
        else:
            max_identifier = (
                models.Instance.objects.filter(identifier__startswith=start).aggregate(
                    max_identifier=Max("identifier")
                )["max_identifier"]
                or "00-00-000"
            )

        sequence = int(max_identifier[-3:])

        identifier = "{0}-{1}-{2}".format(
            identifier_start, timezone.now().strftime("%y"), str(sequence + 1).zfill(3),
        )

    return identifier


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
    is_applicant = serializers.SerializerMethodField()
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

    involved_services = relations.SerializerMethodResourceRelatedField(
        source="get_involved_services", model=Service, read_only=True, many=True
    )

    def get_is_applicant(self, obj):
        return obj.involved_applicants.filter(
            invitee=self.context["request"].user
        ).exists()

    def get_involved_services(self, obj):
        filters = Q(pk__in=obj.circulations.values("activations__service__pk"))

        if settings.APPLICATION.get("USE_INSTANCE_SERVICE"):
            filters |= Q(pk__in=obj.services.values("pk"))
        elif obj.group and obj.group.service:
            filters |= Q(pk=obj.group.service.pk)

        return Service.objects.filter(filters).distinct()

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
        meta_fields = ("editable", "is_applicant")
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
        )
        read_only_fields = (
            "circulations",
            "creation_date",
            "identifier",
            "modification_date",
            "services",
            "involved_services",
        )


class SchwyzInstanceSerializer(InstanceSerializer):
    @transaction.atomic
    def create(self, validated_data):
        instance = super().create(validated_data)

        workflow_api.start_case(
            workflow=workflow_models.Workflow.objects.get(pk="building-permit"),
            form=Form.objects.get(pk="baugesuch"),
            user=self.context["request"].caluma_info.context.user,
            meta={"camac-instance-id": instance.pk},
        )

        return instance


class CalumaInstanceSerializer(InstanceSerializer):
    # TODO once more than one Camac-NG project uses Caluma as a form
    # this serializer needs to be split up into what is actually
    # Caluma and what is project specific
    REJECTION_CHAPTER = 20001
    REJECTION_QUESTION = 20037
    REJECTION_ITEM = 1

    permissions = serializers.SerializerMethodField()

    instance_state = serializers.ResourceRelatedField(
        queryset=models.InstanceState.objects.filter(name="new"),
        default=NewInstanceStateDefault(),
    )

    previous_instance_state = serializers.ResourceRelatedField(
        queryset=models.InstanceState.objects.filter(name="new"),
        default=NewInstanceStateDefault(),
    )

    # TODO fix this for UR
    form = serializers.ResourceRelatedField(
        queryset=models.Form.objects.all(), default=lambda: models.Form.objects.first()
    )

    caluma_form = serializers.SerializerMethodField()

    is_paper = serializers.SerializerMethodField()  # "Papierdossier
    is_modification = serializers.SerializerMethodField()  # "Projektänderung"
    copy_source = serializers.CharField(required=False, write_only=True)

    public_status = serializers.SerializerMethodField()

    active_service = relations.SerializerMethodResourceRelatedField(
        source="get_active_service", model=Service, read_only=True
    )

    responsible_service_users = relations.SerializerMethodResourceRelatedField(
        source="get_responsible_service_users",
        model=get_user_model(),
        many=True,
        read_only=True,
    )
    rejection_feedback = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    def get_is_paper(self, instance):
        return CalumaApi().is_paper(instance)

    def get_is_modification(self, instance):
        return CalumaApi().is_modification(instance)

    def get_caluma_form(self, instance):
        return CalumaApi().get_form_slug(instance)

    def get_active_service(self, instance):
        return instance.responsible_service(filter_type="municipality")

    def get_responsible_service_users(self, instance):
        return get_user_model().objects.filter(
            pk__in=instance.responsible_services.filter(
                service=self.context["request"].group.service
            ).values("responsible_user")
        )

    def get_public_status(self, instance):
        # TODO Instead of a new field, we should actually modify the values of instance_state
        STATUS_MAP = {
            be_constants.INSTANCE_STATE_NEW: be_constants.PUBLIC_INSTANCE_STATE_CREATING,
            be_constants.INSTANCE_STATE_EBAU_NUMMER_VERGEBEN: be_constants.PUBLIC_INSTANCE_STATE_RECEIVING,
            be_constants.INSTANCE_STATE_CORRECTION_IN_PROGRESS: be_constants.PUBLIC_INSTANCE_STATE_COMMUNAL,
            be_constants.INSTANCE_STATE_IN_PROGRESS: be_constants.PUBLIC_INSTANCE_STATE_IN_PROGRESS,
            be_constants.INSTANCE_STATE_KOORDINATION: be_constants.PUBLIC_INSTANCE_STATE_IN_PROGRESS,
            be_constants.INSTANCE_STATE_VERFAHRENSPROGRAMM_INIT: be_constants.PUBLIC_INSTANCE_STATE_IN_PROGRESS,
            be_constants.INSTANCE_STATE_ZIRKULATION: be_constants.PUBLIC_INSTANCE_STATE_IN_PROGRESS,
            be_constants.INSTANCE_STATE_REJECTED: be_constants.PUBLIC_INSTANCE_STATE_REJECTED,
            be_constants.INSTANCE_STATE_CORRECTED: be_constants.PUBLIC_INSTANCE_STATE_CORRECTED,
            be_constants.INSTANCE_STATE_SB1: be_constants.PUBLIC_INSTANCE_STATE_SB1,
            be_constants.INSTANCE_STATE_SB2: be_constants.PUBLIC_INSTANCE_STATE_SB2,
            be_constants.INSTANCE_STATE_TO_BE_FINISHED: be_constants.PUBLIC_INSTANCE_STATE_FINISHED,
            be_constants.INSTANCE_STATE_FINISHED: be_constants.PUBLIC_INSTANCE_STATE_FINISHED,
            be_constants.INSTANCE_STATE_ARCHIVED: be_constants.PUBLIC_INSTANCE_STATE_ARCHIVED,
            be_constants.INSTANCE_STATE_DONE: be_constants.PUBLIC_INSTANCE_STATE_DONE,
        }

        return STATUS_MAP.get(
            instance.instance_state_id, be_constants.PUBLIC_INSTANCE_STATE_CREATING
        )

    included_serializers = {
        **InstanceSerializer.included_serializers,
        "active_service": "camac.user.serializers.PublicServiceSerializer",
        "responsible_service_users": "camac.user.serializers.UserSerializer",
        "involved_applicants": "camac.applicants.serializers.ApplicantSerializer",
    }

    @permission_aware
    def _get_main_form_permissions(self, instance):
        permissions = set(["read"])

        if instance.instance_state.name == "new":
            permissions.add("write")

        return permissions

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

        if state in ["correction", "comm"]:
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

        if (
            state in ["sb2", "conclusion"]
            and service_group.name == "construction-control"
        ):
            permissions.add("read")

        if (
            state == "sb1"
            and is_paper
            and service_group.pk in get_paper_settings("sb1")["ALLOWED_SERVICE_GROUPS"]
            and role.pk in get_paper_settings("sb1")["ALLOWED_ROLES"]
        ):
            permissions.update(["read", "write"])

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

        if state == "conclusion" and service_group.name == "construction-control":
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
        permissions = set(["write"])

        if CalumaApi().is_paper(instance):
            permissions.update(CalumaApi().get_nfd_form_permissions(instance))

        return permissions

    def _get_nfd_form_permissions_for_support(self, instance):
        return set(["read", "write"])

    @permission_aware
    def _get_case_meta_permissions(self, instance):
        return set(["read"])

    def _get_case_meta_permissions_for_service(self, instance):
        return set(["read"])

    def _get_case_meta_permissions_for_municipality(self, instance):
        permissions = set(["read"])

        if instance.instance_state.name != "new":
            permissions.add("write")

        return permissions

    def _get_case_meta_permissions_for_support(self, instance):
        return set(["read", "write"])

    def get_permissions(self, instance):
        return {
            "case-meta": self._get_case_meta_permissions(instance),
            **{
                form: sorted(getattr(self, f"_get_{form}_form_permissions")(instance))
                for form in settings.APPLICATION.get("CALUMA", {}).get(
                    "FORM_PERMISSIONS", set()
                )
            },
        }

    def get_name(self, instance):
        api = CalumaApi()
        name = api.get_form_name(instance)
        parts = []

        migrated = api.is_migrated(instance)
        paper = api.is_paper(instance)
        modification = api.is_modification(instance)

        if migrated:
            name = api.get_migration_type(instance)[1]
            parts.append(_("migrated"))

        if not migrated and paper:
            parts.append(_("paper"))

        if not migrated and modification:
            parts.append(_("modification"))

        parts = [f"({part})" for part in parts]

        return " ".join([str(name), *parts])

    def _copy_applicants(self, source, target):
        for applicant in source.involved_applicants.all():
            target.involved_applicants.update_or_create(
                invitee=applicant.invitee,
                defaults={
                    "created": timezone.now(),
                    "user": applicant.user,
                    "email": applicant.email,
                },
            )

    def _copy_attachments(self, source, target):
        for attachment in source.attachments.all():
            try:
                new_file = ContentFile(attachment.path.read())
            except FileNotFoundError:  # pragma: no cover
                # file does not exist so use the old file
                new_file = attachment.path

            # store sections first
            sections = attachment.attachment_sections.all()

            # copy the file
            new_file.name = attachment.path.name
            attachment.path = new_file

            attachment.attachment_id = None
            attachment.instance = target
            attachment.uuid = uuid4()
            attachment.save()

            attachment.attachment_sections.set(sections)
            attachment.save()

    @permission_aware
    def validate(self, data):
        return data

    def validate_for_municipality(self, data):
        group = self.context["request"].group

        if settings.APPLICATION["CALUMA"]["CREATE_IN_PROCESS"]:
            data["instance_state"] = models.InstanceState.objects.get(name="comm")

        if settings.APPLICATION["CALUMA"]["USE_LOCATION"]:
            data["location"] = group.locations.first()

        return data

    def create(self, validated_data):
        caluma_api = CalumaApi()

        copy_source = validated_data.pop("copy_source", None)
        source_instance = copy_source and models.Instance.objects.get(pk=copy_source)

        group = self.context["request"].group

        if source_instance:
            caluma_form = caluma_api.get_form_slug(source_instance)
            is_modification = self.initial_data.get("is_modification", False)
            is_paper = caluma_api.is_paper(source_instance)
        else:
            caluma_form = self.initial_data.get("caluma_form")
            if caluma_form is None:
                caluma_form = get_caluma_form_from_camac(self.validated_data["form"].pk)

            is_modification = False
            is_paper = (
                group.service  # group needs to have a service
                and group.service.service_group.pk
                in get_paper_settings()["ALLOWED_SERVICE_GROUPS"]
                and group.role.pk in get_paper_settings()["ALLOWED_ROLES"]
            )

        instance = super().create(validated_data)

        if settings.APPLICATION["CALUMA"]["USE_LOCATION"]:  # pragma: no cover
            self._update_instance_location(instance)

        workflow = workflow_models.Workflow.objects.filter(
            Q(allow_forms__in=[caluma_form]) | Q(allow_all_forms=True)
        ).first()

        case_meta = {"camac-instance-id": instance.pk}

        if settings.APPLICATION["CALUMA"].get("GENERATE_DOSSIER_NR"):
            # Give dossier a unique dossier number
            case_meta["dossier-number"] = generate_identifier(instance)

        case = workflow_api.start_case(
            workflow=workflow,
            form=Form.objects.get(pk=caluma_form),
            user=self.context["request"].caluma_info.context.user,
            meta=case_meta,
        )

        if source_instance:
            source_document_pk = workflow_models.Case.objects.get(
                **{"meta__camac-instance-id": source_instance.pk}
            ).document.pk

            old_document = case.document
            new_document = caluma_api.copy_document(
                source_document_pk,
                exclude_form_slugs=(
                    ["6-dokumente", "7-bestaetigung", "8-freigabequittung"]
                    if is_modification
                    else ["8-freigabequittung"]
                ),
            )
            case.document = new_document
            case.save()
            old_document.delete()

        # TODO migrate BE
        caluma_api.update_or_create_answer(
            case.document.pk, "is-paper", "is-paper-yes" if is_paper else "is-paper-no"
        )

        if settings.APPLICATION["CALUMA"]["HAS_PROJECT_CHANGE"]:
            caluma_api.update_or_create_answer(
                case.document.pk,
                "projektaenderung",
                "projektaenderung-ja" if is_modification else "projektaenderung-nein",
            )

        if is_paper:
            # remove the previously created applicants
            instance.involved_applicants.all().delete()

            # prefill municipality question if possible
            value = str(group.service.pk)
            source = Municipalities()

            if source.validate_answer_value(value, case.document, "gemeinde", None):
                caluma_api.update_or_create_answer(case.document.pk, "gemeinde", value)

            # create instance service for permissions
            InstanceService.objects.create(
                instance=instance,
                service_id=group.service.pk,
                active=1,
                activation_date=None,
            )

        if source_instance and not is_modification:
            self._copy_applicants(source_instance, instance)
            self._copy_attachments(source_instance, instance)

        return instance

    def get_rejection_feedback(self, instance):
        return Answer.get_value_by_cqi(
            instance,
            self.REJECTION_CHAPTER,
            self.REJECTION_QUESTION,
            self.REJECTION_ITEM,
            default="",
        )

    class Meta(InstanceSerializer.Meta):
        fields = InstanceSerializer.Meta.fields + (
            "caluma_form",
            "is_paper",
            "is_modification",
            "copy_source",
            "public_status",
            "active_service",
            "responsible_service_users",
            "involved_applicants",
            "rejection_feedback",
            "name",
        )
        read_only_fields = InstanceSerializer.Meta.read_only_fields + (
            "caluma_form",
            "is_paper",
            "is_modification",
            "public_status",
            "active_service",
            "responsible_service_users",
            "involved_applicants",
            "rejection_feedback",
            "name",
        )
        meta_fields = InstanceSerializer.Meta.meta_fields + ("permissions",)


class CalumaInstanceSubmitSerializer(CalumaInstanceSerializer):
    def _create_history_entry(self, texts):
        history = models.HistoryEntry.objects.create(
            instance=self.instance,
            created_at=timezone.now(),
            user=self.context["request"].user,
            history_type=HistoryActionConfig.HISTORY_TYPE_STATUS,
        )
        for (language, text) in texts:
            models.HistoryEntryT.objects.create(
                history_entry=history, title=text, language=language
            )

    def _notify_submit(self, template_slug, recipient_types):
        """Send notification email."""
        send_mail(
            template_slug,
            self.context,
            recipient_types=recipient_types,
            instance={"type": "instances", "id": self.instance.pk},
        )

    def _set_submit_date(self, validated_data):
        submit_date = timezone.now().strftime(SUBMIT_DATE_FORMAT)
        changed = CalumaApi().set_submit_date(self.instance.pk, submit_date)

        if changed:
            # Set submit date in Camac first...
            # TODO drop this after this is not used anymore in Camac
            Answer.objects.get_or_create(
                instance=self.instance,
                question_id=SUBMIT_DATE_QUESTION_ID,
                item=1,
                chapter_id=SUBMIT_DATE_CHAPTER,
                # CAMAC date is formatted in "dd.mm.yyyy"
                defaults={"answer": submit_date},
            )

    def _get_pdf_section(self, instance, form_slug):
        form_name = form_slug.upper() if form_slug else "MAIN"
        section_type = "PAPER" if CalumaApi().is_paper(instance) else "DEFAULT"

        return AttachmentSection.objects.get(
            pk=settings.APPLICATION["PDF"]["SECTION"][form_name][section_type]
        )

    def _generate_and_store_pdf(self, instance, form_slug=None):
        request = self.context["request"]

        pdf = document_merge_service.DMSHandler().generate_pdf(
            instance, form_slug, request
        )

        attachment_section = self._get_pdf_section(instance, form_slug)
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

    def _create_answer_proposals(self, instance):
        """Create service proposal based on answers.

        Create "action proposals" given some answer values for specific questions:
        (question, answer, config) -> AProposal
        """

        # get suggested services
        service_suggestions = CalumaApi().get_circulation_proposals(instance)

        # create answer proposals
        today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)

        proposals = [
            ProposalActivation(
                instance=instance,
                circulation_type_id=be_constants.CIRCULATION_TYPE_STANDARD,
                service_id=service_id,
                circulation_state_id=be_constants.CIRCULATION_STATE_WORKING,
                deadline_date=today,
                reason="",
            )
            for service_id in service_suggestions
        ]

        ProposalActivation.objects.bulk_create(proposals)

    def _update_rejected_instance(self, instance):
        caluma_api = CalumaApi()

        source_case = caluma_api.get_source_document_value(
            caluma_api.get_main_document(instance), "case"
        )
        source_instance = (
            models.Instance.objects.get(
                pk=source_case.meta.get("camac-instance-id", None)
            )
            if source_case
            else None
        )

        if (
            source_instance
            and source_instance.instance_state.name == "rejected"
            and not caluma_api.is_modification(instance)
        ):
            source_instance.previous_instance_state = source_instance.instance_state
            source_instance.instance_state = models.InstanceState.objects.get(
                name="finished"
            )
            source_instance.save()

            workflow_api.cancel_case(
                case=source_case, user=self.context["request"].caluma_info.context.user
            )

    @transaction.atomic
    def update(self, instance, validated_data):
        request_logger.info(f"Submitting instance {instance.pk}")

        case = workflow_models.Case.objects.get(
            **{"meta__camac-instance-id": self.instance.pk}
        )

        instance.previous_instance_state = instance.instance_state
        instance.instance_state = models.InstanceState.objects.get(name="subm")

        instance.save()

        if not instance.responsible_service(filter_type="municipality"):
            municipality = case.document.answers.get(question_id="gemeinde").value

            InstanceService.objects.create(
                instance=self.instance,
                service_id=int(municipality),
                active=1,
                activation_date=None,
            )

        self._generate_and_store_pdf(instance)
        self._set_submit_date(validated_data)
        self._create_history_entry(get_translations(gettext_noop("Dossier submitted")))
        self._create_answer_proposals(instance)
        self._update_rejected_instance(instance)

        work_item = workflow_models.WorkItem.objects.filter(
            **{
                "task_id__in": settings.APPLICATION["CALUMA"]["SUBMIT_TASKS"],
                "status": workflow_models.WorkItem.STATUS_READY,
                "case__meta__camac-instance-id": self.instance.pk,
            }
        ).first()

        if work_item:
            workflow_api.complete_work_item(
                work_item=work_item,
                user=self.context["request"].caluma_info.context.user,
            )

        instance_submitted.send(
            sender=self.__class__,
            instance=instance,
            user_pk=self.context["request"].user.pk,
            group_pk=self.context["request"].group.pk,
        )

        # send out emails upon submission
        for notification_config in settings.APPLICATION["NOTIFICATIONS"]["SUBMIT"]:
            self._notify_submit(**notification_config)

        return instance


class CalumaInstanceReportSerializer(CalumaInstanceSubmitSerializer):
    """Handle submission of "SB1" form."""

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.previous_instance_state = instance.instance_state
        instance.instance_state = models.InstanceState.objects.get(name="sb2")

        instance.save()

        work_item = workflow_models.WorkItem.objects.filter(
            **{
                "task_id": settings.APPLICATION["CALUMA"]["REPORT_TASK"],
                "status": workflow_models.WorkItem.STATUS_READY,
                "case__meta__camac-instance-id": self.instance.pk,
            }
        ).first()

        if work_item:
            workflow_api.complete_work_item(
                work_item=work_item,
                user=self.context["request"].caluma_info.context.user,
            )

        # generate and submit pdf
        self._generate_and_store_pdf(instance, "sb1")

        self._create_history_entry(get_translations(gettext_noop("SB1 submitted")))

        sb1_submitted.send(
            sender=self.__class__,
            instance=instance,
            user_pk=self.context["request"].user.pk,
            group_pk=self.context["request"].group.pk,
        )

        # send out emails upon submission
        for notification_config in settings.APPLICATION["NOTIFICATIONS"]["REPORT"]:
            self._notify_submit(**notification_config)

        return instance


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

    def _sync_circulations(self, from_service, to_service):
        if self.instance.instance_state.name not in [
            "circulation_init",
            "circulation",
            "coordination",
        ]:
            return

        for circulation in self.instance.circulations.all():
            # Get all activations where the old responsible service invited
            # it's own sub services or the invited service is the newly
            # responsible service
            deleted_activations = circulation.activations.filter(
                Q(service_parent=from_service, service__service_parent=from_service)
                | Q(service=to_service)
            )

            if deleted_activations.exists():
                # Delete said activations
                deleted_activations.delete()
                # Sync circulation with caluma
                CalumaApi().sync_circulation(
                    circulation, self.context["request"].caluma_info.context.user
                )

            if not circulation.activations.exists():
                # Delete empty circulation
                circulation.delete()

                continue

            # Set service parent of remaining activations to the newly responsible service
            circulation.activations.filter(service_parent=from_service).update(
                service_parent=to_service
            )

        # Set service parent of circulations to the newly responsible service
        self.instance.circulations.filter(service=from_service).update(
            service=to_service
        )

    def _sync_with_caluma(self, from_service, to_service):
        CalumaApi().reassign_work_items(
            self.instance.pk, from_service.pk, to_service.pk
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
        texts = get_translations(
            gettext_noop("Changed responsible service to: %(service)s")
        )

        history = models.HistoryEntry.objects.create(
            instance=self.instance,
            created_at=timezone.now(),
            user=self.context["request"].user,
            history_type=HistoryActionConfig.HISTORY_TYPE_STATUS,
        )

        for (language, text) in texts:
            service_t = to_service.trans.filter(language=language).first()
            name = service_t.name if service_t else to_service.name

            models.HistoryEntryT.objects.create(
                history_entry=history,
                title=_(text % {"service": name}),
                language=language,
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
        self._sync_circulations(from_service, to_service)
        self._sync_with_caluma(from_service, to_service)
        self._send_notification()
        self._trigger_ech_message()
        self._add_history_entry(to_service)

        return instance

    class Meta:
        resource_name = "instance-change-responsible-services"


class CalumaInstanceFinalizeSerializer(CalumaInstanceSubmitSerializer):
    """Handle submission of "SB2" form."""

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.previous_instance_state = instance.instance_state
        instance.instance_state = models.InstanceState.objects.get(name="conclusion")

        instance.save()

        work_item = workflow_models.WorkItem.objects.filter(
            **{
                "task_id": settings.APPLICATION["CALUMA"]["FINALIZE_TASK"],
                "status": workflow_models.WorkItem.STATUS_READY,
                "case__meta__camac-instance-id": self.instance.pk,
            }
        ).first()

        if work_item:
            workflow_api.complete_work_item(
                work_item=work_item,
                user=self.context["request"].caluma_info.context.user,
            )

        # generate and submit pdf
        self._generate_and_store_pdf(instance, "sb2")

        self._create_history_entry(get_translations(gettext_noop("SB2 submitted")))

        sb2_submitted.send(
            sender=self.__class__,
            instance=instance,
            user_pk=self.context["request"].user.pk,
            group_pk=self.context["request"].group.pk,
        )

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

    def validate(self, data):
        location = self.instance.location
        if location is None:
            raise exceptions.ValidationError(_("No location assigned."))

        data["identifier"] = generate_identifier(self.instance)
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
        permission = perms.get(group.role.name, "applicant")

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

    visibility = serializers.ChoiceField(choices=models.JournalEntry.VISIBILITIES)

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
