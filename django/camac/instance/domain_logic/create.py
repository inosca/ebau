from __future__ import annotations

import json
from typing import TYPE_CHECKING
from uuid import uuid4

from alexandria.core.models import Document
from caluma.caluma_form import api as form_api, models as form_models
from caluma.caluma_workflow import api as workflow_api, models as workflow_models
from django.conf import settings
from django.core.files.base import ContentFile
from django.db.models import CharField, Q
from django.db.models.fields.json import KeyTextTransform
from django.db.models.functions import Cast
from django.utils import timezone
from django.utils.text import slugify
from rest_framework.exceptions import ValidationError

from camac.caluma.api import CalumaApi
from camac.caluma.extensions.data_sources import Municipalities
from camac.constants import kt_uri as ur_constants
from camac.core.models import InstanceLocation, InstanceService
from camac.core.utils import (
    canton_aware,
    generate_dossier_nr,
    generate_sort_key,
    generate_special_id,
)
from camac.instance import models
from camac.instance.master_data import MasterData
from camac.instance.models import Instance, InstanceGroup
from camac.permissions.events.core import Trigger
from camac.settings.modules.instance_copy import (
    AllowListedCopyFormConfig,
    DenyListedCopyFormConfig,
)
from camac.settings.utils import is_module_enabled
from camac.timelines.models import FormTimeline
from camac.user.models import Service
from camac.user.permissions import permission_aware

if TYPE_CHECKING:
    from caluma.caluma_user.models import BaseUser

    from camac.settings.modules.instance_copy import InstanceCopyConfig

SUBMIT_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"

caluma_api = CalumaApi()


def link_instances(first, second):
    if not first.instance_group and not second.instance_group:
        instance_group = InstanceGroup.objects.create()

        first.instance_group = instance_group
        first.save()

        second.instance_group = instance_group
        second.save()
    elif first.instance_group and second.instance_group:
        instances_with_same_group = Instance.objects.filter(
            instance_group=second.instance_group
        )
        instances_with_same_group.update(instance_group=first.instance_group)
    elif first.instance_group:
        second.instance_group = first.instance_group
        second.save()
    elif second.instance_group:
        first.instance_group = second.instance_group
        first.save()


