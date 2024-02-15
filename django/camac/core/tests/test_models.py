from camac.core.models import (
    Answer,
    FormGroup,
    InstanceResource,
    QuestionType,
    Resource,
)


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


def test_instance_resource_defaults(db, instance_resource):
    new_ir = InstanceResource.objects.create(
        resource_id=instance_resource.resource_id,
        available_instance_resource_id=instance_resource.available_instance_resource_id,
        hidden=0,
    )
    assert new_ir.form_group_id == FormGroup.objects.first().pk
    assert new_ir.sort == instance_resource.sort + 1


def test_resource_defaults(db, resource):
    new_resource = Resource.objects.create(
        available_resource_id=resource.available_resource_id,
        hidden=0,
    )
    assert new_resource.sort == resource.sort + 1
