from caluma.caluma_form.models import Answer, Document, DynamicOption, Option
from caluma.caluma_form.validators import DocumentValidator
from caluma.caluma_workflow.models import Case
from django.utils.translation import get_language

from .utils import handle_string_values


class AnswersDict(dict):
    """Dict with special get capabilities."""

    def get(self, key, default=None):
        """
        Get `key` and fallback to `default` if not available or value is None.

        The vanilla `dict.get()` would only fallback to the default if the key is
        missing.
        """
        if key in self:
            value = self[key]
            return value if value is not None else default
        return default


# Dicts with all questions we need from caluma. Questions under the "top" key, are
# directly accessible. Other keys refer to tableQuestions with their corresponding
# sub-questions. The second tuple element is an example value and also used for tests.
# In contrast to
# `ech_bern.tests.caluma_document_data.{baugesuch_data,vorabklaerung_data}`, these
# dicts contain the slugs of *Choices.
# If you find yourself editing these slugs, you might also want to edit
# `baugesuch_data`.
slugs_baugesuch = {
    "top": [
        ("anzahl-abstellplaetze-fur-motorfahrzeuge", 23),
        ("baukosten-in-chf", 232323),
        ("bemerkungen", " Foo bar "),
        ("beschreibung-bauvorhaben", "Beschreibung\nMehr Beschreibung"),
        ("dauer-in-monaten", 23),
        ("effektive-geschosszahl", 23),
        ("gemeinde", "2"),
        ("geplanter-baustart", "2019-09-15"),
        ("gwr-egid", "23"),
        ("nr", "23"),
        ("nutzungsart", ["nutzungsart-wohnen"]),
        ("nutzungszone", "Testnutzungszone"),
        ("ort-grundstueck", "Burgdorf"),
        ("ort-parzelle", "Burgdorf"),
        ("sammelschutzraum", "sammelschutzraum-ja"),
        ("strasse-flurname", "Teststrasse"),
    ],
    "beschreibung-der-prozessart-tabelle": [
        [("prozessart", "prozessart-fliesslawine")]
    ],
    "parzelle": [
        [
            ("e-grid-nr", "23"),
            ("lagekoordinaten-nord", "1070500.000"),
            ("lagekoordinaten-ost", "2480034.0"),
            ("parzellennummer", "1586"),
        ],
        [
            ("e-grid-nr", "24"),
            ("lagekoordinaten-nord", "1070600.000"),
            ("lagekoordinaten-ost", "2480035.0"),
            ("parzellennummer", "1587"),
        ],
    ],
    "personalien-gesuchstellerin": [
        [
            ("name-gesuchstellerin", "Smith"),
            ("nummer-gesuchstellerin", "23"),
            ("ort-gesuchstellerin", "Burgdorf"),
            ("plz-gesuchstellerin", 2323),
            ("strasse-gesuchstellerin", "Teststrasse"),
            ("vorname-gesuchstellerin", "Winston"),
            (
                "juristische-person-gesuchstellerin",
                "juristische-person-gesuchstellerin-nein",
            ),
            ("name-juristische-person-gesuchstellerin", None),
        ]
    ],
    "personalien-grundeigentumerin": [
        [
            ("name-grundeigentuemerin", "Smith"),
            ("nummer-grundeigentuemerin", "23"),
            ("ort-grundeigentuemerin", "Burgdorf"),
            ("plz-grundeigentuemerin", 2323),
            ("strasse-grundeigentuemerin", "Teststrasse"),
            ("vorname-grundeigentuemerin", "Winston"),
            (
                "juristische-person-grundeigentuemerin",
                "juristische-person-grundeigentuemerin-nein",
            ),
            ("name-juristische-person-grundeigentuemerin", None),
        ]
    ],
    "personalien-projektverfasserin": [
        [
            ("name-projektverfasserin", "Smith"),
            ("nummer-projektverfasserin", None),
            ("ort-projektverfasserin", "Burgdorf"),
            ("plz-projektverfasserin", 2323),
            ("strasse-projektverfasserin", "Teststrasse"),
            ("vorname-projektverfasserin", "Winston"),
            (
                "juristische-person-projektverfasserin",
                "juristische-person-projektverfasserin-nein",
            ),
            ("name-juristische-person-projektverfasserin", None),
        ]
    ],
    "personalien-vertreterin-mit-vollmacht": [
        [
            ("name-vertreterin", "Smith"),
            ("nummer-vertreterin", "23"),
            ("ort-vertreterin", "Burgdorf"),
            ("plz-vertreterin", 2323),
            ("strasse-vertreterin", "Teststrasse"),
            ("vorname-vertreterin", "Winston"),
            ("juristische-person-vertreterin", "juristische-person-vertreterin-ja"),
            ("name-juristische-person-vertreterin", "Firma XY AG"),
        ]
    ],
}

