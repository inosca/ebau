from caluma.caluma_core.events import on
from caluma.caluma_workflow.events import post_create_work_item
from django.conf import settings
from django.db import transaction

from camac.caluma.event_utils import filter_by_task, setting
from camac.user.models import User

from .general import get_instance


@on(post_create_work_item, raise_exception=True)
@filter_by_task(setting("REJECTION", "WORK_ITEM.TASK"))
@transaction.atomic
def post_create_reject_work_item(sender, work_item, user, context, **kwargs):
    get_instance(work_item, context).set_instance_state(
        settings.REJECTION["WORK_ITEM"]["INSTANCE_STATE"],
        User.objects.get(username=user.username),
    )
