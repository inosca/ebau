import datetime
from typing import Callable

import pytest
from caluma.caluma_form import (
    factories as caluma_form_factories,
    models as caluma_form_models,
)
from dateutil import relativedelta
from django.urls import reverse

from camac.instance.serializers import SUBMIT_DATE_FORMAT


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
def nfd_tabelle_document_row(nfd_tabelle_form: caluma_form_models.Form) -> Callable:
    def wrapper(service_id, status, date_request=None, date_response=None, family=None):
        defaults = {}
        document = caluma_form_factories.DocumentFactory(
            form=nfd_tabelle_form, **defaults
        )
        caluma_form_factories.AnswerFactory(
            document=document, question_id="nfd-tabelle-behoerde", value=service_id
        )
        caluma_form_factories.AnswerFactory(
            document=document, question_id="nfd-tabelle-status", value=status
        )
        return document

    return wrapper


def test_summary_instances(admin_client, instance_factory, case_factory):
    num_instances = 5
    instances = instance_factory.create_batch(num_instances)
    run = 0
    cases = []
    for inst in instances:
        submit_date = inst.creation_date
        submit_date = submit_date - relativedelta.relativedelta(years=run % 3)
        cases.append(
            case_factory.create(
                instance=inst,
                meta={
                    "submit-date": submit_date.strftime(SUBMIT_DATE_FORMAT),
                },
            )
        )
        run += 1
    url = reverse("instances-summary")
    response = admin_client.get(url)
    assert response.json() == num_instances


@pytest.mark.parametrize(
    "role__name,expected", [("Support", 2), ("Municipality", 1), ("Service", 0)]
)
def test_summary_claims(
    service_factory,
    admin_client,
    role,
    group,
    nfd_tabelle_document_row,
    expected,  # noqa
):
    nfd_tabelle_document_row(group.service_id, "nfd-tabelle-status-beantwortet")
    nfd_tabelle_document_row(group.service_id, "nfd-tabelle-status-entwurf")
    nfd_tabelle_document_row(service_factory().pk, "nfd-tabelle-status-beantwortet")
    url = reverse("claims-summary")
    response = admin_client.get(url)
    result = response.json()
    assert result == expected


@pytest.mark.parametrize(
    "role__name,expected_proc_time_avg,expected_deadline_quota,expected_num_queries",
    [
        ("Support", 7 * 60 * 60 * 24, round(2 / 3 * 100, 2), 2),
        ("Service", 9 * 60 * 60 * 24, 50.0, 2),
        ("Applicant", None, None, 1),
    ],
)
def test_activation_summary(
    db,
    activation_factory,
    service_factory,
    role,
    admin_client,
    group,
    django_assert_num_queries,
    expected_proc_time_avg,
    expected_deadline_quota,
    expected_num_queries,
):
    activation_factory(
        service=group.service,
        circulation_state__name="DONE",
        start_date=datetime.datetime(2020, 7, 11),
        end_date=datetime.datetime(2020, 7, 15),
        deadline_date=datetime.datetime(2020, 7, 20),
    )
    activation_factory(
        service=group.service,
        circulation_state__name="DONE",
        start_date=datetime.datetime(2020, 7, 11),
        end_date=datetime.datetime(2020, 7, 25),
        deadline_date=datetime.datetime(2020, 7, 20),
    )
    activation_factory(
        service=service_factory(),
        circulation_state__name="DONE",
        start_date=datetime.datetime(2020, 7, 11),
        end_date=datetime.datetime(2020, 7, 14),
        deadline_date=datetime.datetime(2020, 7, 20),
    )
    activation_factory(
        service=service_factory(),
        circulation_state__name="OPEN",
        start_date=datetime.datetime(2020, 7, 11),
        deadline_date=datetime.datetime(2020, 7, 15),
    )
    with django_assert_num_queries(expected_num_queries):
        response = admin_client.get(reverse("activations-summary"))
    # test: Support gets data for all
    # test: Service gets data for own activations
    # test: other user gets no data
    result = response.json()
    assert result["avg-processing-time"] == expected_proc_time_avg
    assert result["deadline-quota"] == expected_deadline_quota
