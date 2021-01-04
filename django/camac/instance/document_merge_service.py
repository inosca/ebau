import re
from importlib import import_module
from logging import getLogger

import requests
from caluma.caluma_form.models import Document, Question
from caluma.caluma_form.validators import DocumentValidator
from django.conf import settings
from django.core.files.base import ContentFile
from django.db.models import Q
from django.utils.text import slugify
from django.utils.translation import gettext as _
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header

from camac.utils import build_url

request_logger = getLogger("django.request")


def get_form_type_key(form_slug):
    configs = settings.APPLICATION.get("DOCUMENT_MERGE_SERVICE", {})

    for key, config in configs.items():
        if form_slug in config.get("forms", []):
            return key

    return form_slug


def get_form_type_config(form_slug):
    return settings.APPLICATION.get("DOCUMENT_MERGE_SERVICE", {}).get(
        get_form_type_key(form_slug), {}
    )


class DMSHandler:
    def __init__(self):
        self.visitor = DMSVisitor()

    def generate_pdf(self, instance, form_slug, request):
        # get caluma document and generate data for document merge service
        if form_slug:
            _filter = {
                "work_item__case__meta__camac-instance-id": instance.pk,
                "form_id": form_slug,
            }
        else:
            _filter = {"case__meta__camac-instance-id": instance.pk}

        try:
            doc = Document.objects.get(**_filter)
        except (Document.DoesNotExist, Document.MultipleObjectsReturned):
            message = _(
                "None or multiple caluma Documents found for instance: %(instance)s"
            ) % {"instance": instance.pk}
            request_logger.error(message)
            raise exceptions.ValidationError(message)

        template = get_form_type_config(doc.form.slug).get("template")

        if template is None:  # pragma: no cover
            raise exceptions.ValidationError(
                _("No template specified for form '%(form_slug)s'.")
                % {"form_slug": doc.form.slug}
            )

        data = {
            "caseId": instance.pk,
            "caseType": str(doc.form.name),
            "sections": self.visitor.visit(doc),
            "signatureSectionTitle": _("Signatures"),
            "signatureTitle": _("Signature"),
            "signatureMetadata": _("Place and date"),
        }

        # merge pdf and store as attachment
        auth = get_authorization_header(request)
        dms_client = DMSClient(auth)
        pdf = dms_client.merge(data, template)

        _file = ContentFile(pdf, slugify(f"{instance.pk}-{doc.form.name}") + ".pdf")
        _file.content_type = "application/pdf"

        return _file


class DMSClient:
    def __init__(self, auth_token, url=settings.DOCUMENT_MERGE_SERVICE_URL):
        self.auth_token = auth_token
        self.url = url

    def merge(self, data, template, convert="pdf", add_headers={}):
        headers = {"authorization": self.auth_token}
        headers.update(add_headers)
        url = build_url(self.url, f"/template/{template}/merge", trailing=True)

        response = requests.post(
            url, json={"convert": convert, "data": data}, headers=headers
        )
        response.raise_for_status()

        return response.content


