import json
import re
from importlib import import_module

import requests
from caluma.caluma_form.models import Document, Question
from caluma.caluma_form.validators import CustomValidationError, DocumentValidator
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.text import slugify
from django.utils.timezone import localtime
from django.utils.translation import get_language, gettext as _
from rest_framework import exceptions, status
from rest_framework.authentication import get_authorization_header

from camac.instance.master_data import MasterData
from camac.instance.models import Instance
from camac.instance.placeholders.utils import clean_join, get_person_name
from camac.instance.utils import build_document_prefetch_statements
from camac.utils import build_url


def find_in_result(slug, node):
    for item in node:
        if item.get("slug") == slug:
            return item

        result = find_in_result(slug, item.get("children", []))

        if result:
            return result

    return None


def get_form_config():
    return settings.APPLICATION.get("DOCUMENT_MERGE_SERVICE", {}).get("FORM", {})


def get_form_type_key(form_slug):
    for key, config in get_form_config().items():
        if form_slug in config.get("forms", []):
            return key

    return form_slug


def get_form_type_config(form_slug):
    return get_form_config().get(get_form_type_key(form_slug), {})


def get_header_tags(instance, current_service):
    tags = instance.tags.filter(service=current_service)

    return ", ".join(tags.values_list("name", flat=True)) if tags.exists() else None


def get_header_authority(instance):
    service = instance.responsible_service(filter_type="municipality")

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
        "tagHeaderLabel": _("Keywords"),
        "municipalityHeaderLabel": _("Municipality"),
        "authorityHeaderLabel": _("Authority"),
        "responsibleHeaderLabel": _("Responsible"),
        "inputDateHeaderLabel": _("Input date"),
        "descriptionHeaderLabel": _("Description"),
        "modificationHeaderLabel": _("Modification"),
    }


class DMSHandler:
    def get_meta_data(self, instance, document, service):
        master_data = MasterData(instance.case)
        created_at = localtime()

        data = {
            "caseId": instance.pk,
            "caseType": str(instance.case.document.form.name),
            "formType": str(document.form.name)
            if instance.case.document.pk != document.pk
            else None,
            "dossierNr": master_data.dossier_number,
            "municipality": master_data.municipality.get("label")
            if master_data.municipality
            else None,
            "signatureSectionTitle": _("Signatures"),
            "signatureTitle": _("Signature"),
            "signatureMetadata": _("Place and date"),
            "createdAt": _("Created %(date)s at %(time)s")
            % {
                "date": created_at.strftime("%d.%m.%Y"),
                "time": created_at.strftime("%H:%M"),
            },
        }

        if settings.APPLICATION.get("DOCUMENT_MERGE_SERVICE", {}).get(
            "ADD_HEADER_DATA"
        ):
            header_data = {
                "addressHeader": clean_join(
                    clean_join(
                        master_data.street,
                        master_data.street_number,
                    ),
                    master_data.city,
                    separator=", ",
                ),
                "plotsHeader": clean_join(
                    *[obj["plot_number"] for obj in master_data.plot_data],
                    separator=", ",
                )
                if master_data.plot_data
                else None,
                "applicantHeader": clean_join(
                    *[
                        get_person_name(applicant)
                        for applicant in master_data.applicants
                    ],
                    separator=", ",
                )
                if master_data.applicants
                else None,
                "municipalityHeader": master_data.municipality.get("label")
                if master_data.municipality
                else None,
                "tagHeader": get_header_tags(instance, service),
                "authorityHeader": get_header_authority(instance),
                "responsibleHeader": get_header_responsible(instance, service),
                "inputDateHeader": master_data.submit_date,
                "paperInputDateHeader": master_data.paper_submit_date,
                "descriptionHeader": master_data.proposal,
                "modificationHeader": master_data.description_modification,
            }

            data.update(get_header_labels())
            data.update(header_data)

        return data

    def get_instance_and_document(self, instance_id, form_slug=None, document_id=None):
        use_root_document = not document_id and not form_slug

        instance = (
            Instance.objects.select_related(
                "case", "case__document", "case__document__form"
            )
            .prefetch_related(
                *build_document_prefetch_statements(
                    prefix="case__document", prefetch_options=use_root_document
                ),
            )
            .get(pk=instance_id)
        )

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
                document = (
                    Document.objects.select_related("form")
                    .prefetch_related(
                        *build_document_prefetch_statements(prefetch_options=True)
                    )
                    .get(**_filter)
                )
            except (Document.DoesNotExist, Document.MultipleObjectsReturned):
                raise exceptions.ValidationError(
                    _(
                        "None or multiple caluma Documents found for instance: %(instance)s"
                    )
                    % {"instance": instance_id}
                )

        return (instance, document)

    def generate_pdf(self, instance_id, request, form_slug=None, document_id=None):
        instance, document = self.get_instance_and_document(
            instance_id, form_slug, document_id
        )

        template = get_form_type_config(document.form.slug).get("template")

        if template is None:  # pragma: no cover
            raise exceptions.ValidationError(
                _("No template specified for form '%(form_slug)s'.")
                % {"form_slug": document.form.slug}
            )

        # merge pdf and store as attachment
        auth = get_authorization_header(request)
        dms_client = DMSClient(auth)
        visitor = DMSVisitor(document, request.caluma_info.context.user)
        pdf = dms_client.merge(
            {
                **self.get_meta_data(
                    instance,
                    document,
                    request.group.service,
                ),
                "draft": "" if visitor.is_valid() else _("Draft"),
                "sections": visitor.visit(document),
            },
            template,
        )

        _file = ContentFile(
            pdf, slugify(f"{instance_id}-{document.form.name}") + ".pdf"
        )
        _file.content_type = "application/pdf"

        return _file


