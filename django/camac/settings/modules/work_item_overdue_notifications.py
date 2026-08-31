from camac.settings.ebau_schema import ModuleConfig
from camac.settings.modules.work_item_overdue_notifications_schema import (
    OverdueNotificationConfig,
    WorkItemOverdueNotificationsConfig,
)

MANUAL_WORKITEM_OVERDUE = OverdueNotificationConfig(
    template_slug="expired-manual-work-item",
    recipient_types=["work_item_controlling"],
    work_item_allowlist=["create-manual-workitems"],
)

WORK_ITEM_OVERDUE_NOTIFICATIONS = ModuleConfig[WorkItemOverdueNotificationsConfig](
    default=WorkItemOverdueNotificationsConfig(),
    kt_gr=WorkItemOverdueNotificationsConfig(
        enabled=True,
        notifications=[
            MANUAL_WORKITEM_OVERDUE,
        ],
    ),
    kt_so=WorkItemOverdueNotificationsConfig(
        enabled=True,
        notifications=[
            MANUAL_WORKITEM_OVERDUE,
        ],
    ),
)
