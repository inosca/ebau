import json
import re
from importlib import import_module
from os.path import splitext

import requests
from alexandria.core import models as alexandria_models
from alexandria.core.models import (
    File as AlexandriaFile,
)
from caluma.caluma_form.models import Document, Question
from caluma.caluma_form.validators import CustomValidationError, DocumentValidator
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import OuterRef
from django.utils.text import slugify
from django.utils.timezone import get_current_timezone, localtime
from django.utils.translation import get_language, gettext as _
from rest_framework import exceptions, status
from rest_framework.authentication import get_authorization_header

from camac.caluma.api import CalumaApi
from camac.instance.master_data import MasterData
from camac.instance.models import Instance
from camac.instance.placeholders.utils import (
    enrich_personal_data,
    format_gis_center_coordinates,
    get_person_name,
)
from camac.user.models import Service
from camac.utils import build_url, clean_join, get_dict_item

caluma_api = CalumaApi()


def find_in_result(slug, node):
    for item in node:
        if item.get("slug") == slug:
            return item

        result = find_in_result(slug, item.get("children", []))

        if result:
            return result

    return None


def get_form_config():
    return settings.DMS.get("FORM", {})


def get_form_type_key(form_slug):
    for key, config in get_form_config().items():
        if form_slug in config.get("forms", []):
            return key

    return form_slug


def get_form_type_config(form_slug):
    return get_form_config().get(get_form_type_key(form_slug), {})


def get_tag_header(instance, current_service):
    if settings.TAGS and settings.TAGS.use_legacy_tags:
        tags = instance.tags.filter(service=current_service)
    else:
        tags = instance.keywords.filter(service=current_service)
    return ", ".join(tags.values_list("name", flat=True)) if tags.exists() else None


def get_authority(instance):
    return instance.responsible_service(filter_type="municipality")


def get_header_authority(instance):
    service = get_authority(instance)

    return service.get_name() if service else None


def get_header_responsible(instance, current_service):
    responsible_service = instance.responsible_services.filter(
        service=current_service
    ).first()

    return (
        responsible_service.responsible_user.get_full_name()
        if responsible_service
        else None
    )


def get_header_labels():
    return {
        "addressHeaderLabel": _("Address"),
        "plotsHeaderLabel": _("Plots"),
        "applicantHeaderLabel": _("Applicant"),
        "landownerHeaderLabel": _("Landowner"),
        "projectAuthorHeaderLabel": _("Project Author"),
        "tagHeaderLabel": _("Keywords"),
        "municipalityHeaderLabel": _("Municipality"),
        "authorityHeaderLabel": _("Authority"),
        "responsibleHeaderLabel": _("Responsible"),
        "inputDateHeaderLabel": _("Input date"),
        "descriptionHeaderLabel": _("Description"),
        "modificationHeaderLabel": _("Modification"),
    }


def graceful_get(master_data, prop, default=None):
    if not get_dict_item(
        settings.MASTER_DATA, f"CONFIG.{prop}", default=False
    ):  # pragma: no cover
        return default

    value = getattr(master_data, prop, default)

    return value


