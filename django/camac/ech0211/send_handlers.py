from typing import List, Tuple
from urllib.parse import urlparse
from uuid import UUID

import requests
from alexandria.core import models as alexandria_models
from alexandria.core.api import (
    create_document_file as create_alexandria_document_file,
    create_file as create_alexandria_file,
)
from caluma.caluma_form.api import save_answer, save_document
from caluma.caluma_form.models import Form, Question
from caluma.caluma_workflow import api as workflow_api
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils.translation import gettext as _
from lxml import etree

from camac.alexandria.extensions.common import (
    has_alexandria_create_permission,
    has_alexandria_move_permission,
)
from camac.alexandria.extensions.visibilities import (
    CustomVisibility as CustomAlexandriaVisibility,
)
from camac.caluma.api import CalumaApi
from camac.caluma.models import Inquiry
from camac.constants.kt_bern import ATTACHMENT_SECTION_ALLE_BETEILIGTEN
from camac.core.utils import canton_aware
from camac.document.models import Attachment, AttachmentSection
from camac.instance.domain_logic import CreateInstanceLogic
from camac.instance.models import Instance, InstanceAlexandriaDocument, InstanceState
from camac.instance.serializers import (
    CalumaInstanceChangeResponsibleServiceSerializer,
    CalumaInstanceSubmitSerializer,
)
from camac.permissions import api as permissions_api, events as permissions_events
from camac.user.models import Service

from .constants import ECH0211_NAMESPACES, ECH_JUDGEMENT_DECLINED
from .parsers import ComplexSubmitMappings
from .signals import ruling
from .utils import judgement_to_decision


class SendHandlerException(Exception):
    def __init__(self, message, status=400):
        super().__init__(message)
        self.status = status


class AttachmentAccessibilityMixin:
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


class AlexandriaDocumentMixin:
    def create_alexandria_documents(
        self,
        xmlDocuments,
        category: alexandria_models.Category,
        skip_linking=False,
        caluma_document_id=None,
        raise_on_download_error=True,
    ) -> List[alexandria_models.Document]:
        created_documents = []
        all_documents = []
        for doc in xmlDocuments:
            # The uuid 00000000-0000-0000-0000-000000000000 (which UUID(int=0) returns)
            # means that the file has a download link and does not exist yet. If the
            # uuid is anything else, we expect that the document has already been created.
            if UUID(doc.uuid) == UUID(int=0):
                if document := self.create_document_and_files(
                    doc, category, caluma_document_id, raise_on_download_error
                ):
                    created_documents.append(document)
            else:
                document = self.get_existing_document(doc.uuid)

            all_documents.append(document)

        if not skip_linking:
            self.link_alexandria_documents(created_documents)

        return all_documents

    def check_alexandria_category_permission(
        self, category: alexandria_models.Category
    ):
        if not has_alexandria_create_permission(self.request, self.instance, category):
            raise SendHandlerException(
                "Document category permission denied.",
                status=400,
            )

    def check_alexandria_category_move_permission(
        self,
        document: alexandria_models.Document,
        new_category: alexandria_models.Category,
    ):
        if not has_alexandria_move_permission(
            self.request,
            self.instance,
            document=document,
            new_category=new_category,
        ):
            raise SendHandlerException(
                "Document category permission denied.",
                status=400,
            )

    def link_alexandria_documents(self, documents: List[alexandria_models.Document]):
        for document in documents:
            InstanceAlexandriaDocument.objects.create(
                instance=self.instance, document=document
            )
            document.metainfo["camac-instance-id"] = self.instance.pk
            document.save()

    def convert_xml_to_alexandria_documents(
        self,
        xmlDocuments,
        category_slug: str,
        caluma_document_id=None,
        raise_on_download_error=True,
    ):
        category = alexandria_models.Category.objects.get(slug=category_slug)
        self.check_alexandria_category_permission(category)
        return self.create_alexandria_documents(
            xmlDocuments,
            category,
            caluma_document_id=caluma_document_id,
            raise_on_download_error=raise_on_download_error,
        )

    def get_existing_document(self, document_uuid):
        document = (
            CustomAlexandriaVisibility()
            .filter_queryset_for_document(
                alexandria_models.Document.objects.filter(pk=document_uuid),
                self.request,
            )
            .first()
        )
        # Validate that Document with specified uuid exists
        if not document:  # pragma: no cover
            raise SendHandlerException(
                f'Document "{document_uuid}" does not exist. Make sure to upload the document beforehand.'
            )
        return document

    def create_document_and_files(
        self, doc, category, caluma_document_id, raise_on_download_error=True
    ):
        document = None
        # use first title as document title
        title = doc.titles.title[0].value()
        description = doc.comments.comment[0].value() if doc.comments else None
        for file in doc.files.file:
            file_response = requests.get(file.pathFileName)
            try:
                file_response.raise_for_status()
            except Exception:  # pragma: todo cover
                # FIXME: coverage here is missing (exception block), need to investigate
                # The inner block raise_on_download_error) was never covered.

                if raise_on_download_error:  # pragma: no cover
                    raise SendHandlerException(
                        f'File at "{file.pathFileName}" could not be downloaded.'
                    )
                continue

            file_name = urlparse(file.pathFileName).path.split("/")[-1]
            file_obj = ContentFile(file_response.content, name=file_name)
            if not document:
                document, __ = create_alexandria_document_file(
                    user=str(self.user.pk),
                    group=str(self.group.service.pk),
                    category=category,
                    document_title=title,
                    file_name=file_name,
                    file_content=file_obj,
                    mime_type=file.mimeType,
                    file_size=len(file_response.content),
                    additional_document_attributes={
                        "description": description,
                    },
                )
            else:
                create_alexandria_file(
                    user=str(self.user.pk),
                    group=str(self.group.service.pk),
                    document=document,
                    name=file_name,
                    content=file_obj,
                    mime_type=file.mimeType,
                    size=len(file_response.content),
                )

        if document and caluma_document_id:  # pragma: no cover
            document.metainfo["caluma-document-id"] = caluma_document_id
            document.save()
        return document


