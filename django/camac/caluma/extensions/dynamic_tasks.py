from itertools import chain
from typing import List

from caluma.caluma_form.models import Document
from caluma.caluma_workflow.dynamic_tasks import BaseDynamicTasks, register_dynamic_task
from caluma.caluma_workflow.models import Task, WorkItem
from django.conf import settings
from django.utils.translation import gettext as _

from camac.caluma.extensions.events.construction_monitoring import (
    CONSTRUCTION_STEP_TRANSLATIONS,
    can_perform_construction_monitoring,
    construction_step_can_continue,
)
from camac.caluma.extensions.events.general import get_instance
from camac.core.utils import canton_aware, create_history_entry
from camac.instance import domain_logic
from camac.user.models import User


class CustomDynamicTasks(BaseDynamicTasks):
    @register_dynamic_task("after-decision")
    @canton_aware
    def resolve_after_decision(self, case, user, prev_work_item, context):
        if not domain_logic.DecisionLogic.should_continue_after_decision(
            case.instance, prev_work_item
        ):
            return []

        tasks = []
        if case.workflow_id == "building-permit":
            tasks = settings.DECISION["TASKS_AFTER_BUILDING_PERMIT_DECISION"]

        involve_geometer = (
            prev_work_item.document.answers.filter(question_id="decision-geometer")
            .values_list("value", flat=True)
            .first()
        )

        if involve_geometer == "decision-geometer-yes":
            tasks.append("geometer")

        return tasks

    @canton_aware
    def resolve_after_decision_so(self, case, user, prev_work_item, context):
        if domain_logic.DecisionLogic.should_continue_after_decision(
            case.instance, prev_work_item
        ):
            return [
                settings.CONSTRUCTION_MONITORING["INIT_CONSTRUCTION_MONITORING_TASK"]
            ]

        decision = domain_logic.DecisionLogic.get_decision_answer(
            question_id=settings.DECISION["QUESTIONS"]["DECISION"],
            work_item=prev_work_item,
        )

        if (
            case.meta.get("is-appeal")
            and decision != settings.APPEAL["ANSWERS"]["DECISION"]["CONFIRMED"]
        ):
            # If the decision comes from an appeal which is not confirmed
            # (either changed or rejected) the workflow is finished because
            # there will be a new copy of the instance which is used for the
            # further workflow
            return []

        if (
            case.instance.instance_state.name
            == settings.WITHDRAWAL["INSTANCE_STATE_CONFIRMED"]
        ):
            # If the decision comes from a withdrawal, the workflow is finished
            return []

        if case.document.form_id in ["voranfrage", "meldung"]:
            # Preliminary clarifications and construction notifications are
            # always finished after the decision
            return []

        return [settings.CONSTRUCTION_MONITORING["COMPLETE_INSTANCE_TASK"]]

    @register_dynamic_task("after-decision-ur")
    def resolve_after_decision_ur(self, case, user, prev_work_item, context):
        tasks = []

        involve_geometer = (
            prev_work_item.document.answers.get(
                question_id="decision-task-nachfuehrungsgeometer"
            ).value
            == "decision-task-nachfuehrungsgeometer-ja"
        )
        involve_gebaeudeschaetzung = (
            prev_work_item.document.answers.get(
                question_id="decision-task-gebaudeschaetzung"
            ).value
            == "decision-task-gebaudeschaetzung-ja"
        )

        if involve_geometer:
            tasks.append("geometer")
        if involve_gebaeudeschaetzung:
            tasks.append("gebaeudeschaetzung")

        return tasks

    @register_dynamic_task("after-complete-check-ur")
    def resolve_after_complete_check_ur(self, case, user, prev_work_item, context):
        complete_check_document = case.work_items.get(task="complete-check").document

        answer = complete_check_document.answers.get(
            question_id="complete-check-vollstaendigkeitspruefung"
        ).value

        if answer in [
            "complete-check-vollstaendigkeitspruefung-incomplete",
            "complete-check-vollstaendigkeitspruefung-incomplete-wait",
        ]:
            return ["additional-demand"]

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

    @register_dynamic_task("after-submit")
    def resolve_after_submit(self, case, user, prev_work_item, context):
        if case.meta.get("is-appeal"):
            return ["create-manual-workitems", "appeal", "decision"]
        elif case.document.form_id == "voranfrage":
            return ["create-manual-workitems", "distribution"]
        elif case.document.form_id == "meldung":
            return ["create-manual-workitems", "decision"]

        return ["create-manual-workitems", "formal-exam", "init-additional-demand"]

    @register_dynamic_task("after-check-additional-demand")
    def resolve_after_check_additional_demand(
        self, case, user, prev_work_item, context
    ):
        if prev_work_item.document.answers.filter(
            question_id=settings.ADDITIONAL_DEMAND["QUESTIONS"]["DECISION"],
            value=settings.ADDITIONAL_DEMAND["ANSWERS"]["DECISION"]["REJECTED"],
        ).exists():
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

    @register_dynamic_task("after-exam")
    def resolve_after_exam(self, case, user, prev_work_item, context):
        if (
            settings.REJECTION.get("WORK_ITEM")
            and prev_work_item.document.answers.filter(
                question_id=settings.REJECTION["WORK_ITEM"]["ON_ANSWER"][
                    prev_work_item.task_id
                ][0],
                value=settings.REJECTION["WORK_ITEM"]["ON_ANSWER"][
                    prev_work_item.task_id
                ][1],
            ).exists()
        ):
            return [settings.REJECTION["WORK_ITEM"]["TASK"]]

        if prev_work_item.task_id == "formal-exam":
            return ["material-exam"]
        elif prev_work_item.task_id == "material-exam":
            tasks = ["distribution", "publication", "fill-publication", "objections"]

            if prev_work_item.case.meta.get("is-bab"):
                tasks.append("material-exam-bab")

            return tasks

        return []  # pragma: no cover

    @register_dynamic_task("after-check-sb2")
    def resolve_after_check_sb2(self, case, user, prev_work_item, context):
        geometer_work_item = WorkItem.objects.filter(
            case=case,
            task_id="geometer",
            status=WorkItem.STATUS_COMPLETED,
        ).first()

        if geometer_work_item:
            perform_cadastral_survey = (
                geometer_work_item.document.answers.filter(
                    question_id="geometer-beurteilung-notwendigkeit-vermessung"
                )
                .values_list("value", flat=True)
                .first()
            )

            if (
                perform_cadastral_survey
                == "geometer-beurteilung-notwendigkeit-vermessung-notwendig"
            ):
                return ["cadastral-survey"]

        return []

    # After decision in Kt. SZ and UR
    @register_dynamic_task("after-make-decision")
    def resolve_after_make_decision(self, case, user, prev_work_item, context):
        if can_perform_construction_monitoring(case.instance):
            return ["init-construction-monitoring"]

        return [settings.CONSTRUCTION_MONITORING["COMPLETE_INSTANCE_TASK"]]

    @register_dynamic_task("after-init-construction-monitoring")
    def resolve_after_construction_monitoring(
        self, case, user, prev_work_item, context
    ):
        if context and context.get("skip", False):
            return settings.CONSTRUCTION_MONITORING["COMPLETE_INSTANCE_TASK"]

        return [
            settings.CONSTRUCTION_MONITORING["CONSTRUCTION_STAGE_TASK"],
            settings.CONSTRUCTION_MONITORING["COMPLETE_CONSTRUCTION_MONITORING_TASK"],
        ]

    @register_dynamic_task("after-construction-step")
    def resolve_after_construction_step(
        self, case: object, user: object, prev_work_item: object, context: dict
    ) -> List[str]:
        previous_step = prev_work_item.meta["construction-step-id"]

        # Return first task of current construction step if the step
        # hasn't been approved
        if not construction_step_can_continue(prev_work_item):
            return list(
                Task.objects.filter(
                    **{
                        "meta__construction-step-id": previous_step,
                        "meta__construction-step__index": 0,
                    }
                ).values_list("pk", flat=True)
            )

        # Create history entry for completed construction-step
        instance = get_instance(prev_work_item)
        camac_user = User.objects.get(username=user.username)
        construction_step_translation = CONSTRUCTION_STEP_TRANSLATIONS[previous_step]
        construction_step_completed_translation = _("Construction step completed")
        history_text = f"{construction_step_translation} ({prev_work_item.case.parent_work_item.name}) {construction_step_completed_translation}"
        create_history_entry(instance, camac_user, history_text)

        # Retrieve selected construction steps
        document = Document.objects.filter(
            work_item__case__pk=case.pk,
            form_id=settings.CONSTRUCTION_MONITORING[
                "CONSTRUCTION_STEP_PLAN_CONSTRUCTION_STAGE_FORM"
            ],
        ).first()

        answer = (
            document.answers.select_related("question")
            .prefetch_related("question__options")
            .filter(question_id="construction-steps")
            .first()
        )

        selected_construction_steps = answer.value if answer else []

        # Find next steps (with initial tasks) to perform, which were selected
        # in construction stage planning step. Certain construction steps may
        # have multiple succeeding construction steps.
        def find_next_steps(
            construction_step: str, selected_construction_steps: List[str]
        ) -> List[str]:
            if (
                previous_step != construction_step
                and construction_step in selected_construction_steps
            ):
                return [construction_step]

            construction_step_task = Task.objects.filter(
                **{"meta__construction-step-id": construction_step}
            ).first()
            next_construction_steps = construction_step_task.meta["construction-step"][
                "next"
            ]

            steps = []
            for step in next_construction_steps:
                steps += find_next_steps(step, selected_construction_steps)

            return steps

        next_steps = find_next_steps(
            previous_step,
            selected_construction_steps,
        )

        return list(
            Task.objects.filter(
                **{
                    "meta__construction-step-id__in": next_steps,
                    "meta__construction-step__index": 0,
                }
            ).values_list("pk", flat=True)
        )

    @register_dynamic_task("after-formal-exam")
    def resolve_after_formal_exam(self, case, user, prev_work_item, context):
        if settings.PUBLICATION.get(
            "AFTER_FORMAL_EXAM_PUBLICATION_TASKS", []
        ) and case.document.form.slug not in ["bauanzeige", "vorlaeufige-beurteilung"]:
            return settings.PUBLICATION["AFTER_FORMAL_EXAM_PUBLICATION_TASKS"]
        return [settings.DISTRIBUTION["DISTRIBUTION_TASK"]]