class DMSHandler:
    def get_files(self, instance):
        files = []

        master_data = MasterData(instance.case)
        municipality = Service.objects.filter(pk=master_data.municipality_slug).first()

        if municipality and municipality.logo:
            files.append(("files", ("municipality_logo", municipality.logo.file.file)))

        situationsplan_file = self._get_situationsplan(instance)
        if situationsplan_file:
            files.append(
                (
                    "files",
                    (
                        "situationsplan",
                        situationsplan_file.content.file,
                    ),
                )
            )

        return files

    def get_meta_data(self, instance, document, service):
        master_data = MasterData(instance.case)
        timezone = get_current_timezone()

        generated_at = localtime()
        created_at = document.created_at.astimezone(timezone)
        modified_at = (
            document.modified_content_at.astimezone(timezone)
            if document.modified_content_at
            else created_at
        )

        data = {
            "caseId": instance.pk,
            "caseType": str(instance.case.document.form.name),
            "formType": (
                str(document.form.name)
                if instance.case.document.pk != document.pk
                else None
            ),
            "dossierNr": graceful_get(master_data, "dossier_number"),
            "municipality": graceful_get(master_data, "municipality_name"),
            "signatureSectionTitle": _("Signatures"),
            "signatureTitle": _("Signature"),
            "signatureMetadata": _("Place and date"),
            "generatedAt": _("Generated %(date)s at %(time)s")
            % {
                "date": generated_at.strftime("%d.%m.%Y"),
                "time": generated_at.strftime("%H:%M"),
            },
            "modifiedAt": _("Modified %(date)s at %(time)s")
            % {
                "date": modified_at.strftime("%d.%m.%Y"),
                "time": modified_at.strftime("%H:%M"),
            },
            "createdAt": _("Created %(date)s at %(time)s")
            % {
                "date": created_at.strftime("%d.%m.%Y"),
                "time": created_at.strftime("%H:%M"),
            },
            "uploadedAt": _("Uploaded %(date)s at %(time)s")
            % {
                "date": generated_at.strftime("%d.%m.%Y"),
                "time": generated_at.strftime("%H:%M"),
            },
            "gisCoordinatesCenter": format_gis_center_coordinates(
                graceful_get(master_data, "gis_coordinates", default=None)
            ),
        }

        if settings.DMS.get("ADD_ADDRESS_DATA"):
            if municipality := get_authority(instance):
                address_data = {
                    "addressRecipient": municipality.get_trans_attr("name"),
                    "addressStreet": municipality.address,
                    "addressCityZip": clean_join(
                        municipality.zip, municipality.get_trans_attr("city")
                    ),
                }
                data.update(address_data)

        if settings.DMS.get("ADD_HEADER_DATA"):
            header_data = {
                "addressHeader": clean_join(
                    clean_join(
                        graceful_get(master_data, "street"),
                        graceful_get(master_data, "street_number"),
                    ),
                    clean_join(
                        graceful_get(master_data, "city"),
                        graceful_get(master_data, "zip"),
                    ),
                    separator=", ",
                ),
                "plotsHeader": clean_join(
                    *[
                        obj["plot_number"]
                        for obj in graceful_get(master_data, "plot_data", default=[])
                    ],
                    separator=", ",
                ),
                # all applicant names as comma-separated string
                "applicantHeader": clean_join(
                    *[
                        get_person_name(applicant)
                        for applicant in graceful_get(
                            master_data, "applicants", default=[]
                        )
                    ],
                    separator=", ",
                ),
                # all applicants as structured data
                "applicants": enrich_personal_data(
                    graceful_get(master_data, "applicants")
                ),
                "landowners": enrich_personal_data(
                    graceful_get(master_data, "landowners")
                ),
                "projectAuthors": enrich_personal_data(
                    graceful_get(master_data, "project_authors")
                ),
                "municipalityServiceContent": graceful_get(
                    master_data, "municipality_service_content"
                ),
                "municipalityHeader": graceful_get(master_data, "municipality_name"),
                "tagHeader": get_tag_header(instance, service),
                "authorityHeader": get_header_authority(instance),
                "responsibleHeader": get_header_responsible(instance, service),
                "inputDateHeader": graceful_get(master_data, "submit_date"),
                "paperInputDateHeader": graceful_get(master_data, "paper_submit_date"),
                "descriptionHeader": graceful_get(master_data, "proposal"),
                "modificationHeader": graceful_get(
                    master_data, "description_modification"
                ),
                "coordEast": clean_join(
                    *[
                        obj["coord_east"]
                        for obj in graceful_get(master_data, "plot_data", default=[])
                        if "coord_east" in obj
                    ],
                    separator=", ",
                ),
                "coordNorth": clean_join(
                    *[
                        obj["coord_north"]
                        for obj in graceful_get(master_data, "plot_data", default=[])
                        if "coord_north" in obj
                    ],
                    separator=", ",
                ),
            }

            data.update(get_header_labels())
            data.update(header_data)

        return data

    def prepare_documents(self, instance, for_additional_demand=None):
        if settings.APPLICATION["DOCUMENT_BACKEND"] == "camac-ng":  # pragma: no cover
            # not implemented
            return []

        categories = settings.DMS.get("ALEXANDRIA_DOCUMENT_CATEGORIES", [])

        if for_additional_demand:
            filters = {"metainfo__caluma-document-id": for_additional_demand}
        else:
            filters = {"category_id__in": categories}

        documents = (
            alexandria_models.Document.objects.filter(
                **filters,
                instance_document__instance=instance,
            )
            .annotate(
                checksum=alexandria_models.File.objects.filter(
                    document=OuterRef("pk"),
                    variant=alexandria_models.File.Variant.ORIGINAL,
                )
                .order_by("-created_at")
                .values("checksum")[:1]
            )
            .exclude(metainfo__has_key="system-generated")
            .order_by("-created_at")
            .values("title", "created_at", "checksum")
        )

        timezone = get_current_timezone()

        return [
            {
                "filename": str(document["title"]),
                "date": document["created_at"]
                .astimezone(timezone)
                .strftime("%d.%m.%Y"),
                "time": document["created_at"].astimezone(timezone).strftime("%H:%M"),
                "checksum": document["checksum"],
            }
            for document in documents
        ]

    def get_instance_and_document(self, instance_id, form_slug=None, document_id=None):
        use_root_document = not document_id and not form_slug

        instance = Instance.objects.select_related(
            "case", "case__document", "case__document__form"
        ).get(pk=instance_id)

        if use_root_document:
            document = instance.case.document
        else:
            _filter = (
                {"pk": document_id}
                if document_id
                else {
                    "work_item__case__instance__pk": instance_id,
                    "form_id": form_slug,
                }
            )

            try:
                document = Document.objects.select_related("form").get(**_filter)
            except (Document.DoesNotExist, Document.MultipleObjectsReturned):
                raise exceptions.ValidationError(
                    _(
                        "None or multiple caluma Documents found for instance: %(instance)s"
                    )
                    % {"instance": instance_id}
                )

        return (instance, document)

    def get_data(self, instance, document, user, service, for_additional_demand=None):
        visitor = DMSVisitor(document, instance, user)

        if get_form_type_config(document.form.slug).get(
            "check_validity_for_draft", False
        ):
            is_draft = not visitor.is_valid()
        else:
            is_draft = not caluma_api.is_submitted(instance, document)

        return {
            **self.get_meta_data(instance, document, service),
            "draft": _("Draft") if is_draft else "",
            "sections": visitor.build_form_structure(),
            "documents": self.prepare_documents(instance, for_additional_demand),
        }

    def get_filename(self, instance_id, form_name, template, for_additional_demand):
        filename_parts = [instance_id, form_name]
        if filename_addition := settings.DMS.get("FILENAME_ADDITION_MAPPING", {}).get(
            template
        ):
            filename_parts.append(filename_addition)

        if for_additional_demand is not None:
            filename_parts.append(_("Additional demand"))

        filename = slugify("-".join([str(p) for p in filename_parts]))

        return f"{filename}.pdf"

    def generate_pdf(
        self,
        instance_id,
        request,
        form_slug=None,
        document_id=None,
        template=None,
        for_additional_demand=None,
    ):
        instance, document = self.get_instance_and_document(
            instance_id, form_slug, document_id
        )

        if template is None:
            template = get_form_type_config(document.form.slug).get("template")

        if template is None:  # pragma: no cover
            raise exceptions.ValidationError(
                _("No template specified for form '%(form_slug)s'.")
                % {"form_slug": document.form.slug}
            )

        # merge pdf and store as attachment
        auth = get_authorization_header(request)
        dms_client = DMSClient(auth)
        pdf = dms_client.merge(
            self.get_data(
                instance,
                document,
                request.caluma_info.context.user,
                request.group.service,
                for_additional_demand=for_additional_demand,
            ),
            template,
            self.get_files(instance),
            add_headers={"x-camac-group": str(request.group.pk)},
        )

        filename = self.get_filename(
            instance_id,
            str(document.form.name),
            template,
            for_additional_demand,
        )

        _file = ContentFile(pdf, filename)
        _file.content_type = "application/pdf"

        return _file

    def convert_docx_to_pdf(self, request, attachment):
        auth = get_authorization_header(request)
        dms_client = DMSClient(auth)
        pdf_binary = dms_client.convert_docx_to_pdf(attachment.path.file)

        filename = splitext(attachment.name)[0]

        _file = ContentFile(pdf_binary, f"{filename}.pdf")
        _file.content_type = "application/pdf"

        return _file

    def _get_situationsplan(self, instance):
        if settings.APPLICATION_NAME != "kt_gr":
            return

        return (
            AlexandriaFile.objects.filter(
                document__instance_document__instance=instance,
                document__category_id="system",
                document__metainfo__contains={"situationsplan": "true"},
                variant=AlexandriaFile.Variant.ORIGINAL,
            )
            .order_by("-created_at")
            .first()
        )