class BaseSendHandler:
    def __init__(self, data, queryset, user, group, auth_header, caluma_user, request):
        self.data = data
        self.user = user
        self.group = group
        self.auth_header = auth_header
        self.caluma_user = caluma_user
        self.instance = self._get_instance(queryset)
        self.request = request

    def _get_instance(self, queryset):
        try:
            return queryset.get(pk=self.get_instance_id())
        except Instance.DoesNotExist:
            raise SendHandlerException("Unknown instance")
        except ValueError:
            raise SendHandlerException(
                "dossierIdentification must be of type integer", status=400
            )

    def get_instance_id(self):  # pragma: no cover
        raise NotImplementedError()

    def complete_work_item(self, task, filters={}, context={}):
        return self._process_work_item("complete", task, filters, context)

    def skip_work_item(self, task, filters={}, context={}):
        return self._process_work_item("skip", task, filters, context)

    def _process_work_item(self, action, task, filters, context):
        fn = getattr(workflow_api, f"{action}_work_item")
        work_item = WorkItem.objects.filter(
            case__family=self.instance.case,
            task_id=task,
            status=WorkItem.STATUS_READY,
            **filters,
        ).first()

        if work_item and fn:
            fn(work_item=work_item, user=self.caluma_user, context=context)

        return work_item

    def has_permission(self):
        return self.instance.responsible_service() == self.group.service, None

    def apply(self):  # pragma: no cover
        raise NotImplementedError()


