import pytest
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_workflow import models as caluma_workflow_models
from django.core.cache import cache
from django.core.management import call_command

FORM_QUESTION_MAP = [
    ("main-form", "gemeinde"),
    ("main-form", "papierdossier"),
    ("main-form", "baubeschrieb"),
    ("main-form", "personalien-sb"),
    ("main-form", "personalien-gesuchstellerin"),
    ("sb1", "papierdossier"),
    ("sb1", "personalien-sb1-sb2"),
    ("sb2", "papierdossier"),
    ("nfd", "papierdossier"),
]


@pytest.fixture
def caluma_workflow(settings, caluma_forms):
    forms = [
        caluma_form_models.Form.objects.create(slug="baugesuch"),
        caluma_form_models.Form.objects.create(slug="baugesuch-generell"),
        caluma_form_models.Form.objects.create(slug="baugesuch-mit-uvp"),
        caluma_form_models.Form.objects.create(slug="vorabklaerung-einfach"),
        caluma_form_models.Form.objects.create(slug="vorabklaerung-vollstaendig"),
    ]

    call_command("loaddata", settings.ROOT_DIR("kt_bern/config-caluma-workflow.json"))

    workflows = caluma_workflow_models.Workflow.objects.all()

    for workflow in workflows:
        workflow.allow_forms.clear()
        workflow.allow_forms.add(caluma_form_models.Form.objects.get(pk="main-form"))
        workflow.save()

    for form in forms:
        form.delete()

    return workflows


@pytest.fixture
def caluma_forms(settings):
    # forms
    caluma_form_models.Form.objects.create(
        slug="main-form", meta={"is-main-form": True}, name="Baugesuch"
    )
    caluma_form_models.Form.objects.create(slug="sb1")
    caluma_form_models.Form.objects.create(slug="sb2")
    caluma_form_models.Form.objects.create(slug="nfd")

    # dynamic choice options get cached, so we clear them
    # to ensure the new "gemeinde" options will be valid
    cache.clear()

    # questions
    caluma_form_models.Question.objects.create(
        slug="gemeinde",
        type=caluma_form_models.Question.TYPE_DYNAMIC_CHOICE,
        data_source="Municipalities",
    )
    settings.DATA_SOURCE_CLASSES = [
        "camac.caluma.extensions.data_sources.Municipalities"
    ]

    for slug in ["papierdossier", "projektaenderung"]:
        question = caluma_form_models.Question.objects.create(
            slug=slug, type=caluma_form_models.Question.TYPE_CHOICE
        )
        options = [
            caluma_form_models.Option.objects.create(slug=f"{slug}-ja", label="Ja"),
            caluma_form_models.Option.objects.create(slug=f"{slug}-nein", label="Nein"),
        ]
        for option in options:
            caluma_form_models.QuestionOption.objects.create(
                question=question, option=option
            )

    # some question for suggestions
    question = caluma_form_models.Question.objects.create(
        slug="baubeschrieb", type=caluma_form_models.Question.TYPE_MULTIPLE_CHOICE
    )
    caluma_form_models.QuestionOption.objects.create(
        question=question,
        option=caluma_form_models.Option.objects.create(
            slug="baubeschrieb-erweiterung-anbau", label="Erweiterung Anbau"
        ),
    )
    caluma_form_models.QuestionOption.objects.create(
        question=question,
        option=caluma_form_models.Option.objects.create(
            slug="baubeschrieb-um-ausbau", label="Um- oder Ausbau"
        ),
    )
    question = caluma_form_models.Question.objects.create(
        slug="art-versickerung-dach", type=caluma_form_models.Question.TYPE_TEXT
    )

    # sb1 and sb2
    applicant_table = caluma_form_models.Form.objects.create(slug="personalien-tabelle")
    caluma_form_models.Question.objects.create(
        slug="personalien-sb",
        type=caluma_form_models.Question.TYPE_TABLE,
        row_form=applicant_table,
    )
    caluma_form_models.Question.objects.create(
        slug="personalien-gesuchstellerin",
        type=caluma_form_models.Question.TYPE_TABLE,
        row_form=applicant_table,
    )
    caluma_form_models.Question.objects.create(
        slug="personalien-sb1-sb2",
        type=caluma_form_models.Question.TYPE_TABLE,
        row_form=applicant_table,
    )
    caluma_form_models.Question.objects.create(
        slug="name-sb", type=caluma_form_models.Question.TYPE_TEXT
    )
    caluma_form_models.Question.objects.create(
        slug="name-applicant", type=caluma_form_models.Question.TYPE_TEXT
    )

    # link questions with forms
    for form_id, question_id in FORM_QUESTION_MAP:
        caluma_form_models.FormQuestion.objects.create(
            form_id=form_id, question_id=question_id
        )
