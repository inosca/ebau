from pathlib import Path

import pytest
from caluma.form.models import Document
from django.core.management import call_command

from ..document_merge_service import DMSVisitor


@pytest.fixture
def dms_visitor():
    return DMSVisitor()


@pytest.fixture
def full_document(db):
    path = Path(__file__).parent / "fixtures/form-fixture.json"
    call_command("loaddata", path)

    root_doc = Document.objects.get(form__slug="test-form")
    root_doc.form.meta["is-main-form"] = True
    root_doc.form.save()


# @pytest.mark.parametrize(
#     "caluma_question__type",
#     [
#         (Question.TYPE_INTEGER),
#         (Question.TYPE_FLOAT),
#         (Question.TYPE_DATE),
#         (Question.TYPE_TEXT),
#         (Question.TYPE_TEXTAREA),
#     ],
# )
# def test_document_merge_service_simple_question(
#     db, dms_visitor, caluma_question, answer_factory
# ):
#     answer = answer_factory(question=caluma_question)
#     result = dms_visitor.visit(answer)
#     assert result["value"] == answer.value


# @pytest.mark.parametrize("caluma_question__type", [(Question.TYPE_STATIC)])
# def test_document_merge_service_static_question(
#     db, dms_visitor, caluma_question, answer_factory
# ):
#     answer = answer_factory(question=caluma_question)
#     result = dms_visitor.visit(answer)
#     assert result["content"] == answer.value


# @pytest.mark.parametrize("caluma_question__type", [(Question.TYPE_CHOICE)])
# def test_document_merge_service_choice_question(
#     db, dms_visitor, caluma_question, answer_factory, question_option_factory
# ):
#     opt1, *_ = question_option_factory.create_batch(5, question=caluma_question)
#     answer = answer_factory(question=caluma_question, value=opt1.option.slug)
#     result = dms_visitor.visit(answer)

#     checked_choices = [choice for choice in result["choices"] if choice["checked"]]
#     assert len(checked_choices) == 1
#     assert checked_choices[0]["label"] == str(opt1.option.label)


# @pytest.mark.parametrize(
#     "caluma_question__type,checked",
#     [
#         (Question.TYPE_MULTIPLE_CHOICE, 0),
#         (Question.TYPE_MULTIPLE_CHOICE, 1),
#         (Question.TYPE_MULTIPLE_CHOICE, 2),
#     ],
# )
# def test_document_merge_service_multiple_choice_question(
#     db, dms_visitor, caluma_question, answer_factory, question_option_factory, checked
# ):
#     question_options = question_option_factory.create_batch(5, question=caluma_question)
#     answer = answer_factory(
#         question=caluma_question,
#         value=[opt.option.slug for opt in question_options[:checked]],
#     )
#     result = dms_visitor.visit(answer)

#     checked_choices = [
#         choice["label"] for choice in result["choices"] if choice["checked"]
#     ]
#     assert len(checked_choices) == checked
#     assert set(checked_choices) == set(
#         str(opt.option.label) for opt in question_options[:checked]
#     )


def test_document_merge_service_full_document(db, snapshot, full_document, dms_visitor):
    root_doc = Document.objects.get(form__slug="test-form")
    result = dms_visitor.visit(root_doc)

    snapshot.assert_match(result)
