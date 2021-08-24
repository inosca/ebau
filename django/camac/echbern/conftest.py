import pytest
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_workflow import api as workflow_api, models as caluma_workflow_models

from camac.constants.kt_bern import QUESTION_EBAU_NR
from camac.echbern.data_preparation import slugs_baugesuch, slugs_vorabklaerung_einfach
from camac.instance.serializers import SUBMIT_DATE_FORMAT


@pytest.fixture
def ech_instance(
    db,
    admin_user,
    instance_service_factory,
    service_t_factory,
    camac_answer_factory,
    caluma_workflow_config_be,
):
    inst_serv = instance_service_factory(
        instance__user=admin_user,
        instance__pk=2323,
        service__name=None,
        service__city=None,
        service__zip="3400",
        service__address="Teststrasse 23",
        service__email="burgdorf@example.com",
        service__pk=2,
        service__trans=None,
        service__service_group__name="municipality",
        active=1,
    )

    service_t_factory(
        service=inst_serv.service,
        language="de",
        name="Leitbehörde Burgdorf",
        city="Burgdorf",
    )

    camac_answer_factory(
        instance=inst_serv.instance, question__pk=QUESTION_EBAU_NR, answer="2020-1"
    )

    return inst_serv.instance


@pytest.fixture
def ech_instance_case(ech_instance, caluma_admin_user):
    def wrapper(is_vorabklaerung=False):
        workflow_slug = (
            "preliminary-clarification" if is_vorabklaerung else "building-permit"
        )

        case = workflow_api.start_case(
            workflow=caluma_workflow_models.Workflow.objects.get(pk=workflow_slug),
            form=caluma_form_models.Form.objects.get(slug="main-form"),
            user=caluma_admin_user,
            meta={
                "submit-date": ech_instance.creation_date.strftime(SUBMIT_DATE_FORMAT),
                "paper-submit-date": ech_instance.creation_date.strftime(
                    SUBMIT_DATE_FORMAT
                ),
            },
        )

        ech_instance.case = case
        ech_instance.save()

        return case

    return wrapper


def fill_document_ech(document, data):
    for question_slug, value in data:
        question = caluma_form_models.Question.objects.get(slug=question_slug)
        if question.type == "dynamic_choice":
            caluma_form_models.DynamicOption.objects.create(
                document=document, question=question, slug=value, label=value
            )
        if question.type == "dynamic_multiple_choice":  # pragma: no cover
            for v in value:
                caluma_form_models.DynamicOption.objects.create(
                    document=document, question=question, slug=v, label=v
                )
        caluma_form_models.Answer.objects.create(
            document=document, value=value, question=question
        )


@pytest.fixture
def vorabklaerung_einfach_filled(
    caluma_config_bern, instance_with_case, instance_factory
):
    instance = instance_with_case(
        instance_factory(),
        workflow="preliminary-clarification",
        form="vorabklaerung-einfach",
    )

    document = instance.case.document
    fill_document_ech(document, slugs_vorabklaerung_einfach["top"])
    return document


@pytest.fixture
def baugesuch_filled(
    caluma_config_bern,
    answer_factory,
    answer_document_factory,
    instance_with_case,
    instance_factory,
):
    instance = instance_with_case(
        instance_factory(), workflow="building-permit", form="baugesuch-generell-v2"
    )

    document = instance.case.document

    for key, data in slugs_baugesuch.items():
        if key == "top":
            fill_document_ech(document, data)
            continue
        t_question = caluma_form_models.Question.objects.get(slug=key)
        t_answer = answer_factory(document=document, question=t_question)
        for row in data:
            row_answer_doc = answer_document_factory(answer=t_answer)
            fill_document_ech(row_answer_doc.document, row)

    return document
