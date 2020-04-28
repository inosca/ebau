import pytest
from caluma.caluma_form import models as caluma_form_models
from django.conf import settings

from camac.constants.kt_bern import (
    QUESTION_EBAU_NR,
    SERVICE_GROUP_LEITBEHOERDE_GEMEINDE,
)
from camac.echbern.data_preparation import slugs_baugesuch, slugs_vorabklaerung_einfach
from camac.instance.models import Instance


@pytest.fixture
def ech_instance(
    db, admin_user, instance_service_factory, service_t_factory, camac_answer_factory
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
        service__service_group__pk=SERVICE_GROUP_LEITBEHOERDE_GEMEINDE,
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
def vorabklaerung_einfach_filled(caluma_config_bern, document_factory, answer_factory):
    form = caluma_form_models.Form.objects.get(slug="vorabklaerung-einfach")
    document = document_factory(form=form)
    fill_document_ech(document, slugs_vorabklaerung_einfach["top"])
    document.meta = {"camac-instance-id": 2}
    document.save()
    return document


@pytest.fixture
def baugesuch_filled(
    caluma_config_bern, document_factory, answer_factory, answer_document_factory
):
    form = caluma_form_models.Form.objects.get(slug="baugesuch-generell")
    document = document_factory(form=form)

    for key, data in slugs_baugesuch.items():
        if key == "top":
            fill_document_ech(document, data)
            continue
        t_question = caluma_form_models.Question.objects.get(slug=key)
        t_answer = answer_factory(document=document, question=t_question)
        for row in data:
            row_answer_doc = answer_document_factory(answer=t_answer)
            fill_document_ech(row_answer_doc.document, row)

    document.meta = {"camac-instance-id": 1}
    document.save()
    return document


@pytest.fixture(autouse=True)
def service_filter_settings(application_settings, mocker):
    application_settings["ACTIVE_SERVICE_FILTERS"] = settings.APPLICATIONS["kt_bern"][
        "ACTIVE_SERVICE_FILTERS"
    ]
    application_settings["ACTIVE_BAUKONTROLLE_FILTERS"] = settings.APPLICATIONS[
        "kt_bern"
    ]["ACTIVE_BAUKONTROLLE_FILTERS"]

    def responsible_service_demo_side_effects(self):
        return self._responsible_service_kt_bern()

    mocker.patch.object(
        Instance,
        "_responsible_service_demo",
        responsible_service_demo_side_effects,
        create=True,
    )
