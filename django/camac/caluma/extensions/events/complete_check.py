import reversion
from caluma.caluma_core.events import filter_events, on
from caluma.caluma_workflow.api import skip_work_item
from caluma.caluma_workflow.events import post_complete_work_item, post_create_work_item
from django.conf import settings
from django.db import transaction

from camac.constants import kt_uri as uri_constants
from camac.user.models import User


@on(post_complete_work_item, raise_exception=True)
@transaction.atomic
@filter_events(lambda work_item: work_item.task.slug == "complete-check")
def convert_instance_ur(sender, work_item, user, context=None, **kwargs):
    if settings.APPLICATION_NAME != "kt_uri":  # pragma: no cover
        return

    requires_building_permit = (
        work_item.document.answers.get(
            question_id="complete-check-baubewilligungspflichtig"
        ).value
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
        form_type_answer = work_item.case.document.answers.get(question_id="form-type")
        form_type_answer.value = "form-type-baubewilligungsverfahren"
        form_type_answer.save()

        with reversion.create_revision():
            camac_user = User.objects.get(username=user.username)
            reversion.set_user(camac_user)
            work_item.case.instance.form_id = uri_constants.FORM_BAUGESUCH
            work_item.case.instance.save()


@on(post_create_work_item, raise_exception=True)
@transaction.atomic
@filter_events(lambda work_item: work_item.task.slug == "complete-distribution")
def skip_circulation_ur(sender, work_item, user, context, **kwargs):
    if settings.APPLICATION_NAME != "kt_uri":
        return

    complete_check_document = work_item.case.parent_work_item.case.work_items.get(
        task_id="complete-check"
    ).document
    requires_circulation = (
        complete_check_document.answers.get(
            question_id="complete-check-baubewilligungspflichtig"
        ).value
        == "complete-check-baubewilligungspflichtig-baubewilligungspflichtig"
    )

    if not requires_circulation:
        skip_work_item(work_item=work_item, user=user, context=context)
