import re
from typing import List

import magic
from alexandria.core.api import create_document_file
from alexandria.core.models import Category
from caluma.caluma_form import api as form_api
from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Form as CalumaForm, Question
from caluma.caluma_workflow import api as workflow_api
from caluma.caluma_workflow.api import skip_work_item
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.core.files import File
from django.db import transaction

from camac.caluma.extensions.events.general import get_caluma_setting
from camac.core.models import InstanceService
from camac.core.utils import generate_dossier_nr, generate_sort_key
from camac.dossier_import.dossier_classes import Dossier
from camac.dossier_import.messages import (
    DOSSIER_IMPORT_STATUS_ERROR,
    DOSSIER_IMPORT_STATUS_SUCCESS,
    DOSSIER_IMPORT_STATUS_WARNING,
    DossierSummary,
    Message,
    MessageCodes,
    Severity,
    get_message_max_level,
)
from camac.dossier_import.validation import TargetStatus
from camac.dossier_import.writers import (
    CalumaAnswerWriter,
    CalumaListAnswerWriter,
    CalumaPlotDataWriter,
    CaseMetaWriter,
    DossierWriter,
)
from camac.instance.domain_logic import CreateInstanceLogic
from camac.instance.models import Form, Instance, InstanceState
from camac.tags.models import Keyword

PERSON_MAPPING = {
    "company": "juristische-person-name",
    "last_name": "nachname",
    "first_name": "vorname",
    "street": "strasse",
    "street_number": "strasse-nummer",
    "zip": "plz",
    "town": "ort",
    "phone": "telefon",
    "email": "e-mail",
}

PLOT_DATA_MAPPING = {
    "plot_number": "parzellennummer",
    "egrid_number": "e-grid",
    "coord_east": "lagekoordinaten-ost",
    "coord_north": "lagekoordinaten-nord",
}


class ConfigurationError(Exception):
    pass


