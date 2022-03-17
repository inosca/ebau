from datetime import timedelta

from caluma.caluma_form.models import Document, Form
from caluma.caluma_user.models import AnonymousUser
from caluma.caluma_workflow import api as caluma_workflow_api
from caluma.caluma_workflow.events import post_complete_work_item, post_skip_work_item
from caluma.caluma_workflow.models import Case, Task, Workflow, WorkItem
from caluma.caluma_workflow.utils import get_jexl_groups
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count, Q
from django.utils import timezone

from camac.caluma.api import CalumaApi
from camac.caluma.extensions.events.circulation import (
    post_complete_circulation_work_item,
)
from camac.core.models import PublicationEntry
from camac.instance.models import Instance, InstanceResponsibility


class Command(BaseCommand):
    help = "Create an caluma case and work items for every instance"

    def add_arguments(self, parser):
        parser.add_argument(
            "--only-creation-log",
            dest="only_creation_log",
            action="store_true",
            default=False,
        )

    def create_work_item_from_task(
        self,
        case,
        task_slug,
        meta={},
        child_case=None,
        context={},
        deadline=None,
        instance=None,
        applicant=False,
        additional_filters={},
    ):
        task = Task.objects.get(pk=task_slug)

        if WorkItem.objects.filter(case=case, task=task, **additional_filters).exists():
            if self.verbose:
                self.stdout.write(
                    f"{task_slug} work item on case {case.pk} exists skipping"
                )
            return

        if (
            task_slug == "publication"
            and PublicationEntry.objects.filter(
                instance=instance, is_published=1
            ).exists()
        ):
            if self.verbose:
                self.stdout.write(
                    f"Publication was finished on instance {instance.pk} skipping publication task creation"
                )
            return

        meta = {
            "migrated": True,
            "not-viewed": True,
            "notify-deadline": True,
            "notify-completed": False,
            **meta,
        }

        if not deadline and task.lead_time:
            deadline = timezone.now() + timedelta(seconds=task.lead_time)

        addressed_groups = get_jexl_groups(
            task.address_groups, task, case, AnonymousUser(), None, context
        )

        responsible_user = []
        if instance:
            responsibility = InstanceResponsibility.objects.filter(
                instance=instance, service__pk=addressed_groups[0]
            ).first()
            if responsibility:
                responsible_user = [responsibility.user.username]

        if applicant:
            addressed_groups.append("applicant")

        work_item = WorkItem.objects.create(
            case=case,
            task=task,
            meta=meta,
            name=task.name,
            status=WorkItem.STATUS_READY,
            child_case=child_case,
            deadline=deadline,
            addressed_groups=addressed_groups,
            controlling_groups=get_jexl_groups(
                task.control_groups, task, case, AnonymousUser(), None, context
            ),
            assigned_users=responsible_user,
        )

        self.stdout.write(f"Created work item {work_item.pk} {work_item.name}")

        return work_item

    def migrate_circulation(self, instance, case):
        if self.verbose:
            self.stdout.write(f"Migrating instance {instance.pk} circulations")

        circulations = instance.circulations.annotate(
            not_idle_activations=Count(
                "activations", filter=~Q(activations__circulation_state__name="IDLE")
            )
        )

        # create all circulation work items first
        for circulation in circulations.filter(not_idle_activations__gte=1):
            self.create_work_item_from_task(
                case,
                "circulation",
                meta={"circulation-id": circulation.pk},
                instance=instance,
                context={"circulation-id": circulation.pk},
                additional_filters={"meta__circulation-id": circulation.pk},
            )

        # sync them later when all work items are created to avoid creating a
        # broken workflow state
        for circulation in circulations.filter(not_idle_activations__gte=1):
            CalumaApi().sync_circulation(circulation, AnonymousUser())

            for activation in circulation.activations.filter(
                circulation_state__name="REVIEW"
            ):
                work_item = WorkItem.objects.filter(
                    **{
                        "meta__activation-id": activation.pk,
                        "task_id": "write-statement",
                    }
                ).first()

                if not work_item.status == WorkItem.STATUS_READY:
                    # Check statement work item was already skipped - continue
                    continue

                caluma_workflow_api.skip_work_item(
                    work_item,
                    AnonymousUser(),
                    {"circulation-id": circulation.pk, "activation-id": activation.pk},
                )

                self.stdout.write(
                    f"Skipped work item 'check-statement' for activation {activation.pk} that's already in review"
                )

    @transaction.atomic
    def handle(self, *args, **options):  # noqa: C901
        self.verbose = not options["only_creation_log"]

        self.stdout.write("Starting Instance to Caluma Case and WorkItem migration")

        post_complete_work_item.disconnect(post_complete_circulation_work_item)
        post_skip_work_item.disconnect(post_complete_circulation_work_item)

        for instance in Instance.objects.all():
            if self.verbose:
                self.stdout.write(f"Migrating instance {instance.pk}")
            instance_state = instance.instance_state.name
            case_status = Case.STATUS_RUNNING

            if instance_state in ["arch", "del"]:
                case_status = Case.STATUS_COMPLETED

            document = Document.objects.create(form=Form.objects.get(pk="baugesuch"))
            workflow = Workflow.objects.get(pk="building-permit")

            case = Case.objects.get_or_create(
                defaults={
                    "workflow": workflow,
                    "status": case_status,
                    "document": document,
                    "created_at": instance.creation_date,
                    "modified_at": instance.modification_date,
                    "meta": {"migrated": True, "camac-instance-id": instance.pk},
                },
                **{"meta__camac-instance-id": instance.pk},
            )[0]
            if self.verbose:
                self.stdout.write(f"Using case {case.pk}")

            if instance_state == "new":
                self.create_work_item_from_task(case, "submit")
            elif instance_state == "rejected":
                self.create_work_item_from_task(case, "formal-addition", applicant=True)
                self.create_work_item_from_task(case, "create-manual-workitems")
                self.create_work_item_from_task(case, "depreciate-case")
            elif instance_state == "subm":
                self.create_work_item_from_task(case, "reject-form", instance=instance)
                self.create_work_item_from_task(
                    case, "complete-check", instance=instance
                )
                self.create_work_item_from_task(case, "create-manual-workitems")
                self.create_work_item_from_task(case, "depreciate-case")
            elif instance_state == "comm":
                self.create_work_item_from_task(
                    case, "start-circulation", instance=instance
                )
                self.create_work_item_from_task(case, "skip-circulation")
                self.create_work_item_from_task(case, "create-manual-workitems")
                self.create_work_item_from_task(case, "depreciate-case")
                self.create_work_item_from_task(case, "publication", instance=instance)
            elif instance_state == "circ":
                self.migrate_circulation(instance, case)
                self.create_work_item_from_task(case, "create-manual-workitems")
                self.create_work_item_from_task(case, "depreciate-case")
                self.create_work_item_from_task(case, "publication", instance=instance)
                self.create_work_item_from_task(
                    case, "additional-demand", instance=instance
                )
            elif instance_state == "redac":
                self.create_work_item_from_task(
                    case, "make-decision", instance=instance
                )
                self.create_work_item_from_task(
                    case, "reopen-circulation", instance=instance
                )
                self.create_work_item_from_task(case, "create-manual-workitems")
                self.create_work_item_from_task(case, "depreciate-case")
                self.create_work_item_from_task(case, "publication", instance=instance)
            elif instance_state == "nfd":
                self.create_work_item_from_task(
                    case, "submit-additional-demand", applicant=True
                )
                self.create_work_item_from_task(case, "create-manual-workitems")
                self.create_work_item_from_task(case, "depreciate-case")
                self.create_work_item_from_task(case, "publication", instance=instance)
            elif instance_state in ["stopped", "done"]:
                self.create_work_item_from_task(case, "archive-instance")

        post_complete_work_item.connect(post_complete_circulation_work_item)
        post_skip_work_item.connect(post_complete_circulation_work_item)

        self.stdout.write("Created Cases and WorkItems from Instances")
