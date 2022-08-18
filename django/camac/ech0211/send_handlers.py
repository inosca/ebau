from collections import namedtuple

from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Question
from caluma.caluma_workflow import api as workflow_api
from caluma.caluma_workflow.models import Case, WorkItem
from django.conf import settings

from camac.constants.kt_bern import (
    ATTACHMENT_SECTION_ALLE_BETEILIGTEN,
    DECISION_TYPE_UNKNOWN,
)
from camac.core.models import InstanceService
from camac.document.models import Attachment, AttachmentSection
from camac.instance.models import Instance, InstanceState
from camac.instance.serializers import CalumaInstanceChangeResponsibleServiceSerializer
from camac.user.models import Service

from .constants import ECH_JUDGEMENT_DECLINED
from .signals import ruling
from .utils import judgement_to_decision


class SendHandlerException(Exception):
    def __init__(self, message, status=400):
        super().__init__(message)
        self.status = status


class DocumentAccessibilityMixin:
    def get_attachments(self, ech_documents):
        uuids = set([doc.uuid for doc in ech_documents])
        attachments = Attachment.objects.filter(uuid__in=uuids).distinct()
        if attachments.count() != len(uuids):
            attachment_uuids = set(attachments.values_list("uuid", flat=True))
            missing = ", ".join(uuids - attachment_uuids)
            raise SendHandlerException(
                f"No document found for uuids: {missing}.", status=404
            )
        return attachments

    def has_attachment_permissions(self, attachments):
        for attachment in attachments:
            if (
                self.instance != attachment.instance
                or attachment.instance.responsible_service() != self.group.service
            ):
                return False
        return True

    def link_to_section(self, attachments, target=ATTACHMENT_SECTION_ALLE_BETEILIGTEN):
        section_alle_beteiligten = AttachmentSection.objects.get(pk=target)
        for attachment in attachments:
            if not attachment.attachment_sections.filter(pk=target).exists():
                attachment.attachment_sections.add(section_alle_beteiligten)


class BaseSendHandler:
    def __init__(self, data, queryset, user, group, auth_header, caluma_user):
        self.data = data
        self.user = user
        self.group = group
        self.auth_header = auth_header
        self.caluma_user = caluma_user
        self.instance = self._get_instance(queryset)

    def _get_instance(self, queryset):
        try:
            return queryset.get(pk=self.get_instance_id())
        except Instance.DoesNotExist:
            raise SendHandlerException("Unknown instance")

    def get_instance_id(self):
        return (
            self.data.eventNotice.planningPermissionApplicationIdentification.dossierIdentification
        )

    def get_case(self):
        return Case.objects.get(instance__pk=self.get_instance_id())

    def complete_work_item(self, task, filters={}, context={}):
        return self._process_work_item("complete", task, filters, context)

    def skip_work_item(self, task, filters={}, context={}):
        return self._process_work_item("skip", task, filters, context)

    def _process_work_item(self, action, task, filters, context):
        fn = getattr(workflow_api, f"{action}_work_item")
        work_item = WorkItem.objects.filter(
            case__family=self.get_case(),
            task_id=task,
            status=WorkItem.STATUS_READY,
            **filters,
        ).first()

        if work_item and fn:
            fn(work_item=work_item, user=self.caluma_user, context=context)

    def has_permission(self):
        return self.instance.responsible_service() == self.group.service, None

    def apply(self):  # pragma: no cover
        raise NotImplementedError()


class NoticeRulingSendHandler(DocumentAccessibilityMixin, BaseSendHandler):
    def has_permission(self):
        if not super().has_permission()[0]:
            return False, None

        if self.instance.instance_state.name == "circulation_init":
            if self.data.eventNotice.decisionRuling.judgement != ECH_JUDGEMENT_DECLINED:
                return (
                    False,
                    f'For instances in the state "Zirkulation initialisieren", only a NoticeRuling with judgement "{ECH_JUDGEMENT_DECLINED}" is allowed.',
                )
            return True, None
        if self.instance.instance_state.name not in ["coordination", "circulation"]:
            return (
                False,
                'NoticeRuling is only allowed for instances in the state "In Koordination" or "In Zirkulation".',
            )

        return True, None

    def apply(self):
        attachments = self.get_attachments(self.data.eventNotice.document)
        if not self.has_attachment_permissions(attachments):
            raise SendHandlerException(
                "You don't have permission for at least one document you provided.",
                status=403,
            )

        case = self.get_case()
        workflow_slug = case.workflow_id
        judgement = self.data.eventNotice.decisionRuling.judgement

        try:
            decision = judgement_to_decision(judgement, workflow_slug)
        except KeyError:
            raise SendHandlerException(
                f'"{judgement}" is not a valid judgement for "{workflow_slug}"'
            )

        if judgement == ECH_JUDGEMENT_DECLINED:
            # reject instance
            self.instance.previous_instance_state = self.instance.instance_state
            self.instance.instance_state = InstanceState.objects.get(name="rejected")
            self.instance.save()

            # send eCH event
            ruling.send(
                sender=self.__class__,
                instance=self.instance,
                user_pk=self.user.pk,
                group_pk=self.group.pk,
            )

            # suspend case
            workflow_api.suspend_case(case=case, user=self.caluma_user)
        else:
            self.skip_work_item(settings.DISTRIBUTION["DISTRIBUTION_TASK"])

            # write the decision document
            decision_document = case.work_items.get(
                task_id="decision", status=WorkItem.STATUS_READY
            ).document
            save_answer(
                document=decision_document,
                question=Question.objects.get(slug="decision-decision-assessment"),
                value=decision,
            )
            save_answer(
                document=decision_document,
                question=Question.objects.get(slug="decision-date"),
                date=self.data.eventNotice.decisionRuling.date.date(),
            )
            if workflow_slug == "building-permit":
                save_answer(
                    document=decision_document,
                    question=Question.objects.get(slug="decision-approval-type"),
                    value=DECISION_TYPE_UNKNOWN,
                )

            # this handle status changes and assignment of the construction control
            # for "normal" judgements
            self.complete_work_item("decision")

        self.link_to_section(attachments)


