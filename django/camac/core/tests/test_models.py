from camac.core.models import Answer, QuestionType


def test_answer_get_value_by_cqi(
    db,
    instance,
    answer_list_factory,
    question_chapter_factory,
):

    type = QuestionType.objects.create(pk=4)
    question_chapter = question_chapter_factory.create(question__question_type=type)
    question = question_chapter.question
    answer_list_factory.create(question=question, name="Foo", value="Foo")
    answer_list_factory.create(question=question, name="Bar", value="Bar")
    answer_list_factory.create(question=question, name="Foobar", value="Foobar")

    Answer.objects.create(
        instance=instance,
        question=question,
        answer='["Foo", "Bar", "Foobar"]',
        item=1,
        chapter=question_chapter.chapter,
    )

    answer = Answer.get_value_by_cqi(
        instance,
        question_chapter.chapter_id,
        question.pk,
        1,
        default="",
    )

    assert answer == "Foo, Bar, Foobar"
