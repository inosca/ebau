from caluma.caluma_workflow.models import Case, WorkItem
from dateutil import relativedelta
from django.conf import settings
from django.db.models import Q
from django.utils.translation import gettext_noop as _
from rest_framework import serializers

from camac.caluma.api import CalumaApi
from camac.core.models import PublicationEntry
from camac.document.models import Attachment, AttachmentDownloadHistory

from ..master_data import MasterData
from . import fields


# This doesn't have coverage because the fields that needed this were
# removed recently. It is therefore not part of the snapshot tests anymore.
# If Uri decides that they will never use this, it can be removed.
def _is_controlled_by_a_coordination_service():  # pragma: no cover
    if settings.APPLICATION.get("COORDINATION_SERVICE_IDS"):
        return Q(
            controlling_groups__overlap=settings.APPLICATION["COORDINATION_SERVICE_IDS"]
        )

    raise RuntimeError(  # pragma: no cover
        "You can not specify the '_is_controlled_by_a_coordination_service' filter if the 'COORDINATION_SERVICE_IDS' are not set in the django.py"
    )


def _is_addressed_to_a_coordination_service():
    if settings.APPLICATION.get("COORDINATION_SERVICE_IDS"):
        return Q(
            addressed_groups__overlap=settings.APPLICATION["COORDINATION_SERVICE_IDS"]
        )

    raise RuntimeError(  # pragma: no cover
        "You can not specify the '_is_addressed_to_a_coordination_service' filter if the 'COORDINATION_SERVICE_IDS' are not set in the django.py"
    )


def _is_addressed_to_the_responsible_service(instance):
    responsible_service = instance.responsible_service()

    return (
        Q(addressed_groups__contains=[responsible_service.pk])
        if instance.responsible_service()
        else Q()
    )


def _get_date_of_downloaded_decision_document(instance):
    decision_attachments = Attachment.objects.filter(
        **{"context__isDecision": True}, instance_id=instance.pk
    )

    for decision_attachment in decision_attachments:
        if downloaded_attachments := AttachmentDownloadHistory.objects.filter(
            attachment_id=decision_attachment.attachment_id
        ).first():
            return downloaded_attachments.date_time


def _check_feedback_answer(instance, slug):
    decision_workitem = list(
        filter(
            lambda work_item: work_item.task_id == "decision", instance._all_work_items
        )
    )[:1]
    if decision_workitem:
        feedback_answer = (
            decision_workitem[0]
            .document.answers.filter(question_id="decision-task-feedback-type")
            .first()
        )
        if feedback_answer:
            if feedback_answer.value == slug:
                return True
    return False


def _get_decision_work_item_closed_at(instance):
    work_item = list(
        filter(
            lambda work_item: work_item.task_id == "decision"
            and work_item.case == instance.case
            and work_item.status == WorkItem.STATUS_COMPLETED
            and work_item.closed_at is not None,
            instance._all_work_items,
        )
    )[:1]
    if work_item:
        return work_item[0].closed_at


