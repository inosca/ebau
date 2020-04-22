from logging import getLogger
from uuid import uuid4

from caluma.caluma_form import (
    models as caluma_form_models,
    validators as caluma_form_validators,
)
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db import transaction
from django.db.models import Max
from django.utils import timezone
from django.utils.translation import gettext as _, gettext_noop
from rest_framework import exceptions
from rest_framework_json_api import relations, serializers

from camac.caluma.api import CalumaApi, CalumaInfo
from camac.caluma.extensions.data_sources import Municipalities
from camac.constants import kt_bern as constants
from camac.core.models import (
    Answer,
    InstanceLocation,
    InstanceService,
    Journal,
    JournalT,
    ProposalActivation,
)
from camac.core.serializers import MultilingualSerializer
from camac.core.translations import get_translations
from camac.document.models import AttachmentSection
from camac.echbern.signals import instance_submitted, sb1_submitted, sb2_submitted
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

    def get_is_applicant(self, obj):
        return obj.involved_applicants.filter(
            invitee=self.context["request"].user
        ).exists()

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
    permissions = serializers.SerializerMethodField()

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

    def get_is_paper(self, instance):
        return CalumaApi().is_paper(instance)

    def get_is_modification(self, instance):
        return CalumaApi().is_modification(instance)

    def get_caluma_form(self, instance):
        return CalumaApi().get_form_slug(instance)

    def get_active_service(self, instance):
        return instance.active_service

    def get_responsible_service_users(self, instance):
        return get_user_model().objects.filter(
            pk__in=instance.responsible_services.filter(
                service=self.context["request"].group.service
            ).values("responsible_user")
        )

    def get_public_status(self, instance):
        # TODO Instead of a new field, we should actually modify the values of instance_state
        STATUS_MAP = {
            constants.INSTANCE_STATE_NEW: constants.PUBLIC_INSTANCE_STATE_CREATING,
            constants.INSTANCE_STATE_EBAU_NUMMER_VERGEBEN: constants.PUBLIC_INSTANCE_STATE_RECEIVING,
            constants.INSTANCE_STATE_DOSSIERPRUEFUNG: constants.PUBLIC_INSTANCE_STATE_COMMUNAL,
            constants.INSTANCE_STATE_CORRECTION_IN_PROGRESS: constants.PUBLIC_INSTANCE_STATE_COMMUNAL,
            constants.INSTANCE_STATE_KOORDINATION: constants.PUBLIC_INSTANCE_STATE_IN_PROGRESS,
            constants.INSTANCE_STATE_VERFAHRENSPROGRAMM_INIT: constants.PUBLIC_INSTANCE_STATE_IN_PROGRESS,
            constants.INSTANCE_STATE_ZIRKULATION: constants.PUBLIC_INSTANCE_STATE_IN_PROGRESS,
            constants.INSTANCE_STATE_REJECTED: constants.PUBLIC_INSTANCE_STATE_REJECTED,
            constants.INSTANCE_STATE_CORRECTED: constants.PUBLIC_INSTANCE_STATE_CORRECTED,
            constants.INSTANCE_STATE_SB1: constants.PUBLIC_INSTANCE_STATE_SB1,
            constants.INSTANCE_STATE_SB2: constants.PUBLIC_INSTANCE_STATE_SB2,
            constants.INSTANCE_STATE_TO_BE_FINISHED: constants.PUBLIC_INSTANCE_STATE_FINISHED,
            constants.INSTANCE_STATE_FINISHED: constants.PUBLIC_INSTANCE_STATE_FINISHED,
            constants.INSTANCE_STATE_ARCHIVED: constants.PUBLIC_INSTANCE_STATE_ARCHIVED,
            constants.INSTANCE_STATE_DONE: constants.PUBLIC_INSTANCE_STATE_DONE,
        }

        return STATUS_MAP.get(
            instance.instance_state_id, constants.PUBLIC_INSTANCE_STATE_CREATING
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
            permissions.update(["write", "write-meta"])

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
            permissions.update(["read", "write-meta"])

        if state == "correction":
            permissions.add("write")

        if (
            is_paper
            and service_group in get_paper_settings()["ALLOWED_SERVICE_GROUPS"]
            and role in get_paper_settings()["ALLOWED_ROLES"]
            and state == "new"
        ):
            permissions.update(["read", "write", "write-meta"])

        return permissions

    def _get_main_form_permissions_for_support(self, instance):
        return set(["read", "write", "write-meta"])

    @permission_aware
    def _get_sb1_form_permissions(self, instance):
        state = instance.instance_state.name
        permissions = set()

        if state in ["sb1", "sb2", "conclusion"]:
            permissions.add("read")

        if state == "sb1":
            permissions.update(["write", "write-meta"])

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
            permissions.update(["read", "write", "write-meta"])

        return permissions

    def _get_sb1_form_permissions_for_support(self, instance):
        return ["read", "write", "write-meta"]

    @permission_aware
    def _get_sb2_form_permissions(self, instance):
        state = instance.instance_state.name
        permissions = set()

        if state in ["sb2", "conclusion"]:
            permissions.add("read")

        if state == "sb2":
            permissions.update(["write", "write-meta"])

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
            permissions.update(["read", "write", "write-meta"])

        return permissions

    def _get_sb2_form_permissions_for_support(self, instance):
        return ["read", "write", "write-meta"]

    @permission_aware
    def _get_nfd_form_permissions(self, instance):
        return CalumaApi().get_nfd_form_permissions(instance)

    def _get_nfd_form_permissions_for_service(self, instance):
        return set()

    def _get_nfd_form_permissions_for_municipality(self, instance):
        permissions = set(["write", "write-meta"])

        if CalumaApi().is_paper(instance):
            permissions.update(CalumaApi().get_nfd_form_permissions(instance))

        return permissions

    def _get_nfd_form_permissions_for_support(self, instance):
        return set(["read", "write", "write-meta"])

    def get_permissions(self, instance):
        return {
            form: sorted(getattr(self, f"_get_{form}_form_permissions")(instance))
            for form in settings.APPLICATION.get("CALUMA", {}).get(
                "FORM_PERMISSIONS", set()
            )
        }

    def validate(self, data):
        form_slug = self.initial_data.get("caluma_form")

        if form_slug and not CalumaApi().is_main_form(form_slug):  # pragma: no cover
            raise exceptions.ValidationError(
                _("Passed caluma form is not a main form: %(form)s")
                % {"form": form_slug}
            )

        return data

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
            is_modification = False
            is_paper = (
                group.service  # group needs to have a service
                and group.service.service_group.pk
                in get_paper_settings()["ALLOWED_SERVICE_GROUPS"]
                and group.role.pk in get_paper_settings()["ALLOWED_ROLES"]
            )

        instance = super().create(validated_data)

        caluma_documents = {}

        for form_slug in [caluma_form, "sb1", "sb2", "nfd"]:
            # copy the caluma document of provided instance
            if source_instance and form_slug == caluma_form:
                source_document_pk = caluma_api.get_document_by_form_slug(
                    source_instance, form_slug
                )

                document = caluma_api.copy_document(
                    source_document_pk,
                    exclude_form_slugs=(
                        ["6-dokumente", "7-bestaetigung", "8-freigabequittung"]
                        if is_modification
                        else ["8-freigabequittung"]
                    ),
                    meta={"camac-instance-id": instance.pk},
                )
            # or create a new document if no source instance is provided
            else:
                document = caluma_api.create_document(
                    form_slug, meta={"camac-instance-id": instance.pk}
                )

            caluma_api.update_or_create_answer(
                document.pk,
                "papierdossier",
                "papierdossier-ja" if is_paper else "papierdossier-nein",
            )

            if form_slug == caluma_form:
                caluma_api.update_or_create_answer(
                    document.pk,
                    "projektaenderung",
                    "projektaenderung-ja"
                    if is_modification
                    else "projektaenderung-nein",
                )

            caluma_documents[form_slug] = document

        if is_paper:
            # remove the previously created applicants
            instance.involved_applicants.all().delete()

            # prefill municipality question if possible
            value = str(group.service.pk)
            source = Municipalities()
            main_document = caluma_documents[caluma_form]

            if source.validate_answer_value(value, main_document, "gemeinde", None):
                caluma_api.update_or_create_answer(main_document.pk, "gemeinde", value)

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
        )
        read_only_fields = InstanceSerializer.Meta.read_only_fields + (
            "caluma_form",
            "is_paper",
            "is_modification",
            "public_status",
            "active_service",
            "responsible_service_users",
            "involved_applicants",
        )
        meta_fields = InstanceSerializer.Meta.meta_fields + ("permissions",)


