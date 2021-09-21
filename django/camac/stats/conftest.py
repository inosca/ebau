import datetime
from typing import Callable, List, Union

import pytest
from caluma.caluma_form import (
    factories as caluma_form_factories,
    models as caluma_form_models,
)
from caluma.caluma_form.factories import (
    DocumentFactory,
    FormQuestionFactory,
    QuestionFactory,
)
from caluma.caluma_form.models import Form, Question

from camac.instance.models import Instance, InstanceState
from camac.instance.serializers import SUBMIT_DATE_FORMAT


@pytest.fixture
def nfd_tabelle_document_row(nfd_tabelle_form) -> Callable:
    def wrapper(service_id, status, date_request=None, date_response=None, family=None):
        defaults = {}
        if family:
            defaults.update({"family": family})
        document = caluma_form_factories.DocumentFactory(
            form=nfd_tabelle_form, **defaults
        )
        caluma_form_factories.AnswerFactory(
            document=document, question_id="nfd-tabelle-behoerde", value=service_id
        )
        caluma_form_factories.AnswerFactory(
            document=document, question_id="nfd-tabelle-status", value=status
        )
        if date_request:
            caluma_form_factories.AnswerFactory(
                document=document,
                question_id="nfd-tabelle-datum-anfrage",
                date=date_request,
            )
        if date_response:
            caluma_form_factories.AnswerFactory(
                document=document,
                question_id="nfd-tabelle-datum-antwort",
                date=date_response,
            )
        return document

    return wrapper


@pytest.fixture
def nfd_tabelle_form():
    form = caluma_form_factories.FormFactory(slug="nfd-tabelle")
    question_behoerde = caluma_form_factories.QuestionFactory(
        slug="nfd-tabelle-behoerde", type=caluma_form_models.Question.TYPE_INTEGER
    )
    question_status = caluma_form_factories.QuestionFactory(
        slug="nfd-tabelle-status", type=caluma_form_models.Question.TYPE_TEXT
    )
    question_date_request = caluma_form_factories.QuestionFactory(
        slug="nfd-tabelle-datum-anfrage", type=caluma_form_models.Question.TYPE_DATE
    )
    question_date_response = caluma_form_factories.QuestionFactory(
        slug="nfd-tabelle-datum-antwort", type=caluma_form_models.Question.TYPE_DATE
    )
    caluma_form_factories.FormQuestionFactory(form=form, question=question_behoerde)
    caluma_form_factories.FormQuestionFactory(form=form, question=question_status)
    caluma_form_factories.FormQuestionFactory(form=form, question=question_date_request)
    caluma_form_factories.FormQuestionFactory(
        form=form, question=question_date_response
    )
    return form


@pytest.fixture
def nfd_tabelle_table_answer(work_item_factory):
    def wrapper(be_instance):
        nfd_form = Form.objects.get(slug="nfd")
        nfd_document = DocumentFactory(form=nfd_form)
        question_table = QuestionFactory(
            slug="nfd-tabelle-table", type=Question.TYPE_TABLE
        )
        FormQuestionFactory(form=nfd_form, question=question_table)

        work_item_factory(
            case=be_instance.case,
            task_id="nfd",
            document=nfd_document,
        )
        table_answer = nfd_document.answers.create(question_id="nfd-tabelle-table")
        return table_answer

    return wrapper


@pytest.fixture
def rejected_application_factory(
    instance_factory, instance_with_case, history_entry_t_factory, freezer
):
    def wrapper(parent_application: Instance, duration: int = 5) -> Instance:
        """
        Create one rejected application predating a parent application

        @param parent_application: Application instance succeeding rejected instance
        @param duration: num of days until rejection
        @return: instance of rejected application: Instance
        """
        instance_state_finished, created = InstanceState.objects.get_or_create(
            name="finished"
        )
        instance_state_rejected, created = InstanceState.objects.get_or_create(
            name="rejected"
        )
        freezer.move_to(
            parent_application.creation_date - datetime.timedelta(days=duration)
        )
        rejected_application = instance_with_case(
            instance_factory(
                instance_state=instance_state_finished,
                previous_instance_state=instance_state_rejected,
            )
        )
        freezer.move_to(parent_application.creation_date)
        history_entry_t_factory(
            history_entry__instance=rejected_application,
            language="de",
            title="Dossier zurückgewiesen",
        )
        rejected_application.case.meta.update(
            {
                "submit-date": rejected_application.creation_date.strftime(
                    SUBMIT_DATE_FORMAT
                ),
                "paper-submit-date": rejected_application.creation_date.strftime(
                    SUBMIT_DATE_FORMAT
                ),
            }
        )
        rejected_application.case.document.source = parent_application.case.document
        rejected_application.case.document.save()
        return rejected_application

    return wrapper


@pytest.fixture
def nest_rejected_applications(rejected_application_factory):
    def wrapper(parent: Instance, recursions: List[int]) -> Union[Instance, Callable]:
        """
        Recursively nest rejected instances

        Every item in the recursion parameter defines a number of days
         the parent instance predates the current instance.

        The recursions sum up to the total number of days to add to the cases cycle time.
        """
        if not recursions:
            return parent
        new_parent = rejected_application_factory(parent, recursions[0])
        return wrapper(new_parent, recursions[1:])

    return wrapper
