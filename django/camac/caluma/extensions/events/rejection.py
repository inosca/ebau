from caluma.caluma_core.events import filter_events, on
from caluma.caluma_workflow.events import post_create_work_item
from django.conf import settings
from django.db import transaction

from camac.user.models import User

from .general import get_instance


@on(post_create_work_item, raise_exception=True)
@transaction.atomic
@filter_events(
    lambda work_item: work_item.task_id
    == settings.REJECTION.get("WORK_ITEM", {}).get("TASK")
)
def post_create_reject_work_item(sender, work_item, user, context, **kwargs):
    get_instance(work_item, context).set_instance_state(
        settings.REJECTION["WORK_ITEM"]["INSTANCE_STATE"],
        User.objects.get(username=user.username),
    )
