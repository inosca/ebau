import json
from uuid import uuid4

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
from camac.core.utils import canton_aware, generate_dossier_nr
from camac.instance.models import Instance, InstanceGroup
from camac.user.permissions import permission_aware

from . import models

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
    def _get_name(instance: Instance) -> str:
        name = instance.form.name
        meta = models.FormField.objects.filter(instance=instance, name="meta").first()
        if meta:
            meta_value = json.loads(meta.value)
            name = meta_value["formType"]
        return name

    @staticmethod
    def _get_identifier_start(instance: Instance, name: str, prefix: str = None) -> str:
        abbreviations = settings.APPLICATION.get("INSTANCE_IDENTIFIER_FORM_ABBR", {})

        if name in abbreviations.keys():
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
    def generate_identifier(
        cls,
        instance: Instance,
        year: int = None,
        prefix: str = None,
        seq_zero_padding: int = 3,
    ) -> str:
        """
        Build identifier for instance.

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

            name = CreateInstanceLogic._get_name(instance)
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
        Example: IG-6-23-014

        """
        separator = "-"

        identifier = instance.identifier
        if not identifier:
            year = CreateInstanceLogic._get_year(year)

            name = CreateInstanceLogic._get_name(instance)
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
    def generate_identifier_gr(cls, instance: Instance) -> str:
        return generate_dossier_nr(timezone.now().year)

    @classmethod
    def generate_identifier_so(cls, instance: Instance) -> str:  # pragma: no cover
        return generate_dossier_nr(timezone.now().year)

    @staticmethod
    def initialize_caluma(
        instance,
        source_instance,
        case,
        is_modification,
        is_paper,
        group,
        user,
        lead,
    ):
        if source_instance:
            old_document = case.document
            new_document = caluma_api.copy_document(
                source_instance.case.document.pk,
                exclude_form_slugs=(
                    ["7-bestaetigung", "8-freigabequittung"]
                    if is_modification
                    else ["8-freigabequittung"]
                ),
            )
            new_document.form = old_document.form
            new_document.save()

            case.document = new_document
            case.save()
            old_document.delete()

        caluma_api.update_or_create_answer(
            case.document,
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
                case.document,
                "form-type",
                "form-type-" + form_type,
                user,
            )

        if settings.APPLICATION["CALUMA"].get("HAS_PROJECT_CHANGE"):
            caluma_api.update_or_create_answer(
                case.document,
                "projektaenderung",
                "projektaenderung-ja" if is_modification else "projektaenderung-nein",
                user,
            )

        if settings.APPLICATION["CALUMA"].get("USE_LOCATION") and instance.location:
            caluma_api.update_or_create_answer(
                case.document,
                "municipality",
                instance.location.communal_federal_number,
                user,
            )

            # Synchronize the 'Leitbehörde' for display in the dashboard
            if lead:
                caluma_api.update_or_create_answer(
                    case.document,
                    "leitbehoerde",
                    str(lead),
                    user,
                )

        if group.pk == settings.APPLICATION.get("PORTAL_GROUP", False):
            # TODO pre-fill user data into personal data table
            pass

        if is_paper:
            # prefill municipality question if possible
            value = str(group.service.pk)
            source = Municipalities()
            municipality_slug = settings.APPLICATION["MASTER_DATA"]["municipality"][1]

            if source.validate_answer_value(
                value, case.document, municipality_slug, None, None
            ):
                caluma_api.update_or_create_answer(
                    case.document,
                    municipality_slug,
                    value,
                    user,
                )

    @staticmethod
    def copy_applicants(source, target):
        for applicant in source.involved_applicants.all():
            target.involved_applicants.update_or_create(
                invitee=applicant.invitee,
                defaults={
                    "created": timezone.now(),
                    "user": applicant.user,
                    "email": applicant.email,
                },
            )

    @staticmethod
    def copy_attachments(source, target, skip_exported_form_attachment=False):
        attachments = source.attachments.all()

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
    def copy_ebau_number(source_instance, target_instance, case):
        ebau_number = caluma_api.get_ebau_number(source_instance)
        case.meta["ebau-number"] = ebau_number
        case.save()

    @staticmethod
    def copy_extend_validity_answers(source, target, user):
        old_document = source.case.document
        new_document = target.case.document

        for answer in old_document.answers.filter(
            question_id__in=settings.APPLICATION["CALUMA"].get(
                "EXTEND_VALIDITY_COPY_QUESTIONS", []
            )
        ):
            form_api.save_answer(
                answer.question,
                new_document,
                user,
                answer.value,
            )

        for slug in settings.APPLICATION["CALUMA"].get(
            "EXTEND_VALIDITY_COPY_TABLE_QUESTIONS", []
        ):
            caluma_api.copy_table_answer(slug, slug, old_document, new_document)

        form_api.save_answer(
            form_models.Question.objects.get(pk="dossiernummer"),
            new_document,
            user,
            int(source.pk),
        )

    @staticmethod
    def initialize_camac(
        instance,
        source_instance,
        group,
        is_modification,
        is_paper,
        extend_validity_for,
        case,
        user,
        skip_exported_form_attachment,
    ):
        if is_paper:
            # remove the previously created applicants
            instance.involved_applicants.all().delete()

            # create instance service for permissions
            InstanceService.objects.create(
                instance=instance,
                service_id=group.service.pk,
                active=1,
                activation_date=None,
            )

        if source_instance:
            if settings.APPLICATION.get("LINK_INSTANCES_ON_COPY"):
                link_instances(instance, source_instance)  # pragma: no cover
            CreateInstanceLogic.copy_attachments(
                source_instance, instance, skip_exported_form_attachment
            )
            if not is_modification:
                CreateInstanceLogic.copy_applicants(source_instance, instance)
                instance.form = source_instance.form
                instance.save()
        elif extend_validity_for:
            extend_validity_instance = models.Instance.objects.get(
                pk=extend_validity_for
            )
            CreateInstanceLogic.copy_ebau_number(
                extend_validity_instance, instance, case
            )
            CreateInstanceLogic.copy_extend_validity_answers(
                extend_validity_instance, instance, user
            )

    @staticmethod
    def create(
        data,
        caluma_user,
        camac_user,
        group,
        lead=None,
        is_modification=False,
        is_paper=False,
        caluma_form=None,
        source_instance=None,
        start_caluma=True,
        workflow_slug=None,
        skip_exported_form_attachment=False,
    ):
        """Create an instance.

        We assume that the caller can be trusted, so basic validations
        (e.g. if user is allowed to create a copy of the given source instance)
        are skipped here and performed in the serializer instead.
        """
        extend_validity_for = data.pop("extend_validity_for", None)
        generate_identifier = data.pop("generate_identifier", None)

        form = data.get("form")
        if form and form.pk in settings.APPLICATION.get("ARCHIVE_FORMS", []):
            data["instance_state"] = models.InstanceState.objects.get(name="old")

        year = data.pop("year", None)

        if (
            settings.APPLICATION["CALUMA"].get("USE_LOCATION") and source_instance
        ):  # pragma: no cover
            data["location"] = source_instance.location

        instance = Instance.objects.create(**data)

        instance.involved_applicants.create(
            user=camac_user,
            invitee=camac_user,
            created=timezone.now(),
            email=camac_user.email,
        )

        if settings.APPLICATION["CALUMA"].get("USE_LOCATION"):  # pragma: no cover
            CreateInstanceLogic.update_instance_location(instance)

        allowed_workflows = workflow_models.Workflow.objects.filter(
            Q(allow_forms__in=[caluma_form]) | Q(allow_all_forms=True)
        )

        workflow = (
            allowed_workflows.filter(pk=workflow_slug).first()
            if workflow_slug
            else allowed_workflows.first()
        )
        if workflow is None:  # pragma: no cover  TODO: cover
            raise ValidationError(
                f"The workflow {workflow_slug} does not allow the form {caluma_form.slug}"
            )

        case_meta = {"camac-instance-id": instance.pk}

        if generate_identifier:
            # Give dossier a unique dossier number
            case_meta["dossier-number"] = CreateInstanceLogic.generate_identifier(
                instance, year
            )

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
                case,
                is_modification,
                is_paper,
                group,
                caluma_user,
                lead,
            )

        CreateInstanceLogic.initialize_camac(
            instance,
            source_instance,
            group,
            is_modification,
            is_paper,
            extend_validity_for,
            case,
            caluma_user,
            skip_exported_form_attachment,
        )

        return instance
