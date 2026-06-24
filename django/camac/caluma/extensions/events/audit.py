from caluma.caluma_core.events import on
from caluma.caluma_workflow.events import post_complete_work_item, post_skip_work_item
from django.db import transaction
from django.utils.translation import gettext_noop

from camac.caluma.event_utils import (
    application_setting,
    filter_by_canton,
    filter_by_task,
)
from camac.core.utils import create_history_entry
from camac.user.models import User

from .general import get_instance


@on([post_complete_work_item, post_skip_work_item], raise_exception=True)
@filter_by_canton("kt_bern")
@filter_by_task(application_setting("CALUMA.AUDIT_TASK"))
@transaction.atomic
def post_complete_audit(sender, work_item, user, context, **kwargs):
    if not context or not context.get("no-history"):
        create_history_entry(
            instance=get_instance(work_item),
            user=User.objects.get(username=user.username),
            text=(
                gettext_noop("Exam skipped")
                if sender == "post_skip_work_item"
                else gettext_noop("Exam completed")
            ),
        )
