from caluma.caluma_core.events import filter_events, on
from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Question
from caluma.caluma_workflow.events import post_complete_work_item
from django.conf import settings
from django.db import transaction

from camac.caluma.extensions.events.simple_workflow import send_notification
from camac.constants import kt_uri as uri_constants


@on(post_complete_work_item, raise_exception=True)
@transaction.atomic
@filter_events(
    lambda work_item: work_item.task.slug == "complete-check"
    and settings.APPLICATION_NAME == "kt_uri"
)
def convert_instance_ur(sender, work_item, user, context=None, **kwargs):
    requires_building_permit = False

    if complete_check_answer := work_item.document.answers.filter(
        question_id="complete-check-baubewilligungspflichtig"
    ).first():
        requires_building_permit = (
            complete_check_answer.value
            == "complete-check-baubewilligungspflichtig-baubewilligungspflichtig"
        )

    if (
        work_item.case.instance.form_id
        in [
            uri_constants.FORM_MELDUNG_SOLARANLAGE,
            uri_constants.FORM_REKLAME,
            uri_constants.FORM_MELDUNG_GEBAEUDETECHNIK,
        ]
        and requires_building_permit
    ):
        save_answer(
            document=work_item.case.document,
            question=Question.objects.get(
                slug=uri_constants.CALUMA_SPECIAL_FORM_QUESTION_VALUE_MAP[
                    work_item.case.instance.form_id
                ]["question"]
            ),
            value=uri_constants.CALUMA_SPECIAL_FORM_QUESTION_VALUE_MAP[
                work_item.case.instance.form_id
            ]["value"],
            user=user,
        )


@on(post_complete_work_item, raise_exception=True)
@transaction.atomic
@filter_events(
    lambda work_item: work_item.task.slug == "complete-check"
    and settings.APPLICATION_NAME == "kt_uri"
)
def send_notification_after_complete_check(
    sender, work_item, user, context=None, **kwargs
):
    complete_check_answer_value = (
        work_item.document.answers.filter(
            question_id="complete-check-vollstaendigkeitspruefung"
        )
        .values_list("value", flat=True)
        .first()
    )

    if (
        complete_check_answer_value
        == "complete-check-vollstaendigkeitspruefung-complete"
    ):
        instance = work_item.case.family.instance

        send_notification(
            notification={
                "template_slug": "3-1-dossier-angenommen",
                "recipient_types": ["applicant"],
            },
            context=context,
            instance=instance,
            user=user,
            work_item=work_item,
        )
