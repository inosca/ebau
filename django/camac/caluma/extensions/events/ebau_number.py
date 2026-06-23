from caluma.caluma_core.events import on
from caluma.caluma_workflow.events import post_complete_work_item
from django.db import transaction
from django.utils.translation import gettext_noop

from camac.caluma.event_utils import (
    application_setting,
    filter_by_canton,
    filter_by_task,
)
from camac.core.utils import create_history_entry
from camac.ech0211.signals import assigned_ebau_number
from camac.user.models import User

from .general import get_instance


@on(post_complete_work_item, raise_exception=True)
@filter_by_canton("kt_bern")
@filter_by_task(application_setting("CALUMA.EBAU_NUMBER_TASK"))
@transaction.atomic
def post_complete_ebau_number(sender, work_item, user, context, **kwargs):
    instance = get_instance(work_item)
    camac_user = User.objects.get(username=user.username)

    if instance.instance_state.name == "subm":
        # set instance state
        instance.set_instance_state("circulation_init", camac_user)

        # trigger ech event
        assigned_ebau_number.send(
            sender="post_complete_work_item",
            instance=instance,
            user_pk=camac_user.pk,
            group_pk=user.camac_group,
        )

    # create history entry
    if not context or not context.get("no-history"):
        create_history_entry(instance, camac_user, gettext_noop("Assigned ebau number"))
