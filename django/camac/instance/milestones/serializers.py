from caluma.caluma_workflow.models import Case, WorkItem
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


def _check_decision_answer(instance, answer_slug, question_slug):
    decision_workitem = list(
        filter(
            lambda work_item: work_item.task_id == "decision", instance._all_work_items
        )
    )[:1]
    if decision_workitem:
        feedback_answer = (
            decision_workitem[0]
            .document.answers.filter(question_id=question_slug)
            .first()
        )
        if feedback_answer:
            if feedback_answer.value == answer_slug:
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
                    fields.WorkItemsField(
                        slug="additional-demand",
                        label=_("Additional demand municipality"),
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
                    fields.MethodField(
                        slug="publication-date", label=_("Publication date")
                    ),
                    fields.AnswerField(
                        slug="einsprache",
                        label=_("Receipt of objections"),
                        document="tabelle-rechtsmittelverfahren",
                        family_form_id="instance-management",
                    ),
                    fields.WorkItemsField(
                        slug="start-circulation-new",
                        label=_("Start circulation"),
                        task="init-distribution",
                        filter=lambda instance: _is_addressed_to_the_responsible_service(
                            instance
                        ),
                        status=WorkItem.STATUS_COMPLETED,
                        field="closed_at",
                    ),
                    fields.WorkItemsField(
                        task="fill-inquiry",
                        label=_("Forwarding to KOOR"),
                        order_by="created_at",
                        limit=1,
                        filter=lambda instance: _is_addressed_to_a_coordination_service(),
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
                    fields.MethodField(
                        slug="receipt-confirmation-of-preliminary-decision",
                        label=_("Receipt confirmation of preliminary decision"),
                    ),
                    fields.MethodField(
                        slug="receipt-confirmation-of-decision-documents",
                        label=_("Receipt confirmation of decision documents"),
                    ),
                    fields.AnswerField(
                        slug="baubewilligung-gueltig-bis",
                        label=_("Building permit valid until"),
                        document="instance-management",
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
                        slug="paper-submission", label=_("Paper submission")
                    ),
                    fields.CamacWorkflowEntryField(
                        slug="objection-deadline",
                        name="Einsprachefrist",
                        label=_("Objection deadline (migrated)"),
                    ),
                    fields.CamacWorkflowEntryField(
                        slug="submission-to-koor",
                        name="Weiterleitung an Koord",
                        label=_("submission to koor (migrated)"),
                    ),
                    fields.MethodField(
                        slug="start-circulation", label=_("Start circulation migrated")
                    ),
                    fields.CamacWorkflowEntryField(
                        slug="building-decision-migrated",
                        name="Bau- und Einspracheentscheid",
                        label=_("Building decision (migrated)"),
                    ),
                    fields.CamacWorkflowEntryField(
                        slug="dispatch-statement-preliminary-decision-by-post",
                        name="Versand / Stellungnahme - Vorentscheid per Post",
                        label=_(
                            "Dispatch / statement - preliminary decision by post (migrated)"
                        ),
                    ),
                    fields.CamacWorkflowEntryField(
                        slug="dispatch-statement-preliminary-decision-by-email",
                        name="Versand / Stellungnahme - Vorentscheid per Mail",
                        label=_(
                            "Dispatch / statement - preliminary decision by e-mail (migrated)"
                        ),
                    ),
                    fields.CamacWorkflowEntryField(
                        slug="dispatch-decision-documents-by-post",
                        name="Versand Entscheiddokumente per Post",
                        label=_("Dispatch of decision documents by post (migrated)"),
                    ),
                    fields.CamacWorkflowEntryField(
                        slug="dispatch-decision-documents-by-email",
                        name="Versand Entscheiddokumente per Mail",
                        label=_("Dispatch of decision documents by e-mail (migrated)"),
                    ),
                    fields.CamacWorkflowEntryField(
                        slug="dispatch-decision-documents-by-portal",
                        name="Versand Entscheiddokumente per Portal",
                        label=_("Dispatch of decision documents by portal (migrated)"),
                    ),
                ],
            ),
            fields.MilestoneSectionField(
                slug="reports-to-third-parties-regular-process",
                label=_("reports to third parties regular process"),
                fields=[
                    fields.MethodField(
                        slug="notice-to-geometer", label=_("notice to geometer")
                    ),
                    fields.CamacWorkflowEntryField(
                        slug="notification-building-permit-to-surveyor",
                        name="Meldung Baubewilligung an Geometer",
                        label=_(
                            "Notification of building permit to surveyor (migrated)"
                        ),
                    ),
                ],
            ),
            fields.MilestoneSectionField(
                slug="reports-to-third-parties-construction-monitoring",
                label=_("reports to third parties construction monitoring"),
                fields=[
                    fields.AnswerField(
                        slug="meldung-gebaeudeabbruch-an-geometer",
                        label=_("demolition notice to geometer"),
                        document="instance-management",
                    ),
                    fields.WorkItemsField(
                        slug="bauverwaltung-meldung-bau-beendet-an-geometer",
                        label=_("Notice construction finished to geometer"),
                        task="construction-step-schlussabnahme-gebaeude-melden",
                        field="closed_at",
                    ),
                    fields.WorkItemsField(
                        slug="notice-to-gebaeudeschaetzung",
                        label=_("notice to gebaeudeschaetzung"),
                        task="gebaeudeschaetzung",
                        field="created_at",
                    ),
                    fields.WorkItemsField(
                        slug="notice-to-liegenschaftsschaetzung",
                        label=_("notice to liegenschaftsschaetzung"),
                        task="liegenschaftsschaetzung",
                        field="created_at",
                    ),
                    fields.WorkItemsField(
                        slug="meldung-bereit-zur-kanalisationsabnahme-an-abwasser-uri",
                        label=_("notice kanalisationsabnahme to abwasser uri"),
                        task="construction-step-kanalisationsabnahme-melden",
                        field="closed_at",
                    ),
                    fields.WorkItemsField(
                        slug="meldung-bereit-zur-schnurgeruestabnahme-an-geometer",
                        label=_("notice schnurgeruestabnahme to geometer"),
                        task="construction-step-schnurgeruestabnahme-melden",
                        field="closed_at",
                    ),
                    fields.CamacWorkflowEntryField(
                        slug="start-of-construction",
                        name="Baubeginn erfolgt",
                        label=_("Start of construction (migrated)"),
                    ),
                    fields.CamacWorkflowEntryField(
                        slug="acceptance-of-sectional-framework",
                        name="Abnahme Schnurgerüst",
                        label=_("Acceptance of sectional framework (migrated)"),
                    ),
                    fields.CamacWorkflowEntryField(
                        slug="acceptance-of-shell-construction",
                        name="Abnahme Rohbau",
                        label=_("Acceptance of shell construction (migrated)"),
                    ),
                    fields.CamacWorkflowEntryField(
                        slug="construction-finished",
                        name="Bau beendet",
                        label=_("Construction finished (migrated)"),
                    ),
                    fields.CamacWorkflowEntryField(
                        slug="final-acceptance-completed",
                        name="Endabnahme erfolgt",
                        label=_("Final acceptance completed (migrated)"),
                    ),
                    fields.CamacWorkflowEntryField(
                        slug="dossier-archived",
                        name="Dossier archiviert",
                        label=_("Dossier archived (migrated)"),
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
                    if completed_check_additional_demand_work_items_closed_at:
                        return max(
                            completed_check_additional_demand_work_items_closed_at
                        )

        return None  # pragma: no cover

    def get_receipt_confirmation_of_decision_documents(self, instance):
        if _check_decision_answer(
            instance,
            "decision-task-feedback-type-bau-und-einspracheentscheid",
            "decision-task-feedback-type",
        ):
            return _get_date_of_downloaded_decision_document(instance)

    def get_receipt_confirmation_of_preliminary_decision(self, instance):
        if _check_decision_answer(
            instance,
            "decision-task-feedback-type-stellungnahme-vorentscheid",
            "decision-task-feedback-type",
        ):
            return _get_date_of_downloaded_decision_document(instance)

    def get_publication_date(self, instance):
        # There is only one publication possible in Kt. Uri so we can safely use first
        if publication := PublicationEntry.objects.filter(
            instance_id=instance.pk
        ).first():
            return publication.publication_date

    def get_statement_preliminary_decision(self, instance):
        if _check_decision_answer(
            instance,
            "decision-task-feedback-type-stellungnahme-vorentscheid",
            "decision-task-feedback-type",
        ):
            return _get_decision_work_item_closed_at(instance)

    def get_building_decision(self, instance):
        if _check_decision_answer(
            instance,
            "decision-task-feedback-type-bau-und-einspracheentscheid",
            "decision-task-feedback-type",
        ):
            return _get_decision_work_item_closed_at(instance)

    def get_notice_to_geometer(self, instance):
        if _check_decision_answer(
            instance,
            "decision-task-nachfuehrungsgeometer-ja",
            "decision-task-nachfuehrungsgeometer",
        ):
            return _get_decision_work_item_closed_at(instance)

    def get_start_circulation(self, instance):
        workitem = WorkItem.objects.filter(
            case=instance.case,
            task=settings.DISTRIBUTION["DISTRIBUTION_INIT_TASK"],
            **{"meta__migrated-at__isnull": False},
        ).first()
        if workitem:
            return workitem.closed_at
        return ""  # pragma: no cover
