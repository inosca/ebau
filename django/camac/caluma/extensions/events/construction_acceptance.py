from caluma.caluma_core.events import filter_events, on
from caluma.caluma_workflow.events import post_complete_work_item
from django.conf import settings
from django.db import transaction

from camac.notification.utils import send_mail_without_request
from camac.permissions import events as permissions_events
from camac.permissions.config.kt_gr import gr_include_aib

from .general import get_instance


@on(post_complete_work_item, raise_exception=True)
@transaction.atomic
@filter_events(lambda work_item: work_item.task.slug == "construction-acceptance")
def post_complete_construction_acceptance(sender, work_item, user, context, **kwargs):
    notification_config = settings.APPLICATION["NOTIFICATIONS"].get(
        "CONSTRUCTION_ACCEPTANCE", []
    )

    instance = get_instance(work_item)
    permissions_events.Trigger.construction_acceptance_completed(None, instance)

    if instance.case.document.form.slug not in [
        "baugesuch",
        "solaranlage",
        "bauanzeige",
    ]:
        return

    if not gr_include_aib(instance):
        notification_config = [
            config
            for config in notification_config
            if config["recipient_types"] != ["aib"]
        ]

    if not context or not context.get("no-notification"):
        for config in notification_config:
            send_mail_without_request(
                config["template_slug"],
                user.username,
                user.camac_group,
                instance={"id": instance.pk, "type": "instances"},
                recipient_types=config["recipient_types"],
            )
