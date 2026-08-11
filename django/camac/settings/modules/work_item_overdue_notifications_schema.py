from datetime import datetime
from typing import Self

from pydantic import Field, model_validator

from camac.settings.ebau_schema import EBauConfig, ModuleApplicationConfig
from camac.settings.env import env


class OverdueNotificationConfig(EBauConfig):
    """Configuration for an overdue work item notification."""

    template_slug: str = Field(
        description="Slug of the notification template",
    )
    recipient_types: list[str] = Field(
        description="List of recipient types to send the notification to",
    )
    work_item_allowlist: list[str] | None = Field(
        default=None,
        description="Task slugs whose overdue work items trigger this notification",
    )
    work_item_denylist: list[str] | None = Field(
        default=None,
        description="Task slugs whose overdue work items do not trigger this notification",
    )

    @model_validator(mode="after")
    def validate_work_item_list(self) -> Self:
        if (self.work_item_allowlist is None) == (self.work_item_denylist is None):
            raise ValueError(
                "Exactly one of work_item_allowlist or work_item_denylist must be set."
            )

        return self


class WorkItemOverdueNotificationsConfig(ModuleApplicationConfig):
    """Configuration for overdue work item notifications."""

    process_deadlines_from: datetime | None = Field(
        default=env.str("NOTIFICATIONS_PROCESS_DEADLINES_FROM", default=None),
        validate_default=True,
        description=(
            "Earliest deadline processed when overdue notifications are first enabled"
        ),
    )
    notifications: list[OverdueNotificationConfig] = Field(
        default_factory=list,
        description="Notification blocks with their work item filters",
    )
