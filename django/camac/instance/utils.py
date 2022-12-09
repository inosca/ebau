from caluma.caluma_form.models import Answer, AnswerDocument, Option, Question
from caluma.caluma_workflow.models import WorkItem
from django.db.models import Prefetch
from django.utils.translation import gettext as _

from camac.caluma.api import CalumaApi
from camac.constants.kt_bern import (
    DECISION_TYPE_BAUBEWILLIGUNGSFREI,
    DECISION_TYPE_CONSTRUCTION_TEE_WITH_RESTORATION,
    DECISION_TYPE_PARTIAL_PERMIT_WITH_PARTIAL_CONSTRUCTION_TEE_AND_PARTIAL_RESTORATION,
    DECISIONS_BEWILLIGT,
)
from camac.instance.models import Instance
from camac.user.models import Service


def get_construction_control(service):
    """Get construction control matching a given lead authority."""
    try:
        return Service.objects.get(
            service_group__name="construction-control",
            trans__language="de",
            trans__name=service.trans.get(language="de").name.replace(
                "Leitbehörde", "Baukontrolle"
            ),
        )
    except Service.DoesNotExist:  # pragma: no cover
        raise Exception(
            _(
                "Could not find construction control for service %(id)d"
                % {"id": service.pk}
            )
        )


def set_construction_control(instance: Instance) -> Service:
    involved_municipalities = instance.instance_services.filter(
        service__service_group__name="municipality"
    )
    active_municipality = involved_municipalities.filter(active=1).first()

    if active_municipality:
        # active service is a municipality, take this one
        municipality = active_municipality.service
    elif involved_municipalities.exists():
        # active service is an RSTA, take involved (but not active) municipality
        municipality = involved_municipalities.first().service
    else:
        # no involved municipality, take fallback from form
        municipality = Service.objects.get(pk=CalumaApi().get_municipality(instance))

    construction_control = get_construction_control(municipality)
    instance.instance_services.create(service=construction_control, active=1)

    return construction_control


def should_continue_after_decision(instance: Instance, work_item: WorkItem) -> bool:
    answers = work_item.document.answers
    decision = answers.get(question_id="decision-decision-assessment").value

    try:
        decision_type = answers.get(question_id="decision-approval-type").value
    except Answer.DoesNotExist:
        decision_type = None

    return (
        decision == DECISIONS_BEWILLIGT
        and decision_type != DECISION_TYPE_BAUBEWILLIGUNGSFREI
    ) or decision_type in [
        DECISION_TYPE_CONSTRUCTION_TEE_WITH_RESTORATION,
        DECISION_TYPE_PARTIAL_PERMIT_WITH_PARTIAL_CONSTRUCTION_TEE_AND_PARTIAL_RESTORATION,
    ]


def build_document_prefetch_statements(prefix="", prefetch_options=False):
    """Build needed prefetch statements to performantly fetch a document.

    This is needed to reduce the query count when almost all the form data
    is needed for a given document, e.g. when exporting a PDF or listing public
    instances (master data).
    """

    question_queryset = Question.objects.select_related(
        "sub_form", "row_form"
    ).order_by("-formquestion__sort")

    if prefetch_options:
        question_queryset = question_queryset.prefetch_related(
            Prefetch(
                "options",
                queryset=Option.objects.order_by("-questionoption__sort"),
            )
        )

    if prefix:
        prefix += "__"

    return [
        f"{prefix}answers",
        f"{prefix}dynamicoption_set",
        Prefetch(
            f"{prefix}answers__answerdocument_set",
            queryset=AnswerDocument.objects.select_related("document__form")
            .prefetch_related("document__answers", "document__form__questions")
            .order_by("-sort"),
        ),
        Prefetch(
            # root form -> questions
            f"{prefix}form__questions",
            queryset=question_queryset.prefetch_related(
                Prefetch(
                    # root form -> row forms -> questions
                    "row_form__questions",
                    queryset=question_queryset,
                ),
                Prefetch(
                    # root form -> sub forms -> questions
                    "sub_form__questions",
                    queryset=question_queryset.prefetch_related(
                        Prefetch(
                            # root form -> sub forms -> row forms -> questions
                            "row_form__questions",
                            queryset=question_queryset,
                        ),
                        Prefetch(
                            # root form -> sub forms -> sub forms -> questions
                            "sub_form__questions",
                            queryset=question_queryset.prefetch_related(
                                Prefetch(
                                    # root form -> sub forms -> sub forms -> row forms -> questions
                                    "row_form__questions",
                                    queryset=question_queryset,
                                ),
                            ),
                        ),
                    ),
                ),
            ),
        ),
    ]
