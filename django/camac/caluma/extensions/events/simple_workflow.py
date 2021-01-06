import reversion
from caluma.caluma_core.events import on
from caluma.caluma_workflow.events import post_complete_work_item
from django.db import transaction

from camac.core.utils import create_history_entry
from camac.instance.models import InstanceState
from camac.user.models import User

from .general import get_caluma_setting, get_instance


@on(post_complete_work_item)
@transaction.atomic
def post_complete_simple_workflow(sender, work_item, user, context, **kwargs):
    simple_workflow_config = get_caluma_setting("SIMPLE_WORKFLOW", {})

    if work_item.task_id in simple_workflow_config.keys():
        instance = get_instance(work_item)
        camac_user = User.objects.get(username=user.username)

        config = simple_workflow_config[work_item.task_id]

        next_instance_state = config.get("next_instance_state")
        ech_event = config.get("ech_event")
        history_text = config.get("history_text")

        if next_instance_state:
            with reversion.create_revision():
                reversion.set_user(camac_user)

                # go to next instance state
                instance.previous_instance_state = instance.instance_state
                instance.instance_state = InstanceState.objects.get(
                    name=next_instance_state
                )
                instance.save()

        if ech_event:
            # trigger ech message for status change
            ech_event.send(
                sender=f"post_complete_{work_item.task_id.replace('-', '_')}",
                instance=instance,
                user_pk=camac_user.pk,
                group_pk=context.get("group-id"),
            )

        if history_text:
            # create history entry
            create_history_entry(instance, camac_user, history_text)
