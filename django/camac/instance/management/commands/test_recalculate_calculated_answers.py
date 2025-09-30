import os

from caluma.caluma_form.api import save_answer, save_document
from caluma.caluma_form.models import Question
from django.core.management import call_command


def test_recalculate_calculated_answers(
    db,
    caluma_form_factory,
    caluma_form_question_factory,
    caluma_case_factory,
    instance,
):
    main_form = caluma_form_factory(slug="baugesuch-v5")
    form_question_1 = caluma_form_question_factory(
        form=main_form,
        question__type=Question.TYPE_INTEGER,
        question__slug="form_question_1",
        question__is_required=True,
    )
    question_1 = form_question_1.question
    form_question_2 = caluma_form_question_factory(
        form=main_form,
        question__type=Question.TYPE_INTEGER,
        question__slug="form_question_2",
        question__is_required=True,
    )
    question_2 = form_question_2.question
    form_calculated_question = caluma_form_question_factory(
        form=main_form,
        question__slug="calculated_question",
        question__type=Question.TYPE_CALCULATED_FLOAT,
        question__calc_expression=(
            '"form_question_1"|answer(0) + "form_question_2"|answer(0)'
        ),
    )
    calculated_question = form_calculated_question.question

    main_document = save_document(form=main_form)
    main_case = caluma_case_factory(document=main_document)
    instance.case = main_case
    instance.save()

    save_answer(question=question_1, value=25, document=main_document)
    save_answer(question=question_2, value=30, document=main_document)

    # Save a wrong calculated answer value
    calculated_answer = save_answer(
        question=calculated_question, document=main_document, value=7
    )
    assert calculated_answer.value == 7

    question_list = ["calculated_question"]

    call_command(
        "recalculate_calculated_answers",
        *question_list,
        "--commit",
        stdout=open(os.devnull, "w"),
    )

    # Check answer value after running recalculate management command
    calculated_answer.refresh_from_db()
    assert calculated_answer.value == 55

    # Recalculate answers of hidden questions if possible
    calculated_question.is_hidden = "true"
    calculated_question.save()
    calculated_answer = save_answer(
        question=calculated_question, document=main_document, value=7
    )
    call_command(
        "recalculate_calculated_answers",
        *question_list,
        "--commit",
        stdout=open(os.devnull, "w"),
    )

    calculated_answer.refresh_from_db()
    assert calculated_answer.value == 55

    # Cannot evaluate calculated answer because dependency is hidden,
    # don't update
    question_2.is_hidden = "true"
    question_2.save()
    calculated_answer = save_answer(
        question=calculated_question, document=main_document, value=7
    )
    call_command(
        "recalculate_calculated_answers",
        *question_list,
        "--commit",
        stdout=open(os.devnull, "w"),
    )

    calculated_answer.refresh_from_db()
    assert calculated_answer.value == 7
