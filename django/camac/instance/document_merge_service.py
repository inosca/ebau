import requests
from caluma.form.validators import DocumentValidator
from django.conf import settings
from django.utils.translation import gettext as _

from camac.user.models import Service

PEOPLE_SOURCES = {
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
}


def prepare_receipt_page(sections):
    try:
        allgemeine_informationen = next(
            section
            for section in sections
            if section["slug"] == "1-allgemeine-informationen"
        )
        personalien = next(
            child
            for child in allgemeine_informationen["children"]
            if child["slug"] == "personalien"
        )
        people_sources = [
            source
            for source in personalien["children"]
            if source["slug"] in PEOPLE_SOURCES.keys()
        ]

        personalities_t = _("Personalities")
        children = [
            {
                "label": table["label"].replace(f"{personalities_t} -", ""),
                "people": [
                    {
                        "familyName": next(
                            field["value"]
                            for field in row
                            if field["slug"]
                            == PEOPLE_SOURCES[table["slug"]]["familyName"]
                        ),
                        "givenName": next(
                            field["value"]
                            for field in row
                            if field["slug"]
                            == PEOPLE_SOURCES[table["slug"]]["givenName"]
                        ),
                    }
                    for row in table["rows"]
                ],
                "type": "SignatureQuestion",
            }
            for table in people_sources
        ]
        target = {
            "slug": "8-unterschriften",
            "label": _("Signatures"),
            "children": children,
            "type": "FormQuestion",
        }
    except (ValueError, StopIteration):
        raise RuntimeError("Coudn't prepare receipt page")

    return target


class DMSClient:
    def __init__(self, auth_token, url=settings.DOCUMENT_MERGE_SERVICE_URL):
        self.auth_token = auth_token
        self.url = url

    def merge(self, data, template, convert="pdf", add_headers={}):
        headers = {"authorization": self.auth_token}
        headers.update(add_headers)
        url = f"{self.url}template/{template}/merge/"

        response = requests.post(
            url, json={"convert": convert, "data": data}, headers=headers
        )
        response.raise_for_status()

        return response.content


class DMSVisitor:
    def __init__(self, exclude_slugs=[]):
        self.exclude_slugs = exclude_slugs
        self.root_document = None
        self.visible_questions = []

    def visit(self, node, append_receipt_page=False):
        cls_name = type(node).__name__.lower()
        visit_func = getattr(self, f"_visit_{cls_name}")
        result = visit_func(node)

        if append_receipt_page:
            result.append(prepare_receipt_page(result))
        return result

    def _is_visible_question(self, node):
        if node.slug == "einreichen-button":
            return False
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

        if flatten:
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
    ):
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

        if question.data_source == "Service":
            is_service = True
            _filter["service_group"] = 1
        elif question.data_source == "Municipalities":
            _filter["service_group"] = 2
            _filter["service_parent__isnull"] = True
        else:
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
        if is_service:
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
            "text": self._visit_simple_question,
            "textarea": self._visit_simple_question,
            "integer": self._visit_simple_question,
            "float": self._visit_simple_question,
            "date": self._visit_simple_question,
            "choice": self._visit_choice_question,
            "dynamic_choice": self._visit_dynamic_choice_question,
            "multiple_choice": self._visit_multiple_choice_question,
            "dynamic_multiple_choice": self._visit_dynamic_multiple_choice_question,
            "static": self._visit_static_question,
            "table": self._visit_table_question,
            "form": self._visit_form_question,
        }
        fn = fns.get(node.type, lambda *_, **__: {})
        ret.update(fn(node, parent_doc=parent_doc, answer=answer, flatten=flatten))
        return ret
