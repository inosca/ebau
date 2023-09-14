from caluma.caluma_core.events import on
from caluma.caluma_workflow.api import start_case
from caluma.caluma_workflow.events import post_create_work_item
from caluma.caluma_workflow.models import Workflow
from django.conf import settings
from django.db import transaction

from camac.caluma.utils import filter_by_task_base


def get_additional_demand_settings(settings_keys):
    return filter(
        None,
        [
            settings.ADDITIONAL_DEMAND.get(settings_key)
            for settings_key in (
                [settings_keys]
                if not isinstance(settings_keys, list)
                else settings_keys
            )
        ],
    )


def filter_by_task(settings_keys):
    return filter_by_task_base(settings_keys, get_additional_demand_settings)


@on(post_create_work_item, raise_exception=True)
@filter_by_task("ADDITIONAL_DEMAND_TASK")
@transaction.atomic
def post_create_additional_demand(sender, work_item, user, context=None, **kwargs):
    # start child case
    start_case(
        workflow=Workflow.objects.get(
            pk=settings.ADDITIONAL_DEMAND["ADDITIONAL_DEMAND_WORKFLOW"]
        ),
        user=user,
        parent_work_item=work_item,
        context=context,
        created_by_user=user.group,
        created_by_group=user.group,
        modified_by_user=user.group,
        modified_by_group=user.group,
    )
