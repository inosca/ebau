from collections import defaultdict

from caluma.caluma_user.models import AnonymousUser
from caluma.caluma_workflow.models import Task
from caluma.caluma_workflow.utils import create_work_items
from django.core.management.base import BaseCommand
from django.db import transaction

from camac.instance.models import Instance

WITHDRAWAL_LIGHT_INSTANCE_STATES = [
    "subm",
    "init-distribution",
    "circulation",
    "correction",
    "decision",
]

WITHDRAWAL_LIGHT_TASK = "withdrawal-request"


def states(string) -> list[str]:
    return [state.strip() for state in string.split(",")]


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = AnonymousUser(username="admin")
        self.fixed_instances = defaultdict(list)

    def add_arguments(self, parser) -> None:
        parser.add_argument("--dry", action="store_true", dest="dry")
        parser.add_argument("--instance", default=None, type=int)
        parser.add_argument("--instance_states", default=None, type=states)
        parser.add_argument("--withdrawal_task", default=None, type=str)

    def get_instance_filters(self, path="pk") -> dict:
        return {path: self.instance} if self.instance else {}

    @transaction.atomic
    def handle(self, *args, **options):
        tid = transaction.savepoint()

        self.instance = options["instance"]
        self.instance_states = (
            options["instance_states"] or WITHDRAWAL_LIGHT_INSTANCE_STATES
        )
        self.withdrawal_task = options["withdrawal_task"] or WITHDRAWAL_LIGHT_TASK

        self.fix_missing_work_item()

        if len(self.fixed_instances.keys()):
            self.stdout.write("")
            self.stdout.write(
                self.style.SUCCESS(
                    f"Fixed {len(self.fixed_instances.keys())} instances:"
                )
            )
            for instance_id, reasons in sorted(self.fixed_instances.items()):
                instance = Instance.objects.get(pk=instance_id)
                municipality = instance.responsible_service(filter_type="municipality")

                self.stdout.write(
                    "- "
                    + self.style.SUCCESS(str(instance.pk))
                    + f", {instance.instance_state.get_name()}, {municipality.get_name()}, "
                    + self.style.ERROR(", ".join(reasons))
                )

        if options.get("dry"):
            transaction.savepoint_rollback(tid)
        else:
            transaction.savepoint_commit(tid)

    def fix_missing_work_item(self) -> None:
        for instance in Instance.objects.filter(
            instance_state__name__in=self.instance_states,
            **self.get_instance_filters(),
        ).order_by("instance_state__name"):
            case = instance.case

            # Do not overwrite existing tasks in ready or complete
            if case.work_items.filter(task_id=self.withdrawal_task).exists():
                continue

            create_work_items(
                Task.objects.filter(pk=self.withdrawal_task), case, self.user
            )

            self.fixed_instances[instance.pk].append(
                f'Missing work item: "{self.withdrawal_task}"'
            )
            self.stdout.write(
                self.style.WARNING(
                    f"{instance.pk} ({instance.instance_state.get_name()}):"
                )
            )
            self.stdout.write(
                self.style.SUCCESS(f"\tCreated: '{self.withdrawal_task}'")
            )