class MilestonesSerializer(serializers.Serializer):
    def __init__(self, instance, *args, **kwargs):
        super().__init__(instance, *args, **kwargs)

        instance._master_data = MasterData(instance.case)
        instance._child_cases = list(Case.objects.filter(family=instance.case))
        instance._work_items = list(
            WorkItem.objects.filter(case=instance.case).prefetch_related(
                "document__answers"
            )
        )
        instance._all_work_items = list(
            WorkItem.objects.filter(case__in=instance._child_cases).prefetch_related(
                "document__answers"
            )
        )

    def get_paper_submission(self, instance):
        if CalumaApi().is_paper(instance):
            submit_work_item = next(
                (
                    wi
                    for wi in instance._work_items
                    if wi.task_id in settings.APPLICATION["CALUMA"]["SUBMIT_TASKS"]
                ),
                None,
            )
            return submit_work_item.closed_at if submit_work_item else []

        return []  # pragma: no cover

    def get_instance_submitted(self, instance):
        if not CalumaApi().is_paper(instance):
            submit_work_item = next(
                (
                    wi
                    for wi in instance._work_items
                    if wi.task_id in settings.APPLICATION["CALUMA"]["SUBMIT_TASKS"]
                ),
                None,
            )

            return submit_work_item.closed_at if submit_work_item else []

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
                        task="send-additional-demand",
                        status=WorkItem.STATUS_COMPLETED,
                        field="created_at",
                    ),
                    fields.WorkItemsField(
                        slug="check-completed",
                        label=_("Check completed"),
                        task="complete-check",
                        field="closed_at",
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
                    fields.MethodField(
                        slug="publication-date", label=_("Puclication date")
                    ),
                    fields.AnswerField(
                        slug="einsprache",
                        label=_("Receipt of objections"),
                        document="tabelle-rechtsmittelverfahren",
                        family_form_id="instance-management",
                    ),
                    fields.WorkItemsField(
                        task="fill-inquiry",
                        label=_("Forwarding to KOOR"),
                        order_by="created_at",
                        limit=1,
                        filter=lambda instance: _is_addressed_to_a_coordination_service(),
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
                    fields.MethodField(
                        slug="statement-preliminary-decision",
                        label=_("Statement - preliminary decision"),
                    ),
                    fields.MethodField(
                        slug="building-decision",
                        label=_("Building decision"),
                    ),
                    fields.WorkItemsField(
                        slug="notice-to-geometer",
                        label=_("notice to geometer"),
                        task="geometer",
                        field="created_at",
                    ),
                    fields.MethodField(
                        slug="receipt-confirmation-of-decision-documents",
                        label=_("Receipt confirmation of decision documents"),
                    ),
                    fields.MethodField(
                        slug="receipt-confirmation-of-preliminary-decision",
                        label=_("Receipt confirmation of preliminary decision"),
                    ),
                    fields.WorkItemsField(
                        slug="notice-to-gebaeudeschaetzung",
                        label=_("notice to gebaeudeschaetzung"),
                        task="gebaeudeschaetzung",
                        field="created_at",
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
        # In Uri "Dossier vollständig" means that all required information is available
        # to continue with the instance.

        complete_check_work_item = next(
            (
                wi
                for wi in instance._all_work_items
                if wi.task_id == "complete-check"
                and wi.status == WorkItem.STATUS_COMPLETED
            ),
            None,
        )

        if complete_check_work_item:
            if not complete_check_work_item.document.answers.exists():
                # for migrated dossiers in Uri there is no "complete-check"
                return None  # pragma: no cover

            complete_check_answer = complete_check_work_item.document.answers.get(
                question_id="complete-check-vollstaendigkeitspruefung"
            ).value

            if (
                complete_check_answer
                == "complete-check-vollstaendigkeitspruefung-complete"
            ):
                # Dossier is "vollständig"
                return complete_check_work_item.closed_at

            if complete_check_answer in [
                "complete-check-vollstaendigkeitspruefung-incomplete",
                "complete-check-vollstaendigkeitspruefung-incomplete-wait",
            ]:
                # Dossier was incomplete during the check and additional-demands were required
                open_additional_demand_work_items = [
                    wi
                    for wi in instance._all_work_items
                    if (
                        wi.task_id
                        in [
                            "send-additional-demand",
                            "fill-additional-demand",
                            "check-additional-demand",
                        ]
                        and wi.status == WorkItem.STATUS_READY
                    )
                ]

                if len(open_additional_demand_work_items):
                    # There are open additional-demands
                    return None
                else:
                    completed_check_additional_demand_work_items_closed_at = [
                        wi.closed_at
                        for wi in instance._all_work_items
                        if (
                            wi.task_id == "check-additional-demand"
                            and wi.status == WorkItem.STATUS_COMPLETED
                        )
                    ]
                    return max(completed_check_additional_demand_work_items_closed_at)

        return None  # pragma: no cover

    def get_building_permit_valid_until(self, instance):
        decision_work_item = next(
            (
                wi
                for wi in instance._work_items
                if wi.task_id == "decision" and wi.status == WorkItem.STATUS_COMPLETED
            ),
            None,
        )

        if decision_work_item and decision_work_item.closed_at is not None:
            return decision_work_item.closed_at + relativedelta.relativedelta(years=1)

        return []  # pragma: no cover

    def get_receipt_confirmation_of_decision_documents(self, instance):
        if _check_feedback_answer(
            instance, "decision-task-feedback-type-bau-und-einspracheentscheid"
        ):
            return _get_date_of_downloaded_decision_document(instance)

    def get_receipt_confirmation_of_preliminary_decision(self, instance):
        if _check_feedback_answer(
            instance, "decision-task-feedback-type-stellungnahme-vorentscheid"
        ):
            return _get_date_of_downloaded_decision_document(instance)

    def get_publication_date(self, instance):
        # There is only one publication possible in Kt. Uri so we can safely use first
        if publication := PublicationEntry.objects.filter(
            instance_id=instance.pk
        ).first():
            return publication.publication_date

    def get_statement_preliminary_decision(self, instance):
        if _check_feedback_answer(
            instance, "decision-task-feedback-type-stellungnahme-vorentscheid"
        ):
            return _get_decision_work_item_closed_at(instance)

    def get_building_decision(self, instance):
        if _check_feedback_answer(
            instance, "decision-task-feedback-type-bau-und-einspracheentscheid"
        ):
            return _get_decision_work_item_closed_at(instance)