class DMSClient:
    def __init__(self, auth_token, url=settings.DOCUMENT_MERGE_SERVICE_URL):
        self.auth_token = auth_token
        self.url = url

    def merge(self, data, template, convert="pdf", add_headers={}):
        headers = {"authorization": self.auth_token, "content-type": "application/json"}
        headers.update(add_headers)
        url = build_url(self.url, f"/template/{template}/merge", trailing=True)

        response = requests.post(
            url,
            # use the django json encoder to correctly encode dates and
            # datetimes without manual parsing
            data=json.dumps({"convert": convert, "data": data}, cls=DjangoJSONEncoder),
            headers=headers,
        )

        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            raise exceptions.AuthenticationFailed(_("Signature has expired."))

        response.raise_for_status()

        return response.content


class DMSVisitor:
    def __init__(self, document, user):
        self.root_document = document
        self.user = user

        self.validator = DocumentValidator()
        self.validation_context = self.validator._validation_context(document)

        self.template_type = get_form_type_key(document.form.slug)
        self.exclude_slugs = get_form_type_config(self.template_type).get(
            "exclude_slugs", []
        )

    def is_valid(self):
        try:
            self.validator.validate(
                self.root_document, self.user, self.validation_context
            )
            return True
        except CustomValidationError:
            return False

    def visit(self, node):
        cls_name = type(node).__name__.lower()
        visit_func = getattr(self, f"_visit_{cls_name}")
        result = visit_func(node)

        receipt_page = self.prepare_receipt_page(result)

        if receipt_page:
            result.append(receipt_page)

        return result

    def _is_visible_question(self, node):
        return node.slug in self.validation_context["visible_questions"]

    def _is_static_title(self, node):
        return node.type != Question.TYPE_STATIC or str(node.label) in str(
            node.static_content
        )

    def _visit_document(self, node, form=None, flatten=False, **kwargs):
        if not form:
            form = node.form

        children = form.questions.all()

        visited_children = []
        for child in children:
            if (
                child.slug in self.exclude_slugs
                or not self._is_static_title(child)
                or not self._is_visible_question(child)
            ):
                continue

            if (
                node.form.slug == "mp-form"
                and child.type != Question.TYPE_FORM
                and child.slug
                not in [
                    "mp-eigene-pruefgegenstaende",
                    "mp-erforderliche-beilagen-vorhanden",
                    "mp-welche-beilagen-fehlen",
                ]
            ):
                base_question_slug = re.sub(
                    r"(-bemerkungen|-ergebnis)$", "", child.slug
                )
                base_answer = next(
                    filter(
                        lambda answer: answer.question_id == base_question_slug,
                        node.answers.all(),
                    ),
                    None,
                )
                if (
                    not base_answer
                    or not base_answer.value
                    or base_answer.value.endswith("-nein")
                ):
                    continue

            result = self._visit_question(
                child, parent_doc=node, flatten=flatten, **kwargs
            )

            if result is None:  # pragma: no cover
                continue

            if child.type == Question.TYPE_FORM and not len(
                result.get("children", [])
            ):  # pragma: no cover
                continue

            if child.slug == "mp-eigene-pruefgegenstaende" and not len(
                result.get("rows", [])
            ):
                continue

            visited_children.append(result)

        return visited_children

    def _visit_form_question(self, node, parent_doc=None, answer=None, **_):
        return {"children": self._visit_document(parent_doc, form=node.sub_form)}

    def _visit_table_question(self, node, parent_doc=None, answer=None, **_):
        return {
            "columns": [str(column.label) for column in node.row_form.questions.all()],
            "rows": [
                self._visit_document(
                    answer_document.document, form=node.row_form, flatten=True
                )
                for answer_document in answer.answerdocument_set.all()
            ]
            if answer
            else [],
        }

    def _visit_choice_question(
        self, node, parent_doc=None, answer=None, flatten=False, limit=None, **_
    ):
        answer = answer.value if answer else None
        options = filter(
            lambda option: not option.is_archived or option.slug == answer,
            node.options.all(),
        )

        if flatten:
            return {
                "type": "TextQuestion",
                "value": ", ".join(
                    [str(option.label) for option in options if option.slug == answer]
                ),
            }

        return {
            "choices": [
                {"label": str(option.label), "checked": option.slug == answer}
                for option in options
            ][:limit]
        }

    def _visit_multiple_choice_question(
        self, node, parent_doc=None, answer=None, flatten=False, limit=None, **_
    ):
        answers = answer.value if answer else []
        options = filter(
            lambda option: not option.is_archived or option.slug in answers,
            node.options.all(),
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
                ans, document, question, None, None
            )

            if isinstance(value, dict):
                yield value.get(get_language())

            # This can happen with old dynamic options which were saved before
            # the data source were multilingual

            yield value  # pragma: no cover

    def _visit_dynamic_choice_question(self, node, parent_doc=None, answer=None, **_):
        ret = {"type": "TextQuestion", "value": None}

        if answer:
            value = next(self._matching_dynamic_options(answer.value, parent_doc, node))

            if value:
                ret["value"] = str(value)

        return ret

    def _visit_dynamic_multiple_choice_question(
        self, node, parent_doc=None, answer=None, **_
    ):  # pragma: no cover
        answers = answer.value if answer else []
        dynamic_options = [
            do
            for do in self._matching_dynamic_options(answers, parent_doc, node)
            if do is not False
        ]
        return {"type": "TextQuestion", "value": ", ".join(dynamic_options)}

    def _visit_static_question(self, node, parent_doc=None, answer=None, **_):
        return {"content": str(answer.static_content) if answer else None}

    def _visit_simple_question(self, node, parent_doc=None, answer=None, **_):
        return {"value": answer.value if answer else None}

    def _visit_date_question(self, node, parent_doc=None, answer=None, **_):
        return {"value": answer.date if answer and answer.date else None}

    def _visit_question(self, node, parent_doc=None, flatten=False):

        ret = {
            "label": str(node.label),
            "slug": node.slug,
            "type": "".join(
                word.capitalize() for word in f"{node.type}_question".split("_")
            ),
        }

        answer = next(
            filter(
                lambda answer: answer.question_id == node.slug, parent_doc.answers.all()
            ),
            None,
        )

        if not answer and node.is_archived:  # pragma: no cover
            return

        fns = {
            Question.TYPE_DATE: self._visit_date_question,
            Question.TYPE_FLOAT: self._visit_simple_question,
            Question.TYPE_INTEGER: self._visit_simple_question,
            Question.TYPE_TEXT: self._visit_simple_question,
            Question.TYPE_TEXTAREA: self._visit_simple_question,
            Question.TYPE_CHOICE: self._visit_choice_question,
            Question.TYPE_MULTIPLE_CHOICE: self._visit_multiple_choice_question,
            Question.TYPE_DYNAMIC_CHOICE: self._visit_dynamic_choice_question,
            Question.TYPE_DYNAMIC_MULTIPLE_CHOICE: self._visit_dynamic_multiple_choice_question,
            Question.TYPE_STATIC: self._visit_static_question,
            Question.TYPE_TABLE: self._visit_table_question,
            Question.TYPE_FORM: self._visit_form_question,
        }
        fn = fns.get(node.type, lambda *_, **__: {})
        ret.update(fn(node, parent_doc=parent_doc, answer=answer, flatten=flatten))
        return ret

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
