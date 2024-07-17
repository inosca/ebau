from caluma.caluma_workflow.models import Case, WorkItem
from dateutil import relativedelta
from django.conf import settings
from django.db.models import Q
from django.utils.translation import gettext_noop as _
from rest_framework import serializers

from camac.caluma.api import CalumaApi

from ..master_data import MasterData
from . import fields


def _is_controlled_by_a_coordination_service():
    if settings.APPLICATION.get("COORDINATION_SERVICE_IDS"):
        return Q(
            controlling_groups__overlap=settings.APPLICATION["COORDINATION_SERVICE_IDS"]
        )

    raise RuntimeError(  # pragma: no cover
        "You can not specify the '_is_controlled_by_a_coordination_service' filter if the 'COORDINATION_SERVICE_IDS' are not set in the settings.py"
    )


def _is_addressed_to_the_responsible_service(instance):
    responsible_service = instance.responsible_service()

    return (
        Q(addressed_groups__contains=[responsible_service.pk])
        if instance.responsible_service()
        else Q()
    )


class MilestonesSerializer(serializers.Serializer):
    def __init__(self, instance, *args, **kwargs):
        super().__init__(instance, *args, **kwargs)

        instance._master_data = MasterData(instance.case)
        instance._child_cases = Case.objects.filter(family=instance.case)
        instance._work_items = WorkItem.objects.filter(case=instance.case)
        instance._all_work_items = WorkItem.objects.filter(
            case__in=instance._child_cases,
        )

    def get_paper_submission(self, instance):
        if CalumaApi().is_paper(instance):
            if submit_task := instance._work_items.filter(
                task__in=settings.APPLICATION["CALUMA"]["SUBMIT_TASKS"]
            ).first():
                return submit_task.closed_at if submit_task else []

        return []  # pragma: no cover

    def get_instance_submitted(self, instance):
        if not CalumaApi().is_paper(instance):
            submit_work_item = instance._work_items.filter(task="submit").first()
            return submit_work_item.closed_at if submit_work_item else []

        return []  # pragma: no cover

    def get_building_permit_valid_until(self, instance):
        decision_work_item = instance._work_items.filter(task="decision").first()

        if decision_work_item and decision_work_item.closed_at:
            return decision_work_item.closed_at + relativedelta.relativedelta(years=1)

        return []  # pragma: no cover


class UrMilestonesSerializer(MilestonesSerializer):
    sections = fields.MilestonesField(
        sections=[
            fields.MilestoneSectionField(
                slug="regular-process",
                label=_("regular process"),
                fields=[
                    fields.MethodField(
                        slug="instance-submitted", label=_("instance submitted")
                    ),
                    fields.MethodField(
                        slug="paper-submission", label=_("Paper submission")
                    ),
                    fields.WorkItemsField(
                        slug="additional-demand",
                        label=_("Additional demand"),
                        task="additional-demand",
                        status=WorkItem.STATUS_COMPLETED,
                        field="created_at",
                    ),
                    fields.MethodField(
                        slug="instance-complete", label=_("Instance complete")
                    ),
                    fields.WorkItemsField(
                        slug="review-building-commission",
                        label=_("Review building commission"),
                        task="review-building-commission",
                        status=WorkItem.STATUS_COMPLETED,
                        field="closed_at",
                        order_by="-closed_at",
                        limit=1,
                    ),
                    fields.WorkItemsField(
                        slug="start-circulation",
                        label=_("Start circulation"),
                        task="init-distribution",
                        filter=lambda instance: _is_addressed_to_the_responsible_service(
                            instance
                        ),
                        status=WorkItem.STATUS_COMPLETED,
                        field="closed_at",
                    ),
                    fields.WorkItemsField(
                        slug="distribution-completed",
                        label=_("Distribution completed"),
                        task="distribution",
                        field="closed_at",
                        status=WorkItem.STATUS_COMPLETED,
                        filter=lambda instance: Q(
                            _is_addressed_to_the_responsible_service(instance)
                        ),
                    ),
                    fields.WorkItemsField(
                        slug="decision",
                        label=_("Decision made"),
                        task="distribution",
                        field="closed_at",
                        status=WorkItem.STATUS_COMPLETED,
                    ),
                    fields.WorkItemsField(
                        slug="notice-to-geometer",
                        label=_("notice to geometer"),
                        task="geometer",
                        field="created_at",
                    ),
                    fields.WorkItemsField(
                        slug="notice-to-gebaeudeschaetzung",
                        label=_("notice to gebaeudeschaetzung"),
                        task="gebaeudeschaetzung",
                        field="created_at",
                    ),
                    # I added this to get test code coverage.
                    # I will replace this with a more meaningful field once Uri
                    # uses the new workflow and actually has meaningful date questions
                    fields.AnswerField(
                        slug="is-paper", label=_("is paper"), document="building-permit"
                    ),
                    fields.WorkItemsField(
                        slug="check-completed",
                        label=_("Check completed"),
                        task="complete-check",
                        field="closed_at",
                    ),
                    fields.WorkItemsField(
                        slug="forwarded-to-koor",
                        label=_("Forwarded to coordination service"),
                        task="fill-inquiry",
                        filter=lambda instance: _is_controlled_by_a_coordination_service(),
                    ),
                    fields.WorkItemsField(
                        slug="start-cantonal-distribution",
                        label=_("Start of cantonal distribution"),
                        task="inquiry",
                        filter=lambda instance: _is_controlled_by_a_coordination_service(),
                    ),
                    fields.WorkItemsField(
                        slug="returned-to-municipality",
                        label=_("Returned to municipality"),
                        task="check-inquiries",
                        field="closed_at",
                        status=WorkItem.STATUS_COMPLETED,
                        filter=lambda instance: _is_controlled_by_a_coordination_service(),
                    ),
                    fields.MethodField(
                        slug="building-permit-valid-until",
                        label=_("Building permit valid until"),
                    ),
                ],
            ),
        ],
    )

    def get_instance_complete(self, instance):
        # todo: fix this once the additional-demand setup is working with the nested child cases etc.
        return None
        # In Uri "Dossier vollständig" means that all required information is available
        # to continue with the instance.
        # if complete_check_work_item := instance.case.work_items.filter(task_id="complete-check", status=WorkItem.STATUS_COMPLETED):
        #     complete_check_answer = complete_check_work_item.document.answers.get("complete-check-vollstaendigkeitspruefung").value
        #     if complete_check_answer == "complete-check-vollstaendigkeitspruefung-complete":
        #         # Dossier is "vollständig"
        #         return complete_check_work_item.closed_at

        #     if complete_check_answer in ["complete-check-vollstaendigkeitspruefung-incomplete", "complete-check-vollstaendigkeitspruefung-incomplete-wait"]:
        #         # Dossier was incomplete during the check and additional-demands were required
        #         return None