class KtSolothurnDossierWriter(DossierWriter):
    id: str = CalumaAnswerWriter(
        target="kommunale-gesuchsnummer", formatter="to-string"
    )
    proposal = CalumaAnswerWriter(target="umschreibung-bauprojekt")
    cantonal_id = CalumaAnswerWriter(target="kantonale-gesuchsnummer")
    plot_data = CalumaPlotDataWriter(
        target="parzellen", column_mapping=PLOT_DATA_MAPPING
    )
    usage = CalumaAnswerWriter(target="nutzungsplanung-grundnutzung")
    application_type = CalumaAnswerWriter(target="geschaeftstyp")
    submit_date = CaseMetaWriter(target="submit-date", formatter="datetime-to-string")
    publication_date = CalumaAnswerWriter(target="datum-publikation")
    construction_start_date = CalumaAnswerWriter(target="datum-baubeginn")
    profile_approval_date = CalumaAnswerWriter(target="datum-schnurgeruestabnahme")
    final_approval_date = CalumaAnswerWriter(target="datum-schlussabnahme")
    completion_date = CalumaAnswerWriter(target="bauende")
    link = CalumaAnswerWriter(target="link")
    custom_1 = CalumaAnswerWriter(target="freies-textfeld-1")
    custom_2 = CalumaAnswerWriter(target="freies-textfeld-2")
    street = CalumaAnswerWriter(target="strasse-flurname")
    street_number = CalumaAnswerWriter(target="strasse-nummer", formatter="to-string")
    city = CalumaAnswerWriter(target="ort")
    applicant = CalumaListAnswerWriter(
        target="bauherrin", column_mapping=PERSON_MAPPING
    )
    landowner = CalumaListAnswerWriter(
        target="grundeigentuemerin", column_mapping=PERSON_MAPPING
    )
    project_author = CalumaListAnswerWriter(
        target="projektverfasserin", column_mapping=PERSON_MAPPING
    )

    def create_instance(self, dossier: Dossier) -> Instance:
        instance_state = InstanceState.objects.get(
            pk=settings.DOSSIER_IMPORT["INSTANCE_STATE_MAPPING"].get(
                dossier._meta.target_state
            )
        )

        creation_data = dict(
            instance_state=instance_state,
            previous_instance_state=instance_state,
            user=self._user,
            group=self._group,
            form=Form.objects.get(pk=settings.DOSSIER_IMPORT["FORM_ID"]),
        )

        instance = CreateInstanceLogic.create(
            creation_data,
            caluma_user=self._caluma_user,
            camac_user=self._user,
            group=self._group,
            caluma_form=CalumaForm.objects.get(
                pk=settings.DOSSIER_IMPORT["CALUMA_FORM"]
            ),
            start_caluma=True,
        )

        dossier_number = generate_dossier_nr(instance, dossier.submit_date.year)
        instance.case.meta.update(
            {
                "dossier-number": dossier_number,
                "dossier-number-sort": generate_sort_key(dossier_number),
            }
        )
        instance.case.save()

        InstanceService.objects.create(
            instance=instance,
            service_id=self._group.service_id,
            active=1,
            activation_date=None,
        )

        return instance

    def existing_dossier(self, dossier_id):
        keyword = Keyword.objects.filter(
            name=dossier_id, service=self._group.service
        ).first()

        return keyword.instances.first() if keyword else None

    def set_dossier_id(self, instance, dossier_id):
        keyword = Keyword.objects.filter(
            name=dossier_id, service=self._group.service
        ).first()

        if keyword:  # pragma: no cover
            # This only happens after an import was undone
            keyword.instances.add(instance)
        else:
            instance.keywords.create(name=dossier_id, service=self._group.service)

    @transaction.atomic
    def import_dossier(
        self, dossier: Dossier, import_session_id: str, allow_updates: bool = False
    ) -> DossierSummary:
        dossier_summary = DossierSummary(
            dossier_id=dossier.id, status=DOSSIER_IMPORT_STATUS_SUCCESS, details=[]
        )

        # copy messages from loader to summary
        dossier_summary.details += dossier._meta.errors

        if dossier._meta.missing:
            dossier_summary.details.append(
                Message(
                    level=Severity.ERROR.value,
                    code=MessageCodes.MISSING_REQUIRED_VALUE_ERROR.value,
                    detail=f"missing values in required fields: {dossier._meta.missing}",
                )
            )
            dossier_summary.status = DOSSIER_IMPORT_STATUS_ERROR
            return dossier_summary
        created = False
        if instance := self.existing_dossier(dossier.id):
            if not allow_updates:  # pragma: todo cover
                dossier_summary.details.append(
                    Message(
                        level=Severity.WARNING.value,
                        code=MessageCodes.DUPLICATE_DOSSIER.value,
                        detail=f"Dossier with ID {dossier.id} already exists.",
                    )
                )
                dossier_summary.status = DOSSIER_IMPORT_STATUS_ERROR
                return dossier_summary
        else:
            instance = self.create_instance(dossier)
            created = True
            self.set_dossier_id(instance, dossier.id)

            dossier_summary.details.append(
                Message(
                    level=Severity.DEBUG.value,
                    code=MessageCodes.INSTANCE_CREATED.value,
                    detail=f"Instance created with ID:  {instance.pk}",
                )
            )

        dossier_summary.instance_id = instance.pk
        dossier_summary.details += self._create_dossier_attachments(dossier, instance)

        # prevent workflowstate skipping if the instance is updated
        # and also keep history
        if created:
            instance.case.meta["import-id"] = import_session_id
            instance.case.save()

            save_answer(
                document=instance.case.document,
                question=Question.objects.get(slug="gemeinde"),
                value=str(self._group.service_id),
                user=self._caluma_user,
            )

            workflow_message = self._set_workflow_state(instance, dossier)
            dossier_summary.details.append(
                Message(
                    level=get_message_max_level(workflow_message),
                    code=MessageCodes.SET_WORKFLOW_STATE.value,
                    detail=workflow_message,
                )
            )

            instance.history.all().delete()

        self.write_fields(instance, dossier)
        self._write_triage_fields(instance)
        dossier_summary.details += dossier._meta.warnings
        dossier_summary.details += dossier._meta.errors
        dossier_summary.details.append(
            Message(
                level=Severity.DEBUG.value,
                code=MessageCodes.FORM_DATA_WRITTEN.value,
                detail="Form data written.",
            )
        )

        if (
            get_message_max_level(dossier_summary.details) == Severity.ERROR.value
        ):  # pragma: no cover
            dossier_summary.status = DOSSIER_IMPORT_STATUS_ERROR
        if get_message_max_level(dossier_summary.details) == Severity.WARNING.value:
            dossier_summary.status = DOSSIER_IMPORT_STATUS_WARNING  # pragma: no cover

        return dossier_summary

    def _write_triage_fields(self, instance: Instance):
        """Write triage answers for personal data.

        The table questions for landowner, and project author are only displayed
        if the associated triage question whether the data is different from the
        applicant is answered with yes. This method checks if there is any data
        in the personal table and answers the triage question accordingly.
        """

        for table_question in [
            "grundeigentuemerin",
            "projektverfasserin",
            # As the invoice recipient can not be passed to the import, the
            # table will always be empty and the triage question will always be
            # answered with "no". However, we still use the same logic as for
            # the others in order to avoid more code.
            "rechnungsempfaengerin",
        ]:
            table_answer = instance.case.document.answers.filter(
                question_id=table_question
            ).first()
            has_rows = table_answer.documents.exists() if table_answer else False

            suffix = "ja" if has_rows else "nein"
            triage_question = f"{table_question}-abweichend"
            value = f"{triage_question}-{suffix}"

            form_api.save_answer(
                document=instance.case.document,
                question=Question.objects.get(pk=triage_question),
                value=value,
                user=self._caluma_user,
            )

    def _set_workflow_state(self, instance: Instance, dossier) -> List[Message]:
        messages = []
        target_state = dossier._meta.target_state

        SUBMITTED = ["submit"]
        DECIDED = SUBMITTED + [
            "formal-exam",
            "material-exam",
            "distribution",
            "decision",
        ]
        DONE = DECIDED

        path_to_state = {
            "SUBMITTED": SUBMITTED,
            "APPROVED": DECIDED,
            "REJECTED": DECIDED,
            "WRITTEN OFF": DECIDED,
            "DONE": DONE,
        }

        default_context = {"no-notification": True, "no-history": True}

        # In order for a work item to be completed no sibling work items can be
        # in state ready. They have to be dealt with in advance.
        for task_id in path_to_state[target_state]:
            try:
                work_item = instance.case.work_items.get(task_id=task_id)
            except WorkItem.DoesNotExist as e:  # pragma: no cover
                messages.append(
                    Message(
                        level=Severity.ERROR.value,
                        code=MessageCodes.WORKFLOW_SKIP_ITEM_FAILED.value,
                        detail=f"Skip work item with task_id {task_id} failed with {ConfigurationError(e)}.",
                    )
                )
                continue

            if task_id == "decision":
                self.write_decision_form(work_item, dossier)

            if config := get_caluma_setting("PRE_COMPLETE") and get_caluma_setting(
                "PRE_COMPLETE"
            ).get(work_item.task_id):
                for action_name, tasks in config.items():
                    action = getattr(workflow_api, f"{action_name}_work_item")

                    for item in work_item.case.work_items.filter(
                        task_id__in=tasks, status=WorkItem.STATUS_READY
                    ):
                        action(item, self._caluma_user)

            skip_work_item(work_item, user=self._caluma_user, context=default_context)

        messages.append(  # pragma: no cover
            Message(
                level=Severity.DEBUG.value,
                code=MessageCodes.SET_WORKFLOW_STATE.value,
                detail=f"Workflow state set to {target_state}.",
            )
        )

        return messages

    def write_decision_form(self, decision_work_item, dossier):
        decision_mapping = {
            TargetStatus.APPROVED.value: settings.DECISION["ANSWERS"]["DECISION"][
                "APPROVED"
            ],
            TargetStatus.REJECTED.value: settings.DECISION["ANSWERS"]["DECISION"][
                "REJECTED"
            ],
            TargetStatus.WRITTEN_OFF.value: settings.DECISION["ANSWERS"]["DECISION"][
                "WITHDRAWAL"
            ],
            TargetStatus.DONE.value: settings.DECISION["ANSWERS"]["DECISION"][
                "APPROVED"
            ],
        }

        form_api.save_answer(
            document=decision_work_item.document,
            question=Question.objects.get(
                slug=settings.DECISION["QUESTIONS"]["DECISION"]
            ),
            value=decision_mapping[dossier._meta.target_state],
            user=self._caluma_user,
        )

        if dossier._meta.target_state == TargetStatus.REJECTED.value:
            form_api.save_answer(
                document=decision_work_item.document,
                question=Question.objects.get(
                    pk=settings.DECISION["QUESTIONS"]["BAUABSCHLAG"]
                ),
                value=settings.DECISION["ANSWERS"]["BAUABSCHLAG"][
                    "OHNE_WIEDERHERSTELLUNG"
                ],
                user=self._caluma_user,
            )

    def _create_dossier_attachments(
        self, dossier: Dossier, instance: Instance
    ) -> List[Message]:
        messages = []
        if not dossier.attachments:  # pragma: no cover
            return messages

        for document in dossier.attachments:
            content = File(document.file_accessor)

            filename = re.sub(
                r"^{dossier_id}/".format(dossier_id=dossier.id),
                "",
                document.name.encode("utf-8", errors="ignore").decode(
                    "utf-8", errors="ignore"
                ),
            )

            mimimi = magic.Magic(mime=True, uncompress=True)
            mime_type = mimimi.from_buffer(content.file.read())
            content.file.seek(0)

            if not mime_type:  # pragma: no cover
                messages.append(
                    Message(
                        level=Severity.WARNING.value,
                        code=MessageCodes.MIME_TYPE_UNKNOWN,
                        detail=filename,
                    )
                )
                continue

            category = Category.objects.get(
                pk=settings.DOSSIER_IMPORT["ALEXANDRIA_CATEGORY"]
            )

            # TODO: implement reimport
            doc, _ = create_document_file(
                user=self._user.pk,
                group=self._group.service.pk,
                category=category,
                document_title=filename,
                file_name=filename,
                file_content=content,
                mime_type=mime_type,
                file_size=content.size,
                additional_document_attributes={
                    "metainfo": {"camac-instance-id": str(instance.pk)},
                },
            )

            messages.append(
                Message(
                    level=Severity.INFO.value,
                    code=MessageCodes.ATTACHMENT_CREATED.value,
                    detail=f"{doc.title.translate()} ({doc.get_latest_original().mime_type}) in section {category.name.translate()}",
                )
            )
        return messages
