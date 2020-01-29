import re

import requests
from caluma.caluma_form.models import Question
from caluma.caluma_form.validators import DocumentValidator
from django.conf import settings
from django.utils.translation import gettext as _

from camac.user.models import Service
from camac.utils import build_url

SLUGS = {
    "baugesuch": {
        "allgemeine_info": "1-allgemeine-informationen",
        "personalien": "personalien",
        "people_sources": {
            "personalien-gesuchstellerin": {
                "familyName": "name-gesuchstellerin",
                "givenName": "vorname-gesuchstellerin",
            },
            "personalien-vertreterin-mit-vollmacht": {
                "familyName": "name-vertreterin",
                "givenName": "vorname-vertreterin",
            },
            "personalien-grundeigentumerin": {
                "familyName": "name-grundeigentuemerin",
                "givenName": "vorname-grundeigentuemerin",
            },
            "personalien-gebaudeeigentumerin": {
                "familyName": "name-gebaeudeeigentuemerin",
                "givenName": "vorname-gebaeudeeigentuemerin",
            },
            "personalien-projektverfasserin": {
                "familyName": "name-projektverfasserin",
                "givenName": "vorname-projektverfasserin",
            },
        },
        "exclude_slugs": ["8-freigabequittung"],
    },
    "vorabklaerung-einfach": {
        "allgemeine_info": "allgemeine-informationen-vorabklaerung-form",
        "givenName": "vorname-gesuchstellerin-vorabklaerung",
        "familyName": "name-gesuchstellerin-vorabklaerung",
        "exclude_slugs": ["freigabequittung-vorabklaerung-form"],
    },
    "selbstdeklaration": {
        "exclude_slugs": ["freigabequittung-sb1", "freigabequittung-sb2"]
    },
}


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
        form_slug = self.root_document.form.slug

        if form_slug in ["baugesuch", "vorabklaerung-vollstaendig"]:
            return "baugesuch"
        elif form_slug == "vorabklaerung-einfach":
            return form_slug
        elif form_slug in ["sb1", "sb2"]:
            return "selbstdeklaration"

    @property
    def exclude_slugs(self):
        if self._exclude_slugs:  # pragma: no cover
            return self._exclude_slugs
        if not self.template_type:  # pragma: no cover
            return []

        return SLUGS[self.template_type]["exclude_slugs"]

    def visit(self, node, append_receipt_page=False):
        cls_name = type(node).__name__.lower()
        visit_func = getattr(self, f"_visit_{cls_name}")
        result = visit_func(node)

        if append_receipt_page:
            result.append(self.prepare_receipt_page())
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
            if child.slug in self.exclude_slugs:
                continue

            result = self._visit_question(
                child, parent_doc=node, flatten=flatten, **kwargs
            )

            if not result["hidden"]:
                visited_children.append(result)

        return visited_children

    def _visit_form_question(self, node, parent_doc=None, answer=None, **_):
        return {"children": self._visit_document(parent_doc, form=node.sub_form)}

    def _visit_table_question(self, node, parent_doc=None, answer=None, **_):
        return {
            "columns": [str(column.label) for column in node.row_form.questions.all()],
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
        options = node.options.all().order_by("-questionoption__sort")

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
        options = node.options.all().order_by("-questionoption__sort")

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

    def _visit_dynamic_choice_question(self, node, parent_doc=None, answer=None, **_):
        answer = answer.value if answer else None
        options = self._get_dynamic_options(node)

        return {
            "type": "TextQuestion",
            "value": next(
                (str(option[1]) for option in options if option[0] == answer), None
            ),
        }

    def _visit_dynamic_multiple_choice_question(
        self, node, parent_doc=None, answer=None, **_
    ):  # pragma: no cover
        answers = answer.value if answer else []
        options = self._get_dynamic_options(node)

        return {
            "type": "TextQuestion",
            "value": ", ".join(
                [str(option[1]) for option in options if option[0] in answers]
            ),
        }

    def _visit_static_question(self, node, parent_doc=None, answer=None, **_):
        return {"content": str(answer.static_content) if answer else None}

    def _visit_simple_question(self, node, parent_doc=None, answer=None, **_):
        return {"value": answer.value if answer else None}

    def _get_dynamic_options(self, question, **_):
        """Replicate the data_sources.py caluma-extension."""

        is_service = False
        _filter = {"disabled": False}

        if question.data_source == "Service":  # pragma: no cover
            is_service = True
            _filter["service_group"] = 1
        elif question.data_source == "Municipalities":
            _filter["service_group"] = 2
            _filter["service_parent__isnull"] = True
        else:  # pragma: no cover
            raise ValueError(
                "Unknown data_source encountered in question {question.slug}: {question.data_source}"
            )

        options = [
            (str(service.pk), service.get_name())
            for service in Service.objects.filter(**_filter).prefetch_related("groups")
        ]

        if not is_service:
            options = [
                (option[0], option[1].replace("Leitbehörde ", "")) for option in options
            ]

        options.sort(key=lambda entry: entry[1].casefold())
        if is_service:  # pragma: no cover
            options.append((-1, "Andere"))

        return options

    def _visit_question(self, node, parent_doc=None, flatten=False):

        ret = {
            "label": str(node.label),
            "slug": node.slug,
            "type": "".join(
                word.capitalize() for word in f"{node.type}_question".split("_")
            ),
            "hidden": not self._is_visible_question(node),
        }

        if ret["hidden"]:
            ret["value"] = None
            return ret

        answer = parent_doc.answers.filter(question=node).first()

        fns = {
            Question.TYPE_DATE: self._visit_simple_question,
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
        slugs = SLUGS[self.template_type]

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
                table = self._visit_question(question, parent_doc=self.root_document)
                if (
                    table["hidden"]
                    or table["slug"] not in slugs["people_sources"]
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

        else:  # pragma: no cover
            raise ValueError("No matching form found for receipt page")