class NoticeRulingSendHandler(
    AttachmentAccessibilityMixin, AlexandriaDocumentMixin, BaseSendHandler
):
    def get_instance_id(self):
        return self.data.eventNotice.planningPermissionApplicationIdentification.dossierIdentification

    def has_permission(self):
        if not super().has_permission()[0]:
            return False, None

        if self.instance.instance_state.name in settings.ECH0211["NOTICE_RULING"].get(
            "ONLY_DECLINE", []
        ):
            if self.data.eventNotice.decisionRuling.judgement != ECH_JUDGEMENT_DECLINED:
                return (
                    False,
                    f'For instances in the state "Zirkulation initialisieren", only a NoticeRuling with judgement "{ECH_JUDGEMENT_DECLINED}" is allowed.',
                )
            return True, None
        if self.instance.instance_state.name not in settings.ECH0211[
            "NOTICE_RULING"
        ].get("ALLOWED_STATES", []):
            return (
                False,
                'NoticeRuling is only allowed for instances in the state "In Koordination" or "In Zirkulation".',
            )

        return True, None

    @canton_aware
    def _find_and_fill_geometer(self, decision_document):  # pragma: no cover
        pass

    def _find_and_fill_geometer_be(self, decision_document):
        # We only fill this answer if it's not already done
        question_slug = "decision-geometer"
        if decision_document.answers.filter(question_id=question_slug).exists():
            return  # pragma: no cover

        save_answer(
            document=decision_document,
            question=Question.objects.get(slug=question_slug),
            value="decision-geometer-no",
        )

    def _get_decision_document(self, case):
        decision_document = case.work_items.get(
            task_id=settings.DECISION["TASK"], status=WorkItem.STATUS_READY
        ).document
        return decision_document

    def apply(self):
        if settings.APPLICATION["DOCUMENT_BACKEND"] == "alexandria":
            decision_mark = alexandria_models.Mark.objects.get(
                pk=settings.ECH0211["NOTICE_RULING"]["ALEXANDRIA_MARK"]
            )
            alexandria_category = alexandria_models.Category.objects.get(
                slug=settings.ECH0211["NOTICE_RULING"]["ALEXANDRIA_CATEGORY"]
            )
            alexandria_documents = self.convert_xml_to_alexandria_documents(
                self.data.eventNotice.document, alexandria_category.slug
            )
            for doc in alexandria_documents:
                if doc.category != alexandria_category:
                    self.check_alexandria_category_move_permission(
                        document=doc, new_category=alexandria_category
                    )

                    doc.category = alexandria_category
                    doc.save(update_fields=["category"])

                doc.marks.add(decision_mark)
        else:
            attachments = self.get_attachments(self.data.eventNotice.document)
            if not self.has_attachment_permissions(attachments):
                raise SendHandlerException(
                    "You don't have permission for at least one document you provided.",
                    status=403,
                )

        case = self.instance.case
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
            self.instance.set_instance_state("rejected", self.user)

            # question *may* be hidden here if it's not a building-permit,
            # but we don't care and fill anyway
            try:
                self._find_and_fill_geometer(self._get_decision_document(case))
            except WorkItem.DoesNotExist:
                # Happens if we're too early in the workflow
                pass

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
            for slug in settings.ECH0211["NOTICE_RULING"].get(
                "SKIP_TASKS_ON_APPROVAL", []
            ):
                self.skip_work_item(slug)

            # write the decision document
            decision_document = self._get_decision_document(case)
            save_answer(
                document=decision_document,
                question=Question.objects.get(
                    slug=settings.DECISION["QUESTIONS"]["DECISION"]
                ),
                value=decision,
            )
            save_answer(
                document=decision_document,
                question=Question.objects.get(
                    slug=settings.DECISION["QUESTIONS"]["DATE"]
                ),
                date=self.data.eventNotice.decisionRuling.date.date(),
            )

            self._find_and_fill_geometer(decision_document)

            if (
                workflow_slug == "building-permit"
                and "APPROVAL_TYPE" in settings.DECISION["QUESTIONS"]
            ):
                save_answer(
                    document=decision_document,
                    question=Question.objects.get(
                        slug=settings.DECISION["QUESTIONS"]["APPROVAL_TYPE"]
                    ),
                    value=settings.DECISION["ANSWERS"]["APPROVAL_TYPE"]["UNKNOWN"],
                )

            # this handle status changes and assignment of the construction control
            # for "normal" judgements
            self.complete_work_item(settings.DECISION["TASK"])

        if settings.APPLICATION["DOCUMENT_BACKEND"] == "camac-ng":
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
                "Changing responsibility is not possible after the building permit has been issued.",
            )
        return True, None

    def get_instance_id(self):
        return self.data.eventChangeResponsibility.planningPermissionApplicationIdentification.dossierIdentification

    def apply(self):
        new_service_id = self.data.eventChangeResponsibility.responsibleDecisionAuthority.decisionAuthority.buildingAuthorityIdentificationType.localOrganisationId.organisationId

        try:
            new_service = Service.objects.get(pk=new_service_id)
        except Service.DoesNotExist:
            raise SendHandlerException("Unknown target service!")

        data = {
            "service_type": "municipality",
            "to": {"id": new_service.pk, "type": "services"},
        }

        # TODO: move business logic into domain logic to make this less awkward
        serializer = CalumaInstanceChangeResponsibleServiceSerializer(
            self.instance, data=data, context={"request": self.request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()


class AccompanyingReportSendHandler(AlexandriaDocumentMixin, BaseSendHandler):
    def __init__(self, data, queryset, user, group, auth_header, caluma_user, request):
        super().__init__(data, queryset, user, group, auth_header, caluma_user, request)
        self.inquiry = self._get_inquiry()

    def has_permission(self):
        if not super().has_permission():  # pragma: no cover
            return False, None

        if bool(self.inquiry):
            return True, None

        return False, "There is no running inquiry for your service."

    def get_instance_id(self):
        return self.data.eventAccompanyingReport.planningPermissionApplicationIdentification.dossierIdentification

    def _get_inquiry(self):
        return (
            Inquiry.objects.for_instance(self.instance)
            .addressed_to(self.group.service_id)
            .only_pending()
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
                settings.DISTRIBUTION["QUESTIONS"].get("ANCILLARY_CLAUSES"),
                "; ".join(self.data.eventAccompanyingReport.ancillaryClauses),
            ),
        ]:
            if question:
                save_answer(
                    document=self.inquiry.child_case.document,
                    question=Question.objects.get(pk=question),
                    value=value,
                )

        if extensions := settings.ECH0211["ACCOMPANYING_REPORT"].get(
            "EXTENSION_MAPPING"
        ):
            elements = self.data.eventAccompanyingReport.extension.wildcardElements()

            for slug, mapping in extensions.items():
                el = next((el for el in elements if el.tagName == mapping["tag"]))
                question = Question.objects.get(pk=slug)

                text_value = el.firstChild.value.strip()

                value = text_value
                # map values for choice questions
                if text_value == "true" and mapping.get("true_value", None) is not None:
                    value = (
                        [mapping["true_value"]]
                        if question.type == Question.TYPE_MULTIPLE_CHOICE
                        else mapping["true_value"]
                    )
                elif text_value == "false":
                    value = [] if question.type == Question.TYPE_MULTIPLE_CHOICE else ""

                save_answer(
                    document=self.inquiry.child_case.document,
                    question=question,
                    value=value,
                )

        if settings.APPLICATION["DOCUMENT_BACKEND"] == "alexandria":
            documents = self.convert_xml_to_alexandria_documents(
                self.data.eventAccompanyingReport.document,
                settings.ECH0211["ACCOMPANYING_REPORT"]["ALEXANDRIA_CATEGORY"],
            )
            # turn list into queryset, expected by subsequent event handlers
            documents = alexandria_models.Document.objects.filter(
                id__in=[d.id for d in documents]
            )
        else:
            documents = Attachment.objects.filter(
                uuid__in=[d.uuid for d in self.data.eventAccompanyingReport.document]
            )
            if not documents.exists():
                raise SendHandlerException("Unknown document!")

        workflow_api.complete_work_item(
            work_item=self.inquiry.child_case.work_items.filter(
                task_id=settings.DISTRIBUTION["INQUIRY_ANSWER_FILL_TASK"],
                status=WorkItem.STATUS_READY,
            ).first(),
            user=self.caluma_user,
            context={"inquiry": self.inquiry, "documents": documents},
        )


class CloseArchiveDossierSendHandler(BaseSendHandler):
    def has_permission(self):
        if (
            settings.APPLICATION.get("USE_CONSTRUCTION_CONTROL", False)
            and self.instance.responsible_service(filter_type="construction_control")
            != self.group.service
        ):
            return False, "The current service does not match the responsible service."

        allowed_states = settings.ECH0211.get("CLOSE_DOSSIER", {}).get(
            "ALLOWED_STATES", []
        )
        if self.instance.instance_state.name in allowed_states:
            return True, None

        return (
            False,
            f'"CloseDossier" is only allowed for instances in the states {", ".join(allowed_states)}',
        )

    def get_instance_id(self):
        return self.data.eventCloseArchiveDossier.planningPermissionApplicationIdentification.dossierIdentification

    def apply(self):
        for action, task, context in settings.ECH0211.get("CLOSE_DOSSIER", {}).get(
            "WORK_ITEM_ACTIONS", []
        ):
            self._process_work_item(action, task, {}, context)


class TaskSendHandler(AlexandriaDocumentMixin, BaseSendHandler):
    def _is_event_type_claim(self) -> bool:
        return self.data.eventRequest.eventType == "claim"

    def has_permission(self):
        return (
            self.has_permission_claim()
            if self._is_event_type_claim()
            else self.has_permission_task()
        )

    def apply(self):
        return (
            self._apply_claim() if self._is_event_type_claim() else self._apply_task()
        )

    def _get_create_inquiry(self):
        return self._get_work_item(
            settings.DISTRIBUTION["INQUIRY_CREATE_TASK"],
        )

    def _get_additional_demand(self, additional_demand_init):
        return self._get_work_item(
            settings.ADDITIONAL_DEMAND["TASK"],
            **{
                "previous_work_item": additional_demand_init,
            },
        )

    def get_instance_id(self):
        return self.data.eventRequest.planningPermissionApplicationIdentification.dossierIdentification

    def _get_work_item(self, task_id, **kwargs):
        try:
            return WorkItem.objects.get(
                task_id=task_id,
                case__family__instance=self.instance,
                addressed_groups__contains=[str(self.group.service.pk)],
                status=WorkItem.STATUS_READY,
                **kwargs,
            )
        except WorkItem.DoesNotExist:
            raise SendHandlerException(f"No '{task_id}' work item found!")
        except WorkItem.MultipleObjectsReturned:
            raise SendHandlerException(f"More than one '{task_id}' work item found!")

    def _get_service(self):
        try:
            service_id = self.data.eventRequest.extension.wildcardElements()[
                0
            ].firstChild.value
            return Service.objects.get(pk=int(service_id))
        except (ValueError, Service.DoesNotExist):
            raise SendHandlerException("Unknown service!")

    def _get_inquiry(self, service):
        return (
            Inquiry.objects.for_instance(self.instance)
            .addressed_to(service)
            .controlled_by(self.group.service)
            .only_drafts()
            .order_by("created_at")
            .first()
        )

    def has_permission_task(self):
        base_permission = super().has_permission()
        if not base_permission or not base_permission[0]:  # pragma: no cover
            return False, None

        if (
            settings.APPLICATION_NAME == "kt_bern"
            and not self.instance.instance_state.name == "circulation"
        ):
            return (
                False,
                'You can only send a "Task" for instances in the state "In Zirkulation".',
            )

        return True, None

    def has_permission_claim(self):
        # we don't call super().has_permission() for claims, because we don't want
        # to require only the responsible service to send a claim
        if not settings.ECH0211.get("CLAIM", {}).get("ENABLED", False):
            return (
                False,
                "Claim is not enabled for this application.",
            )

        if not permissions_api.PermissionManager.from_request(self.request).has_all(
            self.instance, "additional-demands-write"
        ):
            return (
                False,
                "You don't have permission to send a claim.",
            )

        return True, None

    def _apply_claim(self):
        # complete init workitem to create the additional demand
        additional_demand_init = self.complete_work_item(
            settings.ADDITIONAL_DEMAND["CREATE_TASK"],
            {
                "addressed_groups__contains": [str(self.group.service.pk)],
            },
        )

        # fetch the additional demand work item
        additional_demand = self._get_additional_demand(additional_demand_init)

        # fetch and fill the additional demand send work item,
        # and fill the deadline and comment
        additional_demand_send = additional_demand.child_case.work_items.get(
            task_id=settings.ADDITIONAL_DEMAND["SEND_TASK"],
            status=WorkItem.STATUS_READY,
        )
        save_answer(
            document=additional_demand_send.document,
            question=Question.objects.get(
                pk=settings.ADDITIONAL_DEMAND["QUESTIONS"]["DEADLINE"]
            ),
            value=self.data.eventRequest.directive.deadline.date(),
        )
        save_answer(
            document=additional_demand_send.document,
            question=Question.objects.get(
                pk=settings.ADDITIONAL_DEMAND["QUESTIONS"]["COMMENT"]
            ),
            value="\n".join(
                [
                    c.value.value()
                    for c in self.data.eventRequest.directive.comments.orderedContent()
                ]
            ),
        )

        # store alexandria documents and link to additional demand document
        self.convert_xml_to_alexandria_documents(
            self.data.eventRequest.directive.documents.document,
            category_slug=settings.ECH0211["CLAIM"]["ALEXANDRIA_CATEGORY"],
            caluma_document_id=str(additional_demand_send.document.pk),
            raise_on_download_error=False,
        )

        # complete the additional demand send work item after filling out the form
        # and linking the documents
        self.complete_work_item(
            settings.ADDITIONAL_DEMAND["SEND_TASK"],
            {
                "pk": additional_demand_send.pk,
            },
        )

        # store meta information for all work items for later processing
        # during the applicant fill task
        update_work_items = set(
            [
                additional_demand_init,
                additional_demand,
                *additional_demand.child_case.work_items.all(),
            ]
        )
        for work_item in update_work_items:
            work_item.meta["ech-init-workitem"] = str(additional_demand_init.pk)
            work_item.save(update_fields=["meta"])

            # mark the fill task `additional-demand-ech0211` answer as "true".
            # this will be used in JEXL evaluation to show/hide fields.
            if work_item.task.slug == settings.ADDITIONAL_DEMAND["FILL_TASK"]:
                save_answer(
                    document=work_item.document,
                    question=Question.objects.get(slug="additional-demand-ech0211"),
                    value="true",
                )

        return self.instance

    def _apply_task(self):
        service = self._get_service()

        if service == self.group.service:
            raise SendHandlerException(
                "Services can't create inquiries for themselves!"
            )

        if settings.ECH0211.get("TASK_SEND"):
            for setting_key, fun in (
                ("SKIP_WORK_ITEMS", workflow_api.skip_work_item),
                ("COMPLETE_WORK_ITEMS", workflow_api.complete_work_item),
            ):
                for task in settings.ECH0211["TASK_SEND"].get(setting_key):
                    if work_item := WorkItem.objects.filter(
                        task_id=task,
                        case__family__instance=self.instance,
                        addressed_groups__contains=[str(self.group.service.pk)],
                        status=WorkItem.STATUS_READY,
                    ).first():
                        fun(
                            work_item=work_item,
                            user=self.caluma_user,
                            context={"addressed_groups": [str(self.group.service.pk)]},
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
            save_answer(
                document=inquiry.document,
                question=Question.objects.get(
                    pk=settings.DISTRIBUTION["QUESTIONS"]["REMARK"]
                ),
                value="\n".join(
                    [
                        c.value.value()
                        for c in self.data.eventRequest.directive.comments.orderedContent()
                    ]
                ),
            )
        # Fallback for messages with missing `directive`, this will use the
        # default deadline
        except AttributeError:  # pragma: no cover
            pass

        workflow_api.resume_work_item(work_item=inquiry, user=self.caluma_user)


class KindOfProceedingsSendHandler(
    AttachmentAccessibilityMixin, AlexandriaDocumentMixin, BaseSendHandler
):
    def __init__(self, data, queryset, user, group, auth_header, caluma_user, request):
        super().__init__(data, queryset, user, group, auth_header, caluma_user, request)
        self.attachments = self.get_attachments(
            self.data.eventKindOfProceedings.document
        )

    def get_instance_id(self):
        return self.data.eventKindOfProceedings.planningPermissionApplicationIdentification.dossierIdentification

    def has_permission(self):
        if not super().has_permission():  # pragma: no cover
            return False, None

        if (
            settings.APPLICATION_NAME == "kt_bern"
            and self.instance.instance_state.name != "circulation_init"
        ):
            return (
                False,
                'You can only send a "KindOfProceedings" for instances in the state "Zirkulation initialisieren".',
            )

        return True, None

    def apply(self):
        if settings.APPLICATION["DOCUMENT_BACKEND"] == "alexandria":
            self.convert_xml_to_alexandria_documents(
                self.data.eventKindOfProceedings.document,
                settings.ECH0211["KIND_OF_PROCEEDINGS"]["ALEXANDRIA_CATEGORY"],
            )
            self.complete_work_item(settings.DISTRIBUTION["DISTRIBUTION_INIT_TASK"])
            return

        if not self.has_attachment_permissions(self.attachments):
            raise SendHandlerException(
                "You don't have permission for at least one document you provided.",
                status=403,
            )

        self.complete_work_item(settings.DISTRIBUTION["DISTRIBUTION_INIT_TASK"])
        self.link_to_section(self.attachments)


class SubmitPlanningPermissionApplicationSendHandler(
    BaseSendHandler, AlexandriaDocumentMixin
):
    def _get_instance(self, queryset) -> Instance:
        if self._is_event_type_submit():
            return None

        return super()._get_instance(queryset)

    def has_permission(self) -> Tuple[bool, str]:
        submit_planning_enabled = settings.ECH0211.get(
            "SUBMIT_PLANNING_PERMISSION_APPLICATION", {}
        ).get("ENABLED", False)

        if (
            submit_planning_enabled
            and self.group.role.name
            in settings.ECH0211["SUBMIT_PLANNING_PERMISSION_APPLICATION"][
                "ALLOWED_ROLES"
            ]
        ):
            if self._is_event_type_submit():
                return True, None
            else:
                return super().has_permission()

        return False, None

    def get_instance_id(self) -> str:
        return self.data.eventSubmitPlanningPermissionApplication.planningPermissionApplication.planningPermissionApplicationIdentification.dossierIdentification

    def _save_xml_to_caluma(self, xml_tree, path: str, document, question_config: dict):
        xml_element = xml_tree.xpath(path, namespaces=ECH0211_NAMESPACES)

        value = question_config.get("default")
        if xml_element:
            value = xml_element[0].text
            if "default" in question_config:
                value = type(question_config["default"])(value)
            if "static_value" in question_config:
                value = question_config["static_value"]

        if value is None:
            return

        CalumaApi().update_or_create_answer(
            document, question_config["question_slug"], value, self.caluma_user
        )

    def _apply_submit(self) -> Instance:
        # TODO: Since the entire event is handled in one long-running transaction,
        # this code is susceptible to create duplicate dossier identifiers.
        # Consider refactoring along the lines of the regular instance submission
        # (two separate transactions) to make collisions less likely.

        alexandria_category = alexandria_models.Category.objects.get(
            pk=settings.ECH0211["SUBMIT_PLANNING_PERMISSION_APPLICATION"][
                "ALEXANDRIA_CATEGORY"
            ]
        )
        # First download all documents, as this step is most likely to fail
        documents_to_link = self.create_alexandria_documents(
            self.data.eventSubmitPlanningPermissionApplication.planningPermissionApplication.document,
            alexandria_category,
            skip_linking=True,
        )

        instance_state = InstanceState.objects.get(name="subm")
        data = {
            "instance_state": instance_state,
            "previous_instance_state": instance_state,
            "form_id": settings.ECH0211["SUBMIT_PLANNING_PERMISSION_APPLICATION"][
                "FORM_ID"
            ],
            "user": self.user,
            "group": self.group,
            "generate_identifier": True,
        }
        instance = CreateInstanceLogic.create(
            data,
            self.caluma_user,
            self.user,
            self.group,
            start_caluma=True,
            is_paper=True,
            caluma_form=self.data.eventSubmitPlanningPermissionApplication.planningPermissionApplication.applicationType.lower(),
            workflow_slug=settings.ECH0211["SUBMIT_PLANNING_PERMISSION_APPLICATION"][
                "WORKFLOW"
            ],
        )
        self.instance = instance
        # permisison check needs instance
        self.check_alexandria_category_permission(alexandria_category)
        self.link_alexandria_documents(documents_to_link)
        # set submit date (if in xml data) to case meta
        self.instance.case.meta["ech0211-submitted"] = True
        self.instance.case.save()

        lxml_tree = etree.fromstring(
            self.data.eventSubmitPlanningPermissionApplication.toxml("utf-8")
        )

        document = instance.case.document
        for path, question_config in settings.ECH0211[
            "SUBMIT_PLANNING_PERMISSION_APPLICATION"
        ]["QUESTION_MAPPING"]["SIMPLE"].items():
            self._save_xml_to_caluma(lxml_tree, path, document, question_config)

        for path, table_config in settings.ECH0211[
            "SUBMIT_PLANNING_PERMISSION_APPLICATION"
        ]["QUESTION_MAPPING"]["TABLE"].items():
            xml_elements = lxml_tree.xpath(path, namespaces=ECH0211_NAMESPACES)
            if not xml_elements:  # pragma: no cover
                continue

            row_form, row_question, table_question = table_config
            table_rows = []

            for row in xml_elements:
                row_document = save_document(form=Form.objects.get(slug=row_form))
                for value_path, question_config in row_question.items():
                    self._save_xml_to_caluma(
                        row, value_path, row_document, question_config
                    )
                table_rows.append(row_document.pk)

            save_answer(
                document=document,
                question=Question.objects.get(slug=table_question),
                value=table_rows,
            )

        ComplexSubmitMappings.execute(lxml_tree, document, self.caluma_user)

        # TODO extract submit into domain logic
        submit_serializer = CalumaInstanceSubmitSerializer(
            instance=instance, context={"request": self.request}
        )
        case = instance.case

        submit_serializer._set_location_for_municipality(case, instance)
        instance.save()

        submit_serializer._set_instance_service(case, instance)
        submit_serializer._generate_identifier(case, instance)
        submit_serializer._set_submit_date(case, instance)
        submit_serializer._create_history_entry(_("ECH Dossier submitted"))
        submit_serializer._complete_submit_work_item(instance)
        permissions_events.Trigger.instance_submitted(None, instance)

        return instance

    def _apply_file_subsequently(self):
        raise SendHandlerException(
            "Not supported.",
            status=400,
        )

    def _is_event_type_submit(self) -> bool:
        return self.data.eventSubmitPlanningPermissionApplication.eventType == "submit"

    def apply(self) -> Instance:
        if self._is_event_type_submit():
            return self._apply_submit()

        return self._apply_file_subsequently()


def resolve_send_handler(data):
    handler_mapping = {
        "eventAccompanyingReport": AccompanyingReportSendHandler,
        "eventChangeResponsibility": ChangeResponsibilitySendHandler,
        "eventCloseArchiveDossier": CloseArchiveDossierSendHandler,
        "eventNotice": NoticeRulingSendHandler,
        "eventRequest": TaskSendHandler,
        "eventKindOfProceedings": KindOfProceedingsSendHandler,
        "eventSubmitPlanningPermissionApplication": SubmitPlanningPermissionApplicationSendHandler,
    }
    for event in handler_mapping:
        if getattr(data, event) is not None:
            return handler_mapping[event]
    raise SendHandlerException("Message type not supported!")


def get_send_handler(data, instance, user, group, auth_header, caluma_user, request):
    return resolve_send_handler(data)(
        data, instance, user, group, auth_header, caluma_user, request
    )
