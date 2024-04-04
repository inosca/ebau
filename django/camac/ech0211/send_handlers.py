from typing import List, Tuple

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

from camac.alexandria.extensions.permissions.extension import (
    MODE_CREATE,
    CustomPermission as CustomAlexandriaPermission,
)
from camac.caluma.api import CalumaApi
from camac.constants.kt_bern import ATTACHMENT_SECTION_ALLE_BETEILIGTEN
from camac.core.utils import canton_aware
from camac.document.models import Attachment, AttachmentSection
from camac.instance.domain_logic import CreateInstanceLogic
from camac.instance.models import Instance, InstanceAlexandriaDocument, InstanceState
from camac.instance.serializers import (
    CalumaInstanceChangeResponsibleServiceSerializer,
    CalumaInstanceSubmitSerializer,
)
from camac.permissions import events as permissions_events
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
        self, xmlDocuments, category: alexandria_models.Category
    ) -> List[alexandria_models.Document]:
        documents_to_link = []
        for doc in xmlDocuments:
            document = None
            titles = {}
            for title in doc.titles.title:
                titles[title.lang or "de"] = title.value()
            for file in doc.files.file:
                file_response = requests.get(file.pathFileName)
                file_name = file.pathFileName.split("/")[-1]
                file_obj = ContentFile(file_response.content, name=file_name)
                if not document:
                    document, __ = create_alexandria_document_file(
                        user=self.user,
                        group=self.group,
                        category=category,
                        document_title=titles,
                        file_name=file_name,
                        file_content=file_obj,
                        mime_type=file.mimeType,
                        file_size=len(file_response.content),
                        additional_document_attributes={
                            "metainfo": {
                                "ech-uuid": doc.uuid,
                            }
                        },
                    )
                else:
                    create_alexandria_file(
                        user=self.user,
                        group=self.group,
                        document=document,
                        name=file_name,
                        content=file_obj,
                        mime_type=file.mimeType,
                        size=len(file_response.content),
                    )
            documents_to_link.append(document)
        return documents_to_link

    def has_alexandria_category_permission(self, category: alexandria_models.Category):
        available_permissions = CustomAlexandriaPermission().get_available_permissions(
            self.request,
            self.instance,
            category,
        )
        if MODE_CREATE not in available_permissions:
            raise SendHandlerException(
                "Document category permission denied.",
                status=400,
            )

    def link_alexandria_documents(self, documents: List[alexandria_models.Document]):
        for document in documents:
            InstanceAlexandriaDocument.objects.create(
                instance=self.instance, document=document
            )


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

    def has_permission(self):
        return self.instance.responsible_service() == self.group.service, None

    def apply(self):  # pragma: no cover
        raise NotImplementedError()


class NoticeRulingSendHandler(AttachmentAccessibilityMixin, BaseSendHandler):
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
            self.skip_work_item(settings.DISTRIBUTION["DISTRIBUTION_TASK"])

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

            if workflow_slug == "building-permit":
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


class AccompanyingReportSendHandler(BaseSendHandler):
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
        if (
            self.instance.responsible_service(filter_type="construction_control")
            != self.group.service
        ):
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
        return self.data.eventCloseArchiveDossier.planningPermissionApplicationIdentification.dossierIdentification

    def apply(self):
        self.skip_work_item("sb1")
        self.skip_work_item("sb2")
        self.complete_work_item("complete")


class TaskSendHandler(BaseSendHandler):
    def get_instance_id(self):
        return self.data.eventRequest.planningPermissionApplicationIdentification.dossierIdentification

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
            service_id = self.data.eventRequest.extension.wildcardElements()[
                0
            ].firstChild.value
            return Service.objects.get(pk=int(service_id))
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


class KindOfProceedingsSendHandler(AttachmentAccessibilityMixin, BaseSendHandler):
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


class SubmitPlanningPermissionApplicationSendHandler(
    BaseSendHandler, AlexandriaDocumentMixin
):
    def _get_instance(self, queryset) -> Instance:
        if self._is_event_type_submit():
            return None

        return super()._get_instance(queryset)

    def has_permission(self) -> Tuple[bool, str]:
        if (
            self.group.role.name
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
        value = xml_element[0].text if xml_element else question_config["default"]
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
        self.has_alexandria_category_permission(alexandria_category)
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
