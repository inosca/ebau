import reversion
from caluma.caluma_core.events import on
from caluma.caluma_workflow.events import post_complete_work_item
from django.db import transaction
from django.utils.translation import gettext_noop

from camac.core.utils import create_history_entry
from camac.echbern.signals import assigned_ebau_number
from camac.instance.models import InstanceState
from camac.user.models import User

from .general import get_caluma_setting, get_instance


@on(post_complete_work_item)
@transaction.atomic
def post_complete_ebau_number(sender, work_item, user, context, **kwargs):
    if work_item.task_id == get_caluma_setting("EBAU_NUMBER_TASK"):
        instance = get_instance(work_item)
        camac_user = User.objects.get(username=user.username)

        if instance.instance_state.name == "subm":
            # set instance state
            with reversion.create_revision():
                reversion.set_user(camac_user)
                instance.instance_state = InstanceState.objects.get(
                    name="circulation_init"
                )
                instance.save()

            # trigger ech event
            assigned_ebau_number.send(
                sender="post_complete_work_item",
                instance=instance,
                user_pk=camac_user.pk,
                group_pk=context.get("group-id"),
            )

        # create history entry
        create_history_entry(instance, camac_user, gettext_noop("Assigned ebau number"))
