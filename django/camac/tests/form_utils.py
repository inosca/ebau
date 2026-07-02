from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, TypedDict

from caluma.caluma_form.factories import (
    AnswerDocumentFactory,
    AnswerFactory,
    DocumentFactory,
    DynamicOptionFactory,
    QuestionFactory,
    QuestionOptionFactory,
)
from caluma.caluma_form.models import Answer, Document, FormQuestion, Option, Question

if TYPE_CHECKING:
    from camac.user.models import Service


class FormUtils:
    AnswerValue = str | date | float | int | list[str]
    Options = list[str | tuple[str, str]]

    class TableCell(TypedDict):
        value: FormUtils.AnswerValue
        options: FormUtils.Options

    def __init__(self):
        self._sort = 99999999

    def _question(self, slug, type, label=None, options=None):
        question = Question.objects.filter(pk=slug).first()
        if question is None:
            question = QuestionFactory(
                pk=slug,
                is_required="false",
                type=type,
                **({"label": label} if label else {}),
            )
        if options:
            for option in options:
                if isinstance(option, tuple):
                    o_slug = option[0]
                    o_label = option[1]
                else:
                    o_slug = option
                    o_label = option.capitalize()

                if Option.objects.filter(pk=o_slug).exists():
                    continue

                QuestionOptionFactory(
                    question=question,
                    option__slug=o_slug,
                    option__label=o_label,
                )
        return question

    def _next_sort(self):
        # Sort should be descending, so
        # things are ordered in the way they're constructed (caluma sorting
        # is reverse - highest-to-lowest numbers)
        self._sort -= 1
        return self._sort

    @staticmethod
    def _get_question_type(value, options, label):
        if options or label:
            if isinstance(value, list) or isinstance(label, list):  # pragma: no cover
                return Question.TYPE_MULTIPLE_CHOICE
            return Question.TYPE_CHOICE
        if isinstance(value, date):
            return Question.TYPE_DATE
        if isinstance(value, float):
            return Question.TYPE_FLOAT
        if isinstance(value, list):
            if value and isinstance(value[0], dict):  # pragma: no cover
                raise RuntimeError("YOU SHOULD USE add_table_answer, not add_answer")
            return Question.TYPE_MULTIPLE_CHOICE
        if isinstance(value, int):
            return Question.TYPE_INTEGER
        return Question.TYPE_TEXT

    def add_answer(
        self,
        document: Document,
        question: str,
        value: AnswerValue,
        label: str | list[str] | None = None,
        question_label: str | None = None,
        options: Options | None = None,
        question_type: str | None = None,
    ) -> Answer:
        """Add answer to a caluma document for test cases.

        This will automatically create questions and options if necessary.

        Args:
            document: The document to add the answer to.
            question: The question slug.
            value:
                The value of the answer.

                The datatype of this argument determines the question type
                automatically.
            label:
                Label(s) for the option(s).

                If provided, one option (or multiple if a list is passed) will be
                created automatically and the question type will be set to
                choice or multiple choice.
            question_label: Label for the question.
            options:
                Options for the question.

                - If a list of tuples is passed, the first item is used as the
                slug and the second as the label.
                - If a list of strings is passed, slug and label are the same.
            question_type:
                Fixed type for the question.

                Overrides all automatic question type detection logic.

        Returns:
            The newly created answer.

        Examples:
            Add an answer to a text question:
                >>> form_utils.add_answer(document, "text-question", "Test value")

            Add an answer to a date question with a custom question label:
                >>> form_utils.add_answer(
                ...     document,
                ...     "birthday",
                ...     date(1999, 9, 9),
                ...     question_label="When were you born?",
                ... )

            Add an answer to a choice question with predefined options:
                >>> form_utils.add_answer(
                ...     document,
                ...     "sure",
                ...     "sure-yes",
                ...     options=[
                ...         ("sure-yes", "Yes"),
                ...         ("sure-no", "No"),
                ...         ("sure-maybe", "Maybe"),
                ...     ],
                ... )
        """

        question_type = question_type or FormUtils._get_question_type(
            value, options, label
        )
        value_key = "date" if question_type == Question.TYPE_DATE else "value"

        answer = AnswerFactory(
            document=document,
            question=self._question(question, question_type, question_label, options),
            **{value_key: value},
        )
        FormQuestion.objects.get_or_create(
            form=document.form,
            question=answer.question,
            defaults={"sort": self._next_sort()},
        )

        if label:
            if not isinstance(label, list):
                label = [label]

            if not isinstance(value, list):
                value = [value]

            for val, lab in zip(value, label):
                if not isinstance(lab, dict):
                    lab = {"de": lab, "fr": lab}

                QuestionOptionFactory(
                    question_id=question, option__slug=val, option__label=lab
                )

        return answer

    def add_table_answer(
        self,
        document: Document,
        question: str,
        rows: list[dict[str, TableCell]],
        table_answer: Answer | None = None,
        row_form_id: str | None = None,
    ) -> Answer:
        """Add a table answer (including row documents) to a document.

        Create the table question if necessary and populate it with a row form
        and it's (column) questions based on the provided data, then fill in the
        rows.

        Args:
            document: The document to add the table answer to.
            question: The table question slug.
            rows:
                Row data for the table.

                Each item represents a table row and must be a mapping of
                column slugs to values. If a value is a dictionary, it may
                contain `value` and `options` keys to define choice
                options for the cell.
            table_answer:
                Existing table answer to append rows to.

                If not provided, a new table answer will be created.
            row_form_id:
                Form slug to use for table rows.

                If not provided, the row form slug will be taken from the table
                question.

        Returns:
            The newly created answer.

        Examples:
            Add a table answer with two rows:
                >>> form_utils.add_table_answer(
                ...     document,
                ...     "applicants",
                ...     [
                ...         {"first-name": "Hans", "last-name": "Muster"},
                ...         {"first-name": "Sandra", "last-name": "Testerin"},
                ...     ],
                ... )

            Add a table answer with choice options in a cell:
                >>> form_utils.add_table_answer(
                ...     document,
                ...     "representative",
                ...     [
                ...         {
                ...             "first-name": "Hans",
                ...             "last-name": "Muster",
                ...             "is-juristic": {
                ...                 "value": "is-juristic-yes",
                ...                 "options": [
                ...                     ("is-juristic-yes", "Yes"),
                ...                     ("is-juristic-no", "No"),
                ...                 ]
                ...             }
                ...         },
                ...     ],
                ... )
        """
        answer = (
            self.add_answer(document, question, value=None, question_type="table")
            if not table_answer
            else table_answer
        )
        if row_form_id:
            answer.question.row_form_id = row_form_id
            answer.question.save()
        else:
            row_form_id = answer.question.row_form_id

        for i, row in enumerate(reversed(rows)):
            row_args = {"form_id": row_form_id}
            row_document = DocumentFactory(family=document.family, **row_args)
            for column, value in row.items():
                options = None
                if isinstance(value, dict):
                    options = value["options"]
                    value = value["value"]
                self.add_answer(row_document, column, value, options=options)

            AnswerDocumentFactory(document=row_document, answer=answer, sort=i)

        return answer

    def add_municipality(
        self,
        document: Document,
        question: str,
        service: Service,
    ) -> Answer:
        """Add a municipality answer (including a dynamic option) to a document.

        Args:
            document: The document to add the answer to.
            question: The municipality question slug (usually `"gemeinde"`).
            service:
                The service to set as the municipality.

                The service name is used as the label for the dynamically created
                option.

        Returns:
            The newly created answer.

        Examples:
            >>> form_utils.add_municipality(
            ...     instance.case.document,
            ...     "gemeinde",
            ...     my_service
            ... )
        """

        DynamicOptionFactory(
            question_id=question,
            document=document,
            slug=str(service.pk),
            label={"de": service.get_name()},
        )
        return self.add_answer(document, question, str(service.pk))

    def set_is_paper(self, document: Document, is_paper: bool) -> Answer:
        """Add "is-paper" answer to a document.

        Args:
            document: The document to add the answer to.
            is_paper: Whether the instance is paper or not.

        Returns:
            The newly created answer.

        Examples:
            >>> utils.set_is_paper(instance.case.document, True)
        """

        return self.add_answer(
            document,
            "is-paper",
            f"is-paper-{'yes' if is_paper else 'no'}",
        )
