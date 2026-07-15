from collections.abc import Callable
from typing import Literal

from django.utils.functional import Promise
from pydantic import ConfigDict, Field

from camac.settings.ebau_schema import EBauConfig, ModuleApplicationConfig

type EventType = Literal["created", "completed", "skipped"]

type Ech0211Signal = Literal[
    "camac.ech0211.signals.instance_submitted",
    "camac.ech0211.signals.exam_completed",
    "camac.ech0211.signals.sb1_submitted",
    "camac.ech0211.signals.sb2_submitted",
    "camac.ech0211.signals.circulation_started",
    "camac.ech0211.signals.circulation_ended",
    "camac.ech0211.signals.ruling",
    "camac.ech0211.signals.finished",
    "camac.ech0211.signals.task_send",
    "camac.ech0211.signals.accompanying_report_send",
    "camac.ech0211.signals.file_subsequently",
    "camac.ech0211.signals.change_responsibility",
    "camac.ech0211.signals.assigned_ebau_number",
    "camac.ech0211.signals.rejected",
    "camac.ech0211.signals.rejection_reverted",
    "camac.ech0211.signals.construction_monitoring_started",
    "camac.ech0211.signals.withdrawn",
]


class NotificationConfig(EBauConfig):
    """Configuration for a notification."""

    template_slug: str = Field(
        description="Slug of the notification template",
    )
    recipient_types: list[str] = Field(
        description="List of recipient types to send the notification to",
    )


class EventConfig(EBauConfig):
    """Configuration for an event."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    next_instance_state: str | None = Field(
        description="Slug of the next instance state",
        default=None,
    )
    history_text: str | Promise | None = Field(
        description="Text to be added to the history entry. Can be a string or a lazy translation string",
        default=None,
    )
    ech_event: Ech0211Signal | None = Field(
        description="Slug of the ech0211 signal to be sent",
        default=None,
    )
    notifications: list[NotificationConfig] = Field(
        description="List of notifications to be sent",
        default_factory=list,
    )
    condition: Callable[..., bool] | None = Field(
        description="Condition to be evaluated to potentially skip the event",
        default=None,
    )


class CalumaSimpleWorkflowConfig(ModuleApplicationConfig):
    """Configuration for caluma simple workflows."""

    events: dict[str, dict[EventType, list[EventConfig]]] = Field(
        description=(
            "Events to be created for the application, grouped by task slug and event type"
        ),
        default_factory=dict,
    )

    def get_events(
        self,
        task: str | None = None,
        event: EventType | None = None,
    ) -> list[EventConfig]:
        """Get a filtered list of events matching task/event."""
        task_configs = (
            [self.events.get(task, {})] if task is not None else self.events.values()
        )
        events = []

        for event_configs in task_configs:
            if event is not None:
                events.extend(event_configs.get(event, []))
            else:
                for configs in event_configs.values():
                    events.extend(configs)

        return events

    def disable_notifications(
        self, task: str | None = None, event: EventType | None = None
    ) -> None:
        """Disable notifications for the given task/event."""
        for event_config in self.get_events(task, event):
            event_config.notifications.clear()

    def replace_notifications(
        self, task: str, event: EventType, new_notifications: list[NotificationConfig]
    ) -> None:
        """Replace notifications for the given task/event."""
        current_notifications = self.get_events(task, event)
        if not current_notifications:
            if not self.events.get(task):
                self.events[task] = {}

            self.events[task][event] = [EventConfig(notifications=new_notifications)]

        else:
            for event_config in self.get_events(task, event):
                event_config.notifications = new_notifications

    def override_notifications(
        self,
        task: str | None = None,
        event: EventType | None = None,
        patch: dict[str, str] = None,
    ) -> None:
        """Override partial notifications for the given task/event."""
        for event_config in self.get_events(task, event):
            for key, value in patch.items():
                for notification in event_config.notifications:
                    if hasattr(notification, key):
                        setattr(notification, key, value)

    def replace_events(
        self, task: str, event: EventType, new_events: list[EventConfig]
    ) -> None:
        """Replace complete events for the given task/event.

        Using this method allows you to also replace condtions, next_instance_state,
        history_text and ech_event.
        """
        if task not in self.events:
            self.events[task] = {}
        self.events[task][event] = new_events
