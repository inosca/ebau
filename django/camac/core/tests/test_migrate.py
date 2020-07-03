from uuid import uuid4

from django.db import connection
from django.db.migrations.executor import MigrationExecutor


def test_migrate_add_missing_dynamic_options(transactional_db):
    executor = MigrationExecutor(connection)
    migrate_from = [
        ("core", "0048_auto_20200123_1053"),
        ("caluma_form", "0028_auto_20200210_0929"),
    ]
    migrate_to = [
        ("core", "0049_add_missing_dynamic_options"),
        ("caluma_form", "0028_auto_20200210_0929"),
    ]

    executor.loader.build_graph()
    executor.migrate(migrate_from)

    old_apps = executor.loader.project_state(migrate_from).apps

    Answer = old_apps.get_model("caluma_form", "Answer")
    Document = old_apps.get_model("caluma_form", "Document")
    DynamicOption = old_apps.get_model("caluma_form", "DynamicOption")
    Form = old_apps.get_model("caluma_form", "Form")
    FormQuestion = old_apps.get_model("caluma_form", "FormQuestion")
    Question = old_apps.get_model("caluma_form", "Question")
    Service = old_apps.get_model("user", "Service")
    ServiceGroup = old_apps.get_model("user", "ServiceGroup")

    service1 = Service.objects.create(
        service_parent=None,
        service_group=ServiceGroup.objects.create(name="municipality"),
        disabled=False,
        name="Burgdorf",
        sort=0,
    )

    service2 = Service.objects.create(
        service_parent=None,
        service_group=service1.service_group,
        disabled=False,
        name="Hinterpfultigen",
        sort=0,
    )

    service3 = Service.objects.create(
        service_parent=None,
        service_group=service1.service_group,
        disabled=False,
        name="Madiswil",
        sort=0,
    )

    # Create some old data. Can't use factories here
    main_form = Form.objects.create(slug="main-form")
    question1 = Question.objects.create(
        type="dynamic_choice", slug="question1", data_source="Municipalities"
    )
    FormQuestion.objects.create(
        form=main_form, question=question1, id=f"{main_form.slug}.{question1.slug}"
    )
    question2 = Question.objects.create(
        type="dynamic_multiple_choice", slug="question2", data_source="Municipalities"
    )
    FormQuestion.objects.create(
        form=main_form, question=question2, id=f"{main_form.slug}.{question2.slug}"
    )
    document = Document.objects.create(form=main_form, family=uuid4())
    Answer.objects.create(value=str(service1.pk), document=document, question=question1)
    Answer.objects.create(
        value=[str(service2.pk), str(service3.pk)],
        document=document,
        question=question2,
    )

    assert DynamicOption.objects.count() == 0

    # Migrate forwards.
    executor.loader.build_graph()  # reload.
    executor.migrate(migrate_to)

    new_apps = executor.loader.project_state(migrate_to).apps

    DynamicOption = new_apps.get_model("caluma_form", "DynamicOption")
    Document = new_apps.get_model("caluma_form", "Document")
    Question = new_apps.get_model("caluma_form", "Question")
    Service = new_apps.get_model("user", "Service")

    document = Document.objects.get(pk=document.pk)
    question1 = Question.objects.get(pk=question1.pk)
    question2 = Question.objects.get(pk=question2.pk)
    service1 = Service.objects.get(pk=service1.pk)
    service2 = Service.objects.get(pk=service2.pk)

    # Test the new data.
    assert DynamicOption.objects.count() == 3

    assert (
        DynamicOption.objects.get(
            document=document, question=question1, slug=service1.pk
        ).label["de"]
        == "Burgdorf"
    )
    assert (
        DynamicOption.objects.get(
            document=document, question=question2, slug=service2.pk
        ).label["de"]
        == "Hinterpfultigen"
    )
    assert (
        DynamicOption.objects.get(
            document=document, question=question2, slug=service3.pk
        ).label["de"]
        == "Madiswil"
    )

    # finish migrations
    executor.loader.build_graph()  # reload.
    executor.migrate([("core", "0064_delete_journal")])