class CreateInstanceLogic:
    @classmethod
    @permission_aware
    def validate(cls, data, group):
        if data.get("generate_identifier"):
            raise ValidationError("You don't have permission to generate an identifier")
        return data

    @classmethod
    def validate_for_municipality(cls, data, group):
        if settings.APPLICATION["CALUMA"].get("USE_LOCATION"):
            if (
                data.get("location", False)
                and data["location"] not in group.locations.all()
            ):
                raise ValidationError(
                    "Provided location is not present in group locations"
                )

            data["location"] = data.get("location", group.locations.first())

        return data

    @classmethod
    def validate_for_coordination(cls, data, group):
        """Coordination role is allowed to generate identifiers."""
        return data

    @staticmethod
    def update_instance_location(instance):
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

    @staticmethod
    def _get_year(year: int = None) -> int:
        full_year = timezone.now().year if year is None else year
        year = full_year % 100
        return year

    @staticmethod
    def _get_name_from_camac_form(instance: Instance) -> str:
        # Camac form is only used in UR and SZ (deprecated)
        name = instance.form.name
        meta = models.FormField.objects.filter(instance=instance, name="meta").first()
        if meta:
            meta_value = json.loads(meta.value)
            name = meta_value["formType"]
        return name

    @staticmethod
    def _get_identifier_start(instance: Instance, name: str, prefix: str = None) -> str:
        abbreviations = settings.APPLICATION.get("INSTANCE_IDENTIFIER_FORM_ABBR", {})

        if name in abbreviations:
            identifier_start = abbreviations[name]
        elif settings.APPLICATION.get("SHORT_DOSSIER_NUMBER", False):
            identifier_start = (
                prefix
                and f"{prefix}-{str(instance.location.communal_federal_number)[-2:]}"
            ) or str(instance.location.communal_federal_number)[-2:]
        else:
            identifier_start = (
                prefix and f"{prefix}-{instance.location.communal_federal_number}"
            ) or str(instance.location.communal_federal_number)
        return identifier_start

    @staticmethod
    def _get_last_identifier(name: str, start: str) -> str:
        if settings.APPLICATION["CALUMA"].get("SAVE_DOSSIER_NUMBER_IN_CALUMA") or (
            name in settings.APPLICATION.get("CALUMA_INSTANCE_FORMS", [])
        ):
            last_identifier = (
                workflow_models.Case.objects.filter(
                    **{"meta__dossier-number__startswith": start}
                )
                .annotate(
                    dossier_nr=Cast(
                        KeyTextTransform("dossier-number", "meta"), CharField()
                    )
                )
                .order_by("-dossier_nr")
                .values_list("dossier_nr", flat=True)
                .first()
            )
        else:
            last_identifier = (
                models.Instance.objects.filter(identifier__startswith=start)
                .order_by("-identifier")
                .values_list("identifier", flat=True)
                .first()
            )
        return last_identifier

    @classmethod
    @canton_aware
    def generate_identifier(cls, instance: Instance, year: int = None, **kwargs) -> str:
        return generate_dossier_nr(instance, year or timezone.now().year)

    @classmethod
    def generate_identifier_ur(
        cls,
        instance: Instance,
        year: int = None,
        prefix: str = None,
        seq_zero_padding: int = 3,
    ) -> str:
        """
        Build identifier for Kt. Uri instance.

        Format for normal forms:
        two last digits of communal location number
        year in two digits
        zero-padded sequence
        Example: 11-18-001

        Format for special forms:
        two letter abbreviation of form
        year in two digits
        zero-padded sequence
        Example: AV-20-014

        prefix: Sets first element to prefix
        CAVEAT: if an instance uses form abbreviation the prefix param is ignored.

        Uniqueness is not verified here in order to avoid coupling.
        """

        separator = "-"

        identifier = instance.identifier

        if not identifier:
            year = CreateInstanceLogic._get_year(year)

            name = CreateInstanceLogic._get_name_from_camac_form(instance)
            identifier_start = CreateInstanceLogic._get_identifier_start(
                instance, name, prefix
            )

            start = separator.join([str(identifier_start), str(year).zfill(2)])
            last_identifier = CreateInstanceLogic._get_last_identifier(name, start)

            last_position = (
                last_identifier and int(last_identifier.split(separator)[-1])
            ) or 0

            identifier = separator.join(
                [
                    str(identifier_start),
                    str(year).zfill(2),
                    str(last_position + 1).zfill(seq_zero_padding),
                ]
            )

        return identifier

    @classmethod
    def generate_identifier_sz(
        cls,
        instance: Instance,
        year: int = None,
        prefix: str = None,
        seq_zero_padding: int = 3,
    ) -> str:
        """
        Build identifier for Kt. Schwyz instance.

        Same as generic generate_instance with one exception:
        For internal instances service_id is added to
        the second position and the seq_zero_padding is set to 4.
        Example: IG-6-23-0014
        """
        separator = "-"

        identifier = instance.identifier
        if not identifier:
            year = CreateInstanceLogic._get_year(year)

            name = CreateInstanceLogic._get_name_from_camac_form(instance)
            identifier_start = CreateInstanceLogic._get_identifier_start(
                instance, name, prefix
            )

            if name in settings.APPLICATION.get("INTERNAL_INSTANCE_FORMS", []):
                service_id = instance.group.service_id
                start = separator.join(
                    [str(identifier_start), str(service_id), str(year).zfill(2)]
                )
                last_identifier = CreateInstanceLogic._get_last_identifier(name, start)

                last_position = (
                    last_identifier and int(last_identifier.split(separator)[-1])
                ) or 0

                seq_zero_padding = 4
                identifier = separator.join(
                    [
                        str(identifier_start),
                        str(service_id),
                        str(year).zfill(2),
                        str(last_position + 1).zfill(seq_zero_padding),
                    ]
                )

            else:
                start = separator.join([str(identifier_start), str(year).zfill(2)])
                last_identifier = CreateInstanceLogic._get_last_identifier(name, start)

                last_position = (
                    last_identifier and int(last_identifier.split(separator)[-1])
                ) or 0

                identifier = separator.join(
                    [
                        str(identifier_start),
                        str(year).zfill(2),
                        str(last_position + 1).zfill(seq_zero_padding),
                    ]
                )

        return identifier

    @classmethod
    def generate_identifier_so(cls, instance: Instance, year: int = None) -> str:
        authority = instance.responsible_service()

        if not authority:
            raise ValidationError("Instance does not have a responsible service")

        if authority.service_group.name == "canton":
            # If the canton is the authority, we use the external identifier of
            # the selected municipality
            authority = Service.objects.get(
                pk=instance.case.document.answers.get(question_id="gemeinde").value
            )

        if not authority.external_identifier:
            raise ValidationError(
                "Responsible service does not have an external identifier"
            )

        return generate_special_id(
            "dossier-number",
            instance,
            f"{authority.external_identifier}-{year or timezone.now().year}-",
        )

    @staticmethod
    def copy_caluma_data_allowlisted(
        config: AllowListedCopyFormConfig,
        source_document: form_models.Document,
        target_instance: models.Instance,
        user: BaseUser | None,
    ) -> form_models.Document:
        target_document = target_instance.case.document

        if config.link_source_document:
            target_document.source = source_document
            target_document.save()

        for answer in source_document.answers.filter(
            question_id__in=config.simple_questions
        ):
            form_api.save_answer(
                answer.question,
                target_document,
                user,
                answer.date
                if answer.question.type == form_models.Question.TYPE_DATE
                else answer.value,
            )

        for slug in config.table_questions:
            caluma_api.copy_table_answer(
                slug,
                slug,
                source_document,
                target_document,
            )

        for entry in config.conditional_table_questions:
            answer = source_document.answers.filter(
                question_id__in=entry.condition_questions,
                value__isnull=False,
            ).first()

            source_slugs = (
                entry.sources_by_answer.get(
                    answer.value, entry.default_source_questions
                )
                if answer
                else entry.default_source_questions
            )

            # source_slugs is a list in order to account for versioning of the sources
            # copy_table_answer only copies from sources with answers
            for source_slug in source_slugs:
                caluma_api.copy_table_answer(
                    source_slug,
                    entry.target_question,
                    source_document,
                    target_document,
                )

        return target_document

    @staticmethod
    def copy_caluma_data_denylisted(
        config: DenyListedCopyFormConfig,
        source_document: form_models.Document,
        target_instance: models.Instance,
    ) -> form_models.Document:
        current_document = target_instance.case.document
        target_document = caluma_api.copy_document(
            source_document.pk,
            exclude_form_slugs=config.exclude_forms,
        )

        for answer in target_document.answers.filter(
            question_id__in=config.exclude_questions
        ):
            if answer.question.type == form_models.Question.TYPE_TABLE:
                for row_document in answer.documents.all():
                    row_document.delete()
            answer.delete()

        target_document.form = current_document.form
        target_document.save()

        target_instance.case.document = target_document
        target_instance.case.save()
        current_document.delete()

        return target_document

    @staticmethod
    def copy_caluma_data(
        instance: models.Instance,
        source_instance: models.Instance,
        copy_type: str,
        user: BaseUser | None,
    ) -> None:
        target_instance = instance
        instance_copy_settings: InstanceCopyConfig = settings.INSTANCE_COPY
        config = instance_copy_settings.get_copy_config(copy_type)
        source_document = source_instance.case.document

        if isinstance(config, AllowListedCopyFormConfig):
            target_document = CreateInstanceLogic.copy_caluma_data_allowlisted(
                config,
                source_document,
                target_instance,
                user,
            )

        elif isinstance(config, DenyListedCopyFormConfig):
            target_document = CreateInstanceLogic.copy_caluma_data_denylisted(
                config,
                source_document,
                target_instance,
            )
        else:  # pragma: no cover
            raise ValidationError(f"Invalid copy config type {type(config)}")

        if instance_id_slug := config.instance_id_slug:
            form_api.save_answer(
                form_models.Question.objects.get(pk=instance_id_slug),
                target_document,
                user,
                int(source_instance.pk),
            )

        if special_id_slug := config.special_id_slug:
            dossier_number = caluma_api.get_dossier_number(source_instance)
            form_api.save_answer(
                form_models.Question.objects.get(pk=special_id_slug),
                target_document,
                user,
                dossier_number,
            )

        # BE-specific: assign same eBau number for extend validity,
        # either when doing a full copy of an extend validity instance or
        # when doing an extend validity copy type.
        if (
            copy_type == "full" and caluma_api.is_extend_validity(source_instance)
        ) or copy_type == "extend_validity":
            CreateInstanceLogic.copy_ebau_number(source_instance, instance)

    @staticmethod
    def initialize_caluma(
        instance,
        source_instance,
        copy_type,
        is_modification,
        is_paper,
        group,
        user,
        lead,
    ):
        if source_instance:
            CreateInstanceLogic.copy_caluma_data(
                instance,
                source_instance,
                copy_type,
                user,
            )

        document = instance.case.document
        caluma_api.update_or_create_answer(
            document,
            "is-paper",
            "is-paper-yes" if is_paper else "is-paper-no",
            user,
        )

        if settings.APPLICATION["CALUMA"].get("SYNC_FORM_TYPE"):
            form_type = ur_constants.CALUMA_FORM_MAPPING.get(instance.form.pk)
            if not form_type:
                raise RuntimeError(
                    f"Unmapped form {instance.form.name} (ID {instance.form.pk})"
                )  # pragma: no cover

            caluma_api.update_or_create_answer(
                document,
                "form-type",
                "form-type-" + form_type,
                user,
            )

        if settings.APPLICATION["CALUMA"].get("HAS_PROJECT_CHANGE"):
            caluma_api.update_or_create_answer(
                document,
                "projektaenderung",
                "projektaenderung-ja" if is_modification else "projektaenderung-nein",
                user,
                # Not all forms have this question (Vorabklärungen for example)
                skip_on_error=True,
            )

        if settings.APPLICATION["CALUMA"].get("USE_LOCATION") and instance.location:
            caluma_api.update_or_create_answer(
                document,
                "municipality",
                instance.location.communal_federal_number,
                user,
            )

            # Synchronize the 'Leitbehörde' for display in the dashboard
            if lead:
                caluma_api.update_or_create_answer(
                    document,
                    "leitbehoerde",
                    str(lead),
                    user,
                )

        if is_paper:
            # prefill municipality question if possible
            value = str(group.service.pk)
            source = Municipalities()
            municipality_question = MasterData.get_question_slug("municipality_slug")

            if source.validate_answer_value(
                value, document, municipality_question, None, None
            ):
                caluma_api.update_or_create_answer(
                    document,
                    municipality_question,
                    value,
                    user,
                )

    @classmethod
    @canton_aware
    def copy_attachments(
        cls,
        source,
        target,
        skip_exported_form_attachment=False,
        is_modification=False,
        copy_attachments_from=None,
    ):
        copy_attachments_from = copy_attachments_from or []
        if settings.APPLICATION["DOCUMENT_BACKEND"] == "alexandria":
            CreateInstanceLogic.copy_alexandria_attachments(
                source,
                target,
                skip_exported_form_attachment=skip_exported_form_attachment,
                is_modification=is_modification,
            )
        else:
            CreateInstanceLogic.copy_camac_attachments(
                source,
                target,
                skip_exported_form_attachment=skip_exported_form_attachment,
                copy_attachments_from=copy_attachments_from,
            )

    @staticmethod
    def copy_alexandria_attachments(
        source,
        target,
        skip_exported_form_attachment=False,
        is_modification=False,
    ):
        if is_modification and not settings.ALEXANDRIA.get(
            "INSTANCE_COPY_ON_MODIFICATION", False
        ):
            return

        categories = settings.ALEXANDRIA.get("INSTANCE_COPY_CATEGORIES", [])
        alexandria_documents = Document.objects.filter(
            Q(
                **{
                    "metainfo__camac-instance-id": str(source.pk),
                }
            )
            & (Q(category_id__in=categories) | Q(category__parent_id__in=categories))
        )
        if skip_exported_form_attachment:
            alexandria_documents = alexandria_documents.exclude(
                metainfo__has_key="system-generated"
            )

        for document in alexandria_documents:
            new_document = document.clone()
            new_document.metainfo["camac-instance-id"] = str(target.pk)
            new_document.instance_document.instance_id = target.pk
            new_document.instance_document.save()
            if new_document.metainfo.get("caluma-document-id"):
                new_document.metainfo["caluma-document-id"] = str(
                    target.case.document.pk
                )
            new_document.save()

    @staticmethod
    def copy_camac_attachments(
        source,
        target,
        skip_exported_form_attachment=False,
        copy_attachments_from=None,
    ):
        copy_attachments_from = copy_attachments_from or []
        attachments = source.attachments.all()

        # UR only: when we copy dossiers from php, we only want to
        # copy attachments from the applicant attachment section.
        if copy_attachments_from:
            attachments = attachments.filter(
                attachment_sections__attachment_section_id__in=copy_attachments_from
            )

        if skip_exported_form_attachment:
            form_attachment_name = (
                slugify(f"{source.pk}-{source.case.document.form.name}") + ".pdf"
            )
            attachments = source.attachments.filter(~Q(name=form_attachment_name))

        for attachment in attachments:
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

    @staticmethod
    def copy_ebau_number(source_instance, target_instance):
        ebau_number = caluma_api.get_ebau_number(source_instance)
        target_instance.case.meta["ebau-number"] = ebau_number
        target_instance.case.save()

    @staticmethod
    def copy_all_applicants(source, target):
        for applicant in source.involved_applicants.all():
            new_applicant = target.involved_applicants.create(
                invitee=applicant.invitee,
                created=timezone.now(),
                user=applicant.user,
                email=applicant.email,
                role=applicant.role,
            )
            Trigger.applicant_added(
                request=None, instance=target, applicant=new_applicant
            )

    @staticmethod
    def setup_applicants(
        instance, source_instance, copy_type, camac_user, is_modification
    ):
        # TODO (Kt. BE): appeal, rejection appeal, copies created by support
        # should have all previous applicants copied instead of adding the currently
        # logged in user (from a municipality or support) as applicant
        if source_instance and copy_type == "full" and not is_modification:
            CreateInstanceLogic.copy_all_applicants(source_instance, instance)
        else:
            new_applicant = instance.involved_applicants.create(
                user=camac_user,
                invitee=camac_user,
                created=timezone.now(),
                email=camac_user.email,
            )
            Trigger.applicant_added(
                request=None, instance=instance, applicant=new_applicant
            )

    @staticmethod
    def handle_archive_forms_ur(data):
        """Make sure archive dossiers in Kt. UR start in the state 'old'."""

        # UR is still actively using CAMAC forms for business logic (deprecated)
        form = data.get("form")
        if form and form.pk in settings.APPLICATION.get("ARCHIVE_FORMS", []):
            data["instance_state"] = models.InstanceState.objects.get(name="old")
        return data

    @staticmethod
    def initialize_camac(
        instance,
        source_instance,
        copy_type,
        camac_user,
        group,
        is_modification,
        is_paper,
        skip_exported_form_attachment,
        copy_attachments_from,
    ):
        if is_paper:
            # create instance service for permissions
            InstanceService.objects.create(
                instance=instance,
                service_id=group.service.pk,
                active=1,
                activation_date=None,
            )

        if not is_paper:
            CreateInstanceLogic.setup_applicants(
                instance, source_instance, copy_type, camac_user, is_modification
            )

        if source_instance:
            if settings.APPLICATION.get("LINK_INSTANCES_ON_COPY"):
                link_instances(instance, source_instance)  # pragma: no cover

            instance_copy_settings: InstanceCopyConfig = settings.INSTANCE_COPY
            copy_config = instance_copy_settings.get_copy_config(copy_type)

            if copy_config.copy_attachments:
                CreateInstanceLogic.copy_attachments(
                    source_instance,
                    instance,
                    skip_exported_form_attachment,
                    is_modification,
                    copy_attachments_from,
                )

            if is_module_enabled("TIMELINES"):
                was_rejected = (
                    is_module_enabled("REJECTION")
                    and source_instance.instance_state.name
                    == settings.REJECTION["INSTANCE_STATE"]
                )
                FormTimeline.objects.add_instance_timeline(
                    instance=instance,
                    timeline_type=FormTimeline.Type.PROJECT_CHANGE.value
                    if not was_rejected
                    else FormTimeline.Type.SUBMIT_AFTER_REJECTION.value,
                    start_date=timezone.now(),
                )

    @staticmethod
    def create(
        data,
        caluma_user,
        camac_user,
        group,
        lead=None,
        is_modification=False,
        is_appeal=False,
        is_rejected_appeal=False,
        is_copy=False,
        is_paper=False,
        caluma_form=None,
        source_instance=None,
        start_caluma=True,
        workflow_slug=None,
        skip_exported_form_attachment=False,
        copy_attachments_from=None,
    ):
        """Create an instance.

        We assume that the caller can be trusted, so basic validations
        (e.g. if user is allowed to create a copy of the given source instance)
        are skipped here and performed in the serializer instead.
        """
        copy_attachments_from = copy_attachments_from or []
        copy_type = data.pop("copy_type", None)

        if source_instance:
            copy_type = copy_type or "full"

            # todo: we want to get rid of `copy_instance` hack first, after that it will
            # be easier to refactor the call sites and correctly specify the copy type.
            # For now we use the `exclude_confirmation_answers` argument.
            exclude_confirmation_answers = (
                is_modification
                and not is_appeal
                and not is_rejected_appeal
                and not is_copy
            )
            instance_copy_settings: InstanceCopyConfig = settings.INSTANCE_COPY
            if (
                copy_type == "full"
                and exclude_confirmation_answers
                and instance_copy_settings.has_copy_config("full_without_confirmation")
            ):
                copy_type = "full_without_confirmation"

        generate_identifier = data.pop("generate_identifier", None)

        data = CreateInstanceLogic.handle_archive_forms_ur(data)

        year = data.pop("year", None)

        if (
            settings.APPLICATION["CALUMA"].get("USE_LOCATION") and source_instance
        ):  # pragma: no cover
            data["location"] = source_instance.location

        instance = Instance.objects.create(**data)

        if settings.APPLICATION["CALUMA"].get("USE_LOCATION"):  # pragma: no cover
            CreateInstanceLogic.update_instance_location(instance)

        allowed_workflows = workflow_models.Workflow.objects.filter(
            Q(allow_all_forms=True)
            | Q(allow_forms__in=[caluma_form])
            | Q(allow_forms__slug__regex=rf"^{caluma_form}-v\d+$")
        )

        workflow = (
            allowed_workflows.filter(pk=workflow_slug).first()
            if workflow_slug
            else allowed_workflows.first()
        )
        if workflow is None:  # pragma: todo cover
            raise ValidationError(
                f"The workflow {workflow_slug} does not allow the form {caluma_form}"
            )

        case_meta = {"camac-instance-id": instance.pk}

        if generate_identifier:
            # Give dossier a unique dossier number
            identifier = CreateInstanceLogic.generate_identifier(instance, year)
            case_meta["dossier-number"] = identifier
            case_meta["dossier-number-sort"] = generate_sort_key(identifier)

        case = workflow_api.start_case(
            workflow=workflow,
            form=caluma_form and form_models.Form.objects.get(pk=caluma_form),
            user=caluma_user,
            meta=case_meta,
            context={"instance": instance.pk},
        )

        instance.case = case
        instance.save()

        if start_caluma:
            CreateInstanceLogic.initialize_caluma(
                instance,
                source_instance,
                copy_type,
                is_modification,
                is_paper,
                group,
                caluma_user,
                lead,
            )

        CreateInstanceLogic.initialize_camac(
            instance,
            source_instance,
            copy_type,
            camac_user,
            group,
            is_modification,
            is_paper,
            skip_exported_form_attachment,
            copy_attachments_from,
        )

        Trigger.instance_created(None, instance)

        return instance