class ChangeResponsibilitySendHandler(BaseSendHandler):
    def has_permission(self):
        if not super().has_permission()[0]:  # pragma: no cover
            return False, None
        if self.instance.instance_state.name in [
            "sb1",
            "sb2",
            "conclusion",
            "finished",
        ]:
            return (
                False,
                (
                    "Changing responsibility is not possible after the building permit has been issued.",
                ),
            )
        return True, None

    def get_instance_id(self):
        return (
            self.data.eventChangeResponsibility.planningPermissionApplicationIdentification.dossierIdentification
        )

    def apply(self):
        new_service_id = (
            self.data.eventChangeResponsibility.responsibleDecisionAuthority.decisionAuthority.buildingAuthorityIdentificationType.localOrganisationId.organisationId
        )

        try:
            new_service = Service.objects.get(pk=new_service_id)
        except Service.DoesNotExist:
            raise SendHandlerException("Unknown target service!")

        data = {
            "service_type": "municipality",
            "to": {"id": new_service.pk, "type": "services"},
        }

        Request = namedtuple(
            "Request", ["user", "group", "caluma_info", "query_params", "META"]
        )
        CalumaInfo = namedtuple("CalumaInfo", "context")
        Context = namedtuple("Context", "user")
        request = Request(
            self.user, self.group, CalumaInfo(Context(self.caluma_user)), {}, {}
        )

        serializer = CalumaInstanceChangeResponsibleServiceSerializer(
            self.instance, data=data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()


class AccompanyingReportSendHandler(BaseSendHandler):
    def __init__(self, data, queryset, user, group, auth_header, caluma_user):
        super().__init__(data, queryset, user, group, auth_header, caluma_user)
        self.inquiry = self._get_inquiry()

    def has_permission(self):
        if not super().has_permission():  # pragma: no cover
            return False, None

        if bool(self.inquiry):
            return True, None

        return False, "There is no running inquiry for your service."

    def get_instance_id(self):
        return (
            self.data.eventAccompanyingReport.planningPermissionApplicationIdentification.dossierIdentification
        )

    def _get_inquiry(self):
        return (
            WorkItem.objects.filter(
                task_id=settings.DISTRIBUTION["INQUIRY_TASK"],
                case__family__instance=self.instance,
                addressed_groups__contains=[str(self.group.service_id)],
                status=WorkItem.STATUS_READY,
            )
            .order_by("-created_at")
            .first()
        )

    def apply(self):
        for question, value in [
            (
                # Antwort
                settings.DISTRIBUTION["QUESTIONS"]["STATUS"],
                settings.DISTRIBUTION["ANSWERS"]["STATUS"]["UNKNOWN"],
            ),
            (
                # Stellungnahme
                settings.DISTRIBUTION["QUESTIONS"]["STATEMENT"],
                "; ".join(self.data.eventAccompanyingReport.remark),
            ),
            (
                # Nebenbestimmungen
                settings.DISTRIBUTION["QUESTIONS"]["ANCILLARY_CLAUSES"],
                "; ".join(self.data.eventAccompanyingReport.ancillaryClauses),
            ),
        ]:
            save_answer(
                document=self.inquiry.child_case.document,
                question=Question.objects.get(pk=question),
                value=value,
            )

        attachments = Attachment.objects.filter(
            uuid__in=[d.uuid for d in self.data.eventAccompanyingReport.document]
        )

        if not attachments.exists():
            raise SendHandlerException("Unknown document!")

        workflow_api.complete_work_item(
            work_item=self.inquiry.child_case.work_items.filter(
                task_id=settings.DISTRIBUTION["INQUIRY_ANSWER_FILL_TASK"],
                status=WorkItem.STATUS_READY,
            ).first(),
            user=self.caluma_user,
            context={"inquiry": self.inquiry, "attachments": attachments},
        )


class CloseArchiveDossierSendHandler(BaseSendHandler):
    def has_permission(self):
        if not InstanceService.objects.filter(
            instance=self.instance, active=True, service=self.group.service
        ).exists():
            return False, None
        if self.instance.instance_state.name in ["sb1", "sb2", "conclusion"]:
            return True, None
        return (
            False,
            (
                '"CloseDossier" is only allowed for instances in the states '
                '"Selbstdeklaration (SB1)", "Abschluss (SB2)" and "Zum Abschluss".'
            ),
        )

    def get_instance_id(self):
        return (
            self.data.eventCloseArchiveDossier.planningPermissionApplicationIdentification.dossierIdentification
        )

    def apply(self):
        self.skip_work_item("sb1")
        self.skip_work_item("sb2")
        self.complete_work_item("complete")


class TaskSendHandler(BaseSendHandler):
    def get_instance_id(self):
        return (
            self.data.eventRequest.planningPermissionApplicationIdentification.dossierIdentification
        )

    def has_permission(self):
        if not super().has_permission()[0]:  # pragma: no cover
            return False, None
        if not self.instance.instance_state.name == "circulation":
            return (
                False,
                'You can only send a "Task" for instances in the state "In Zirkulation".',
            )

        return True, None

    def _get_create_inquiry(self):
        task_id = settings.DISTRIBUTION["INQUIRY_CREATE_TASK"]

        try:
            return WorkItem.objects.get(
                task_id=task_id,
                case__family__instance=self.instance,
                addressed_groups__contains=[str(self.group.service.pk)],
                status=WorkItem.STATUS_READY,
            )
        except WorkItem.DoesNotExist:
            raise SendHandlerException(f"No '{task_id}' work item found!")
        except WorkItem.MultipleObjectsReturned:
            raise SendHandlerException(f"More than one '{task_id}' work item found!")

    def _get_service(self):
        try:
            return Service.objects.get(
                pk=int(
                    self.data.eventRequest.extension.wildcardElements()[
                        0
                    ].firstChild.value
                )
            )
        except (ValueError, Service.DoesNotExist):
            raise SendHandlerException("Unknown service!")

    def _get_inquiry(self, service):
        return (
            WorkItem.objects.filter(
                task_id=settings.DISTRIBUTION["INQUIRY_TASK"],
                case__family__instance=self.instance,
                addressed_groups__contains=[str(service.pk)],
                controlling_groups__contains=[str(self.group.service.pk)],
                status=WorkItem.STATUS_SUSPENDED,
            )
            .order_by("created_at")
            .first()
        )

    def apply(self):
        service = self._get_service()

        if service == self.group.service:
            raise SendHandlerException(
                "Services can't create inquiries for themselves!"
            )

        workflow_api.complete_work_item(
            work_item=self._get_create_inquiry(),
            user=self.caluma_user,
            context={"addressed_groups": [str(service.pk)]},
        )

        inquiry = self._get_inquiry(service)

        try:
            save_answer(
                document=inquiry.document,
                question=Question.objects.get(
                    pk=settings.DISTRIBUTION["QUESTIONS"]["DEADLINE"]
                ),
                value=self.data.eventRequest.directive.deadline.date(),
            )
        # Fallback for messages with missing `directive`, this will use the
        # default deadline
        except AttributeError:  # pragma: no cover
            pass

        workflow_api.resume_work_item(work_item=inquiry, user=self.caluma_user)


class KindOfProceedingsSendHandler(DocumentAccessibilityMixin, BaseSendHandler):
    def __init__(self, data, queryset, user, group, auth_header, caluma_user):
        super().__init__(data, queryset, user, group, auth_header, caluma_user)
        self.attachments = self.get_attachments(
            self.data.eventKindOfProceedings.document
        )

    def get_instance_id(self):
        return (
            self.data.eventKindOfProceedings.planningPermissionApplicationIdentification.dossierIdentification
        )

    def has_permission(self):
        if not super().has_permission():  # pragma: no cover
            return False, None

        if self.instance.instance_state.name != "circulation_init":
            return (
                False,
                'You can only send a "KindOfProceedings" for instances in the state "Zirkulation initialisieren".',
            )

        return True, None

    def apply(self):
        if not self.has_attachment_permissions(self.attachments):
            raise SendHandlerException(
                "You don't have permission for at least one document you provided.",
                status=403,
            )

        self.complete_work_item(settings.DISTRIBUTION["DISTRIBUTION_INIT_TASK"])
        self.link_to_section(self.attachments)


def resolve_send_handler(data):
    handler_mapping = {
        "eventAccompanyingReport": AccompanyingReportSendHandler,
        "eventChangeResponsibility": ChangeResponsibilitySendHandler,
        "eventCloseArchiveDossier": CloseArchiveDossierSendHandler,
        "eventNotice": NoticeRulingSendHandler,
        "eventRequest": TaskSendHandler,
        "eventKindOfProceedings": KindOfProceedingsSendHandler,
    }
    for event in handler_mapping:
        if getattr(data, event) is not None:
            return handler_mapping[event]
    raise SendHandlerException("Message type not supported!")


def get_send_handler(data, instance, user, group, auth_header, caluma_user):
    return resolve_send_handler(data)(
        data, instance, user, group, auth_header, caluma_user
    )
