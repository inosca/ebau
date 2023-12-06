from caluma.caluma_core.events import on
from caluma.caluma_workflow.events import post_complete_work_item
from django.db import transaction
from django.utils.module_loading import import_string

from camac.core.utils import create_history_entry
from camac.notification.utils import send_mail_without_request
from camac.user.models import User

from .general import get_caluma_setting, get_instance


@on(post_complete_work_item, raise_exception=True)
@transaction.atomic
def post_complete_simple_workflow(sender, work_item, user, context, **kwargs):
    simple_workflow_config = get_caluma_setting("SIMPLE_WORKFLOW", {})

    if work_item.task_id in simple_workflow_config.keys():
        instance = get_instance(work_item)
        camac_user = User.objects.get(username=user.username)

        config = simple_workflow_config[work_item.task_id]

        next_instance_state = config.get("next_instance_state")
        ech_event_name = config.get("ech_event")
        ech_event = import_string(ech_event_name) if ech_event_name else None

        history_text = config.get("history_text")
        notification = config.get("notification")

        if next_instance_state:
            # go to next instance state
            instance.set_instance_state(next_instance_state, camac_user)

        if ech_event:
            # trigger ech message for status change
            ech_event.send(
                sender=f"post_complete_{work_item.task_id.replace('-', '_')}",
                instance=instance,
                user_pk=camac_user.pk,
                group_pk=user.camac_group,
            )

        if history_text and (not context or not context.get("no-history")):
            # create history entry
            create_history_entry(instance, camac_user, history_text)

        if notification and (not context or not context.get("no-notification")):
            # check conditions
            if "conditions" in notification:
                for type, config in notification["conditions"].items():
                    if type == "forms":
                        if instance.case.document.form.slug not in config:
                            return
                    else:  # pragma: no cover
                        raise RuntimeError(f"unknown condition type: {type}")

            additional_data = (
                {"body": context.get("notification-body")}
                if context and context.get("notification-body")
                else {}
            )

            send_mail_without_request(
                notification["template_slug"],
                user.username,
                user.camac_group,
                instance={"id": instance.pk, "type": "instances"},
                recipient_types=notification["recipient_types"],
                work_item={"id": work_item.pk, "type": "work-items"},
                **additional_data,
            )