def copy_table_answer(
    instance,
    source_question,
    target_form,
    target_answer,
    source_form=None,
    source_question_fallback=None,
):
    if source_form is None:
        source_document_id = CalumaApi().get_main_document(instance)
    else:
        source_document_id = CalumaApi().get_document_by_form_slug(
            instance, source_form
        )

    target_document_id = CalumaApi().get_document_by_form_slug(instance, target_form)
    table_answers = caluma_form_models.Answer.objects.filter(
        document_id=source_document_id, question_id=source_question
    )

    if not target_document_id:
        return

    if not table_answers:
        table_answers = caluma_form_models.Answer.objects.filter(
            document_id=source_document_id, question_id=source_question_fallback
        )

    if not table_answers:
        return

    sb_table_answer = caluma_form_models.Answer.objects.create(
        document_id=target_document_id, question_id=target_answer
    )

    for row in table_answers[0].documents.all():
        sb_row = CalumaApi().copy_document(
            row.id,
            family=caluma_form_models.Document.objects.get(
                id=target_document_id
            ).family,
        )
        sb_table_answer.documents.add(sb_row)


class CalumaInstanceSubmitSerializer(CalumaInstanceSerializer):
    def _create_journal_entry(self, texts):
        journal = Journal.objects.create(
            instance=self.instance,
            mode="auto",
            created=timezone.now(),
            user=self.context["request"].user,
        )
        for (language, text) in texts:
            JournalT.objects.create(journal=journal, text=text, language=language)

    def _notify_submit(self, template_slug, recipient_types):
        """Send notification email."""
        send_mail(
            template_slug,
            self.context,
            recipient_types=recipient_types,
            instance={"type": "instances", "id": self.instance.pk},
        )

    def _set_submit_date(self, validated_data):
        document_pk = validated_data["caluma_document"]
        submit_date = timezone.now().strftime(SUBMIT_DATE_FORMAT)
        changed = CalumaApi().set_submit_date(document_pk, submit_date)

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

    def _validate_document_validity(self, document_id):
        caluma_doc = caluma_form_models.Document.objects.get(pk=document_id)
        validator = caluma_form_validators.DocumentValidator()

        caluma_info = CalumaInfo(self.context["request"])
        validator.validate(caluma_doc, info=caluma_info)

    def validate(self, data):
        data["caluma_document"] = CalumaApi().get_main_document(self.instance)

        if not data["caluma_document"]:  # pragma: no cover
            raise exceptions.ValidationError(
                _("Could not find caluma main document for instance %(instance)s")
                % {"instance": self.instance.pk}
            )

        data["caluma_municipality"] = CalumaApi().get_municipality(self.instance)
        if not data["caluma_municipality"]:  # pragma: no cover
            raise exceptions.ValidationError(
                _(
                    "Could not find municipality in caluma document for instance %(instance)s"
                )
                % {"instance": self.instance.pk}
            )

        self._validate_document_validity(data["caluma_document"])

        return data

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
                circulation_type_id=constants.CIRCULATION_TYPE_STANDARD,
                service_id=service_id,
                circulation_state_id=constants.CIRCULATION_STATE_WORKING,
                deadline_date=today,
                reason="",
            )
            for service_id in service_suggestions
        ]

        ProposalActivation.objects.bulk_create(proposals)

    def _update_rejected_instance(self, instance):
        caluma_api = CalumaApi()

        source_meta = caluma_api.get_source_document_value(
            caluma_api.get_main_document(instance), "meta"
        )
        source_instance = (
            models.Instance.objects.get(pk=source_meta.get("camac-instance-id", None))
            if source_meta
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

    @transaction.atomic
    def update(self, instance, validated_data):
        request_logger.info(f"Submitting instance {instance.pk}")

        instance.previous_instance_state = instance.instance_state
        instance.instance_state = models.InstanceState.objects.get(name="subm")

        instance.save()

        if not instance.active_service:
            InstanceService.objects.create(
                instance=self.instance,
                service_id=int(validated_data.get("caluma_municipality")),
                active=1,
                activation_date=None,
            )

        self._generate_and_store_pdf(instance)
        self._set_submit_date(validated_data)
        self._create_journal_entry(get_translations(gettext_noop("Dossier submitted")))
        self._create_answer_proposals(instance)
        self._update_rejected_instance(instance)

        copy_table_answer(
            instance,
            source_question="personalien-sb",
            target_form="sb1",
            target_answer="personalien-sb1-sb2",
            source_question_fallback="personalien-gesuchstellerin",
        )

        # send out emails upon submission
        for notification_config in settings.APPLICATION["NOTIFICATIONS"]["SUBMIT"]:
            self._notify_submit(**notification_config)

        instance_submitted.send(
            sender=self.__class__,
            instance=instance,
            user_pk=self.context["request"].user.pk,
            group_pk=self.context["request"].group.pk,
        )

        return instance


class CalumaInstanceReportSerializer(CalumaInstanceSubmitSerializer):
    """Handle submission of "SB1" form."""

    def validate(self, data):
        data["caluma_document"] = CalumaApi().get_document_by_form_slug(
            self.instance, "sb1"
        )

        if not data["caluma_document"]:  # pragma: no cover
            raise exceptions.ValidationError(
                _("Could not find caluma `sb1` document for instance %(instance)s")
                % {"instance": self.instance.pk}
            )

        self._validate_document_validity(data["caluma_document"])

        return data

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.previous_instance_state = instance.instance_state
        instance.instance_state = models.InstanceState.objects.get(name="sb2")

        instance.save()

        # generate and submit pdf
        self._generate_and_store_pdf(instance, "sb1")

        self._create_journal_entry(get_translations(gettext_noop("SB1 submitted")))

        copy_table_answer(
            instance,
            source_question="personalien-sb1-sb2",
            target_form="sb2",
            target_answer="personalien-sb1-sb2",
            source_form="sb1",
        )

        # send out emails upon submission
        for notification_config in settings.APPLICATION["NOTIFICATIONS"]["REPORT"]:
            self._notify_submit(**notification_config)

        sb1_submitted.send(
            sender=self.__class__,
            instance=instance,
            user_pk=self.context["request"].user.pk,
            group_pk=self.context["request"].group.pk,
        )

        return instance


class CalumaInstanceFinalizeSerializer(CalumaInstanceSubmitSerializer):
    """Handle submission of "SB2" form."""

    def validate(self, data):
        data["caluma_document"] = CalumaApi().get_document_by_form_slug(
            self.instance, "sb2"
        )

        if not data["caluma_document"]:  # pragma: no cover
            raise exceptions.ValidationError(
                _("Could not find caluma `sb2` document for instance %(instance)s")
                % {"instance": self.instance.pk}
            )

        self._validate_document_validity(data["caluma_document"])

        return data

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.previous_instance_state = instance.instance_state
        instance.instance_state = models.InstanceState.objects.get(name="conclusion")

        instance.save()

        # generate and submit pdf
        self._generate_and_store_pdf(instance, "sb2")

        self._create_journal_entry(get_translations(gettext_noop("SB2 submitted")))

        # send out emails upon submission
        for notification_config in settings.APPLICATION["NOTIFICATIONS"]["FINALIZE"]:
            self._notify_submit(**notification_config)

        sb2_submitted.send(
            sender=self.__class__,
            instance=instance,
            user_pk=self.context["request"].user.pk,
            group_pk=self.context["request"].group.pk,
        )

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