class DMSClient:
    def __init__(self, auth_token, url=settings.DOCUMENT_MERGE_SERVICE_URL):
        self.auth_token = auth_token
        self.url = url

    def _make_dms_request(self, url, **kwargs):
        response = requests.post(
            url,
            data=kwargs.get("data", None),
            headers=kwargs.get("headers", None),
            files=kwargs.get("files", None),
        )

        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            raise exceptions.AuthenticationFailed(_("Signature has expired."))

        response.raise_for_status()

        return response.content

    def merge(self, data, template, files=[], convert="pdf", add_headers={}):
        headers = {"authorization": self.auth_token, **add_headers}
        url = build_url(self.url, f"/template/{template}/merge", trailing=True)

        return self._make_dms_request(
            url,
            headers=headers,
            data={
                "convert": convert,
                "data": json.dumps(data, cls=DjangoJSONEncoder),
            },
            files=files,
        )

    def convert_docx_to_pdf(self, file):
        headers = {"authorization": self.auth_token}
        url = build_url(self.url, "/convert", trailing=False)

        return self._make_dms_request(
            url,
            files={"file": file},
            data={"target_format": "pdf"},
            headers=headers,
        )


class DMSVisitor:
    # TODO: refactor to use new caluma structure code instead of "manually"
    # iterating over the form structure here
    def __init__(self, document, instance, user):
        self.root_document = document
        self.user = user

        self.validator = DocumentValidator()
        self.validation_context = self.validator.get_validation_context(document)
        self.data_source_context = {"instanceId": instance.pk}

        self.template_type = get_form_type_key(document.form.slug)
        self.exclude_slugs = get_form_type_config(self.template_type).get(
            "exclude_slugs", []
        )

    def build_form_structure(self):
        result = [
            self.collect_field(field)
            for field in self.validation_context.children()
            if self._should_include_field(field)
        ]
        receipt_page = self.prepare_receipt_page(result)

        if receipt_page:
            result.append(receipt_page)
        return result

    def _should_include_field(self, field):
        if field.question and field.slug() in self.exclude_slugs:
            return False

        # TODO: Would this be a good idea?
        # if field.question.meta.get("widgetOverride") == "cf-field/input/hidden":
        #     return False

        if not self._is_non_static_or_static_title(field):
            return False

        if (
            field.question.type == Question.TYPE_FORM and not field.children()
        ):  # pragma: no cover
            return False

        if field.is_hidden():
            return False

        if field.question.is_archived and not field.answer:  # pragma: no cover
            return False

        # Some special cases
        if self._should_exclude_mp_form_stuff(field):
            return False

        return True

    def _should_exclude_mp_form_stuff(self, field):
        """Decide whether to exclude the MP form parts.

        In the "Materielle Prüfung" they only want the relevant questions
        rendered in the PDF export. The questions in that form (excluding
        those questions listed in the code below) consist of 3 parts
        (questions):

        * is XY relevant?
        * did XY pass?
        * remarks to XY

        Question 1 will be displayed if answered with "Yes". Questions 2
        and 3 will only be rendered if question 1 was answered with "Yes".
        """

        # NOTE: I'm inverting it here, so it becomes more understandable. This function
        # is called should *exclude*, whereas the caller is named should *include*

        if field.get_root().get_form().slug != "mp-form":
            # Not mp-form - none of our concern
            return False

        if (
            field.slug()
            not in [
                "mp-eigene-pruefgegenstaende",
                "mp-erforderliche-beilagen-vorhanden",
                "mp-welche-beilagen-fehlen",
            ]
            and field.question.type != Question.TYPE_FORM
        ):
            base_question_slug = re.sub(r"(-bemerkungen|-ergebnis)$", "", field.slug())
            base_answer_field = field.get_field(base_question_slug)
            if (
                not base_answer_field
                or not base_answer_field.get_value()
                or base_answer_field.get_value().endswith("-nein")
            ):
                return True

        if field.question.type == Question.TYPE_FORM:
            # If our sub-fields are all excluded, we can exclude this form as well.
            if all(
                self._should_exclude_mp_form_stuff(child) for child in field.children()
            ):
                return True

        if field.slug() == "mp-eigene-pruefgegenstaende" and not field.children():
            return True
        return False

    def collect_field(self, field, flatten=False):
        # Build up basic return value
        ret = {
            "label": str(
                field.question.meta.get("printLabel", {}).get(get_language(), None)
                or field.question.label
            ),
            "slug": field.slug(),
            "type": "".join(
                word.capitalize()
                for word in f"{field.question.type}_question".split("_")
            ),
        }

        # every field except root has a question
        match field.question.type:
            case Question.TYPE_TEXT | Question.TYPE_TEXTAREA | Question.TYPE_DATE:
                ret.update(self.collect_simple_field(field))
            case (
                Question.TYPE_FLOAT
                | Question.TYPE_INTEGER
                | Question.TYPE_CALCULATED_FLOAT
            ):
                ret.update(self.collect_number_field(field))
            case Question.TYPE_FORM:
                ret.update(self.collect_form_field(field, flatten=flatten))
            case Question.TYPE_CHOICE:
                ret.update(self.collect_choice_field(field, flatten=flatten))
            case Question.TYPE_TABLE:
                ret.update(self.collect_table_field(field))
            case Question.TYPE_STATIC:
                ret.update(self.collect_static_field(field))
            case Question.TYPE_MULTIPLE_CHOICE:
                ret.update(self.collect_multiple_choice_field(field, flatten=flatten))
            case Question.TYPE_DYNAMIC_CHOICE:
                ret.update(self.collect_dynamic_choice_field(field))
            case Question.TYPE_DYNAMIC_MULTIPLE_CHOICE:
                ret.update(self.collect_dynamic_multiple_choice_field(field))
            case other:  # pragma: no cover
                raise RuntimeError(f"Question type {other} not dealth with yet")
        return ret

    def collect_simple_field(self, field):
        return {"value": field.get_value()}

    def collect_form_field(self, field, flatten=False):
        children = [
            self.collect_field(f, flatten=flatten)
            for f in field.children()
            if self._should_include_field(f)
        ]

        return {"children": children}

    def is_valid(self):
        try:
            self.validator.validate(
                self.root_document,
                self.user,
                self.validation_context,
                self.data_source_context,
            )
            return True
        except CustomValidationError:
            return False

    def _is_non_static_or_static_title(self, field):
        if field.question.type != Question.TYPE_STATIC:
            # If the question is not static, we don't need to check whether it's
            # only a title or not
            return True

        return str(field.question.label) in str(field.question.static_content)

    def collect_table_field(self, field):
        return {
            "columns": [str(column.label) for column in field.get_column_questions()],
            "rows": [
                self.collect_form_field(subfield, flatten=True)["children"]
                for subfield in field.children()
            ],
        }

    def collect_choice_field(self, field, flatten=False, limit=None):
        # TODO: re-introducing the kwargs necessary?

        plain_value = field.get_value()

        # any non-archived options are possible. Also the selected one,
        # *even if it's actually archived*
        possible_options = [
            option
            for option in field.get_options()
            if option.slug == plain_value or not option.is_archived
        ]

        selected_option = next(
            (option for option in possible_options if option.slug == plain_value),
            None,
        )

        if not possible_options:  # pragma: no cover
            return {}

        if flatten:
            return {
                "type": "TextQuestion",
                "value": str(selected_option.label) if selected_option else "",
            }

        return {
            "choices": [
                {"label": str(option.label), "checked": option.slug == plain_value}
                for option in possible_options
            ][:limit]
        }

    def collect_multiple_choice_field(self, field, flatten=False, limit=None):
        answers = field.get_value()

        options = filter(
            lambda option: not option.is_archived or option.slug in answers,
            field.get_options(),
        )

        if flatten:  # pragma: no cover
            return {
                "type": "TextQuestion",
                "value": ", ".join(
                    [str(option.label) for option in options if option.slug in answers]
                ),
            }

        return {
            "choices": [
                {"label": str(option.label), "checked": option.slug in answers}
                for option in options
            ][:limit]
        }

    def _matching_dynamic_options(self, answer, document, question):
        data_source = getattr(
            import_module("camac.caluma.extensions.data_sources"), question.data_source
        )()
        if not isinstance(answer, list):
            answer = [answer]

        for ans in answer:
            value = data_source.validate_answer_value(
                ans, document, question, None, self.data_source_context
            )

            if isinstance(value, dict):
                yield value.get(get_language())

            # This can happen with old dynamic options which were saved before
            # the data source were multilingual

            yield value  # pragma: no cover

    def collect_dynamic_choice_field(self, field):
        ret = {"type": "TextQuestion", "value": None}
        value = next(
            self._matching_dynamic_options(
                field.get_value(), field.parent._document, field.question
            )
        )
        if value:
            ret["value"] = str(value)
        return ret

    def collect_dynamic_multiple_choice_field(self, field):
        answers = field.get_value()
        dynamic_options = [
            str(opt)
            for opt in self._matching_dynamic_options(
                answers, field.parent._document, field.question
            )
            if opt is not False
        ]
        return {"type": "TextQuestion", "value": ", ".join(dynamic_options)}

    def collect_static_field(self, field):
        return {"content": None}

    def collect_number_field(self, field, convert_to_int_if_bigger_than=1_000_000):
        value = field.get_value()

        if (
            value
            and settings.DMS.get("USE_NUMBER_SEPARATOR")
            and (
                field.slug() not in settings.DMS.get("NUMBER_SEPARATOR_EXCEPTIONS", [])
            )
        ):
            # To prevent scientific notation and numbers after the decimal point,
            # we check if a value is bigger than a threshold and then convert to int.
            # Here, it's used to prevent scientific notation on coordinates.
            if value > convert_to_int_if_bigger_than:
                value = round(value)
            value = f"{value:n}"

        return {"value": value}

    def prepare_receipt_page(self, result):
        if self.template_type not in [
            "baugesuch",
            "selbstdeklaration",
            "building-permit",
        ]:
            return

        config = {
            **get_form_config().get("_base", {}),
            **get_form_config().get(self.template_type, {}),
        }

        children = []
        for slug in config.get("people_sources", []):
            table = find_in_result(slug, result)

            if not table:
                continue

            children.append(
                {
                    "label": table["label"],
                    "people": [
                        {
                            config["people_names"][field["slug"]]: field["value"]
                            for field in row
                            if field["slug"] in config["people_names"]
                        }
                        for row in table["rows"]
                    ],
                    "type": "SignatureQuestion",
                }
            )

        return {
            "slug": "8-unterschriften",
            "label": _("Signatures"),
            "children": children,
            "type": "FormQuestion",
        }
