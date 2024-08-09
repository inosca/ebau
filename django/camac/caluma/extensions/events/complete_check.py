import reversion
from caluma.caluma_core.events import filter_events, on
from caluma.caluma_workflow.events import post_complete_work_item
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
        form_type_answer = work_item.case.document.answers.get(question_id="form-type")
        form_type_answer.value = "form-type-baubewilligungsverfahren"
        form_type_answer.save()

        with reversion.create_revision():
            camac_user = User.objects.get(username=user.username)
            reversion.set_user(camac_user)
            work_item.case.instance.form_id = uri_constants.FORM_BAUGESUCH
            work_item.case.instance.save()
