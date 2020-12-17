from caluma.caluma_core.events import on
from caluma.caluma_workflow.events import post_complete_work_item, post_skip_work_item
from django.db import transaction
from django.utils.translation import gettext_noop

from camac.core.utils import create_history_entry
from camac.user.models import User

from .general import get_caluma_setting, get_instance


@on(post_skip_work_item)
@on(post_complete_work_item)
@transaction.atomic
def post_complete_audit(sender, work_item, user, **kwargs):
    if work_item.task_id == get_caluma_setting("AUDIT_TASK"):
        create_history_entry(
            instance=get_instance(work_item),
            user=User.objects.get(username=user.username),
            text=(
                gettext_noop("Exam skipped")
                if sender == "post_skip_work_item"
                else gettext_noop("Exam completed")
            ),
        )