slugs_vorabklaerung_einfach = {
    "top": [
        ("gemeinde", "2"),
        ("beschreibung-bauvorhaben", "lorem ipsum\tmit tab"),
        ("gwr-egid", "23"),
        ("name-gesuchstellerin", "Smith"),
        ("nr", "23"),
        ("ort-grundstueck", "Burgdorf"),
        ("strasse-flurname", "Teststrasse mit   Leerzeichen"),
    ],
    "personalien-gesuchstellerin": [
        [
            ("name-gesuchstellerin", "Smith"),
            ("nummer-gesuchstellerin", "23"),
            ("ort-gesuchstellerin", "Burgdorf"),
            ("plz-gesuchstellerin", 2323),
            ("strasse-gesuchstellerin", "Teststrasse"),
            ("vorname-gesuchstellerin", "Winston"),
            ("telefon-oder-mobile-gesuchstellerin", "0311234567"),
            ("e-mail-gesuchstellerin", "a@b.ch"),
            (
                "juristische-person-gesuchstellerin",
                "juristische-person-gesuchstellerin-nein",
            ),
            ("name-juristische-person-gesuchstellerin", None),
        ]
    ],
    "parzelle": [
        [
            ("e-grid-nr", "23"),
            ("lagekoordinaten-nord", "1070500.000"),
            ("lagekoordinaten-ost", "2480034.0"),
            ("parzellennummer", "1586"),
        ],
    ],
}


class DocumentParser:
    simple_questions = ["integer", "float", "text", "textarea", "date"]

    def __init__(self, document: Document):
        self.document = document
        self.lang = get_language()
        self.slugs_table = slugs_baugesuch
        if document.form.slug in ["vorabklaerung-einfach", "vorabklaerung-einfach-v4"]:
            self.slugs_table = slugs_vorabklaerung_einfach

        # main slugs are all questions under the "top" key combined with all the other keys
        main_slugs = [slug for slug, _ in self.slugs_table["top"]] + [
            key for key in self.slugs_table if not key == "top"
        ]
        self.answers = AnswersDict(
            **{
                "ech-subject": document.form.name[self.lang],
                "caluma-workflow-slug": document.case.workflow.slug,
            }
        )
        self.answers.update(self.parse_answers(self.document, main_slugs))

    def _get_option_label(self, slug):
        option = Option.objects.get(pk=slug)
        return handle_string_values(option.label[self.lang])

    def _choice(self, answer, document):
        return self._get_option_label(answer.value)

    def _multiple_choice(self, answer, document):
        return [self._get_option_label(slug) for slug in answer.value]

    def _get_dynamic_option_label(self, slug, document, question):
        option = DynamicOption.objects.filter(
            slug=slug, document=document, question=question
        ).first()
        for v in option.label.values():
            if v:
                return handle_string_values(v)

    def _dynamic_choice(self, answer, document):
        return self._get_dynamic_option_label(answer.value, document, answer.question)

    def _dynamic_multiple_choice(self, answer, document):  # pragma: no cover
        return [
            self._get_dynamic_option_label(slug, document, answer.question)
            for slug in answer.value
        ]

    def _table(self, answer, document):
        rows = []
        # the relevant question slugs for this subform
        slugs = [slug for slug, _ in self.slugs_table[answer.question.slug][0]]

        for row_doc in answer.documents.all():
            rows.append(self.parse_answers(row_doc, slugs))
        return rows

    def parse_answers(self, document, slugs):
        """Parse all answers that are visible in the document and intended for ECH."""

        visible_questions = DocumentValidator().visible_questions(document, None)
        caluma_answers = Answer.objects.filter(
            document=document,
            question__slug__in=list(set(slugs) & set(visible_questions)),
        )

        answers = AnswersDict()

        for answer in caluma_answers:
            question_type_name = answer.question.type

            if question_type_name in self.simple_questions:
                answers[answer.question.slug] = handle_string_values(answer.value)
                continue

            answers[answer.question.slug] = getattr(self, f"_{question_type_name}")(
                answer, document
            )

        return answers


def get_document(instance_id):
    """Retrieve caluma answers and compile to answers-dict."""
    case = Case.objects.get(instance__pk=instance_id)
    dp = DocumentParser(case.document)
    return dp.answers
