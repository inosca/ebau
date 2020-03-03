from caluma.caluma_form.models import (
    Answer,
    Document,
    DynamicOption,
    Form,
    FormQuestion,
    Question,
)
from django.db import connection
from django.db.migrations.executor import MigrationExecutor


def test_migrate_add_missing_dynamic_options(transactional_db, service_factory):
    service = service_factory(
        service_parent=None, service_group__pk=2, disabled=False, pk=1, name="Burgdorf"
    )

    service_factory(
        service_parent=None,
        service_group=service.service_group,
        disabled=False,
        pk=2,
        name="Hinterpfultigen",
    )

    service_factory(
        service_parent=None,
        service_group=service.service_group,
        disabled=False,
        pk=3,
        name="Madiswil",
    )

    executor = MigrationExecutor(connection)
    app = "core"
    migrate_from = [(app, "0048_auto_20200123_1053")]
    migrate_to = [(app, "0049_add_missing_dynamic_options")]

    executor.migrate(migrate_from)

    # Create some old data. Can't use factories here
    main_form = Form.objects.create(slug="main-form")
    question1 = Question.objects.create(
        type="dynamic_choice", slug="question1", data_source="Municipalities"
    )
    FormQuestion.objects.create(form=main_form, question=question1)
    question2 = Question.objects.create(
        type="dynamic_multiple_choice", slug="question2", data_source="Municipalities"
    )
    FormQuestion.objects.create(form=main_form, question=question2)
    document = Document.objects.create(form=main_form)
    Answer.objects.create(value="1", document=document, question=question1)
    Answer.objects.create(value=["2", "3"], document=document, question=question2)

    assert DynamicOption.objects.count() == 0

    # Migrate forwards.
    executor.loader.build_graph()  # reload.
    executor.migrate(migrate_to)

    # Test the new data.
    assert DynamicOption.objects.count() == 3

    assert (
        DynamicOption.objects.get(
            document=document, question=question1, slug="1"
        ).label["de"]
        == "Burgdorf"
    )
    assert (
        DynamicOption.objects.get(
            document=document, question=question2, slug="2"
        ).label["de"]
        == "Hinterpfultigen"
    )
    assert (
        DynamicOption.objects.get(
            document=document, question=question2, slug="3"
        ).label["de"]
        == "Madiswil"
    )
