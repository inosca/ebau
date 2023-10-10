from itertools import chain

from caluma.caluma_workflow.dynamic_tasks import BaseDynamicTasks, register_dynamic_task
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings

from camac.instance.utils import should_continue_after_decision


class CustomDynamicTasks(BaseDynamicTasks):
    @register_dynamic_task("after-decision")
    def resolve_after_decision(self, case, user, prev_work_item, context):
        if case.workflow_id == "building-permit" and should_continue_after_decision(
            case.instance, prev_work_item
        ):
            return [
                "sb1",
                settings.APPLICATION["CALUMA"]["MANUAL_WORK_ITEM_TASK"],
                "create-publication",
            ]

        return []

    @register_dynamic_task("after-inquiries-completed")
    def resolve_after_inquiries_completed(self, case, user, prev_work_item, context):
        # Further work-items should only be created if there are no
        # further ready sibling inquiries (i.e. within same distribution case)
        # with the same controlling group as the previously completed inquiry.
        pending_inquiries = case.work_items.filter(
            task_id=settings.DISTRIBUTION["INQUIRY_TASK"],
            status=WorkItem.STATUS_READY,
            controlling_groups=prev_work_item.controlling_groups,
        )

        if pending_inquiries.exists():
            return []

        tasks = []

        # If no check-inquiries work-item exists yet addressed to
        # the controlling group of the previously completed inquiry,
        # it should be created.
        check_inquiries = case.work_items.filter(
            task_id=settings.DISTRIBUTION["INQUIRY_CHECK_TASK"],
            status=WorkItem.STATUS_READY,
            addressed_groups=prev_work_item.controlling_groups,
        )

        if not check_inquiries.exists():
            tasks.append(settings.DISTRIBUTION["INQUIRY_CHECK_TASK"])

        # If no check-distribution work-item exists addressed to
        # the lead authority, then it should be created if the
        # controlling group of the previously completed inquiry is the
        # lead authority itself.
        check_distribution = case.work_items.filter(
            task_id=settings.DISTRIBUTION["DISTRIBUTION_CHECK_TASK"],
            status=WorkItem.STATUS_READY,
            addressed_groups=case.parent_work_item.addressed_groups,
        )

        if (
            not check_distribution.exists()
            and prev_work_item.controlling_groups
            == case.parent_work_item.addressed_groups
        ):
            tasks.append(settings.DISTRIBUTION["DISTRIBUTION_CHECK_TASK"])

        return tasks

    @register_dynamic_task("after-ebau-number")
    def resolve_after_ebau_number(self, case, user, prev_work_item, context):
        tasks = [
            "distribution",
            "audit",
            "publication",
            "fill-publication",
            "information-of-neighbors",
            "legal-submission",
        ]

        if case.meta.get("is-appeal"):
            tasks.append("appeal")

        return tasks

    @register_dynamic_task("after-check-additional-demand")
    def resolve_after_check_additional_demand(
        self, case, user, prev_work_item, context
    ):
        decision = prev_work_item.document.answers.get(
            question_id=settings.ADDITIONAL_DEMAND["DECISION_QUESTION"]
        )

        if settings.ADDITIONAL_DEMAND["DECISION_REJECT"] == decision.value:
            return [settings.ADDITIONAL_DEMAND["FILL_TASK"]]

        return []

    @register_dynamic_task("after-create-inquiry")
    def resolve_after_create_inquiry(self, case, user, prev_work_item, context):
        tasks = [
            settings.DISTRIBUTION["INQUIRY_TASK"],
            settings.DISTRIBUTION["INQUIRY_CREATE_TASK"],
        ]

        # If there doesn't exist a ready "init-additional-demand" work item for
        # each of the passed addressed groups, we need to create a new one. To
        # avoid duplicates, the dynamic group of the "init-additional-demand"
        # task makes sure to not filter out services that already have such a
        # work item
        if set(context["addressed_groups"]) - set(
            chain(
                *case.work_items.filter(
                    addressed_groups__overlap=context["addressed_groups"],
                    task_id=settings.ADDITIONAL_DEMAND["CREATE_TASK"],
                    status=WorkItem.STATUS_READY,
                ).values_list("addressed_groups", flat=True)
            )
        ):
            tasks.append(settings.ADDITIONAL_DEMAND["CREATE_TASK"])

        return tasks