class DMSVisitor:
    def __init__(self, exclude_slugs=[]):
        self._exclude_slugs = exclude_slugs
        self.root_document = None
        self.visible_questions = []

    @property
    def template_type(self):
        """Group similar forms as they use the same template."""
        return get_form_type_key(self.root_document.form.slug)

    @property
    def exclude_slugs(self):
        if self._exclude_slugs:  # pragma: no cover
            return self._exclude_slugs
        if not self.template_type:  # pragma: no cover
            return []

        return get_form_type_config(self.template_type).get("exclude_slugs", [])

    def visit(self, node):
        cls_name = type(node).__name__.lower()
        visit_func = getattr(self, f"_visit_{cls_name}")
        result = visit_func(node)

        receipt_page = self.prepare_receipt_page()

        if receipt_page:
            result.append(receipt_page)

        return result

    def _is_visible_question(self, node):
        if not self.visible_questions:
            validator = DocumentValidator()
            self.visible_questions = validator.visible_questions(self.root_document)

        return node.slug in self.visible_questions

    def _visit_document(self, node, form=None, flatten=False, **kwargs):
        if self.root_document is None:
            self.root_document = node

        if not form:
            form = node.form

        children = form.questions.all().order_by("-formquestion__sort")

        visited_children = []
        for child in children:
            if child.slug in self.exclude_slugs or not self._is_visible_question(child):
                continue

            result = self._visit_question(
                child, parent_doc=node, flatten=flatten, **kwargs
            )
            if result is None:
                continue

            if child.type == Question.TYPE_FORM and not len(
                result.get("children", [])
            ):  # pragma: no cover
                continue

            visited_children.append(result)

        return visited_children

    def _visit_form_question(self, node, parent_doc=None, answer=None, **_):
        return {"children": self._visit_document(parent_doc, form=node.sub_form)}

    def _visit_table_question(self, node, parent_doc=None, answer=None, **_):
        return {
            "columns": [
                str(column.label)
                for column in node.row_form.questions.all().order_by(
                    "-formquestion__sort"
                )
            ],
            "rows": [
                self._visit_document(doc, flatten=True)
                for doc in answer.documents.all()
            ]
            if answer
            else [],
        }

    def _visit_choice_question(
        self, node, parent_doc=None, answer=None, flatten=False, limit=None, **_
    ):
        answer = answer.value if answer else None
        options = (
            node.options.all()
            .filter(Q(is_archived=False) | Q(slug=answer))
            .order_by("-questionoption__sort")
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
        options = (
            node.options.all()
            .filter(Q(is_archived=False) | Q(slug__in=answers))
            .order_by("-questionoption__sort")
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
            value = data_source.validate_answer_value(ans, document, question, None)
            yield value

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
        return {
            "value": answer.date.strftime("%Y-%m-%d")
            if answer and answer.date
            else None
        }

    def _visit_question(self, node, parent_doc=None, flatten=False):

        ret = {
            "label": str(node.label),
            "slug": node.slug,
            "type": "".join(
                word.capitalize() for word in f"{node.type}_question".split("_")
            ),
        }

        answer = parent_doc.answers.filter(question=node).first()

        if not answer and node.is_archived:
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

    def prepare_receipt_page(self):
        if self.template_type in ["vorabklaerung-einfach", "baugesuch"]:
            slugs = settings.APPLICATION.get("DOCUMENT_MERGE_SERVICE", {}).get(
                self.template_type, {}
            )

            allgemeine_info = self.root_document.form.questions.get(
                slug=slugs["allgemeine_info"]
            ).sub_form

        if self.template_type == "vorabklaerung-einfach":

            def _get_person_value(slug_key):
                question = allgemeine_info.questions.get(slug=slugs[slug_key])
                return self._visit_question(question, parent_doc=self.root_document)[
                    "value"
                ]

            given_name, family_name = [
                _get_person_value(key) for key in ["givenName", "familyName"]
            ]

            return {
                "label": _("Applicant"),
                "people": [{"familyName": family_name, "givenName": given_name}],
                "type": "SignatureQuestion",
            }

        elif self.template_type == "baugesuch":
            personalien = allgemeine_info.questions.get(
                slug=slugs["personalien"]
            ).sub_form

            children = []
            for question in personalien.questions.all():
                if not self._is_visible_question(question):  # pragma: no cover
                    continue

                table = self._visit_question(question, parent_doc=self.root_document)

                if (
                    table["slug"] not in slugs["people_sources"]
                    or "rows" in table
                    and not table["rows"]
                ):  # pragma: no cover
                    continue

                children.append(
                    {
                        "label": re.match(r".* - (.*)$", table["label"]).group(1),
                        "people": [
                            {
                                "familyName": next(
                                    field["value"]
                                    for field in row
                                    if field["slug"]
                                    == slugs["people_sources"][table["slug"]][
                                        "familyName"
                                    ]
                                ),
                                "givenName": next(
                                    field["value"]
                                    for field in row
                                    if field["slug"]
                                    == slugs["people_sources"][table["slug"]][
                                        "givenName"
                                    ]
                                ),
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

        if self.template_type == "selbstdeklaration":
            # TODO: Soon we'll have a responsible person for this form. The
            # people will then be computed from that table instead of this
            # static empty person.
            return {
                "label": _("Applicant"),
                "people": [{"firstName": "", "lastName": ""}],
                "type": "SignatureQuestion",
            }

        return None  # pragma: no cover
