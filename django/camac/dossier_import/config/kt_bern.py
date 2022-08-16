from typing import List

from caluma.caluma_form import api as form_api
from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Form as CalumaForm, Question
from caluma.caluma_form.validators import CustomValidationError
from caluma.caluma_user.models import BaseUser
from caluma.caluma_workflow import api as workflow_api
from caluma.caluma_workflow.api import skip_work_item
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from camac.caluma.extensions.events.general import get_caluma_setting
from camac.constants.kt_bern import (
    DECISION_TYPE_UNKNOWN,
    DECISIONS_BEWILLIGT,
    DECISIONS_POSITIVE,
)
from camac.core.models import InstanceService
from camac.dossier_import.dossier_classes import Dossier
from camac.dossier_import.messages import (
    DOSSIER_IMPORT_STATUS_ERROR,
    DOSSIER_IMPORT_STATUS_SUCCESS,
    DOSSIER_IMPORT_STATUS_WARNING,
    DossierSummary,
    Message,
    MessageCodes,
    get_message_max_level,
)
from camac.dossier_import.writers import (
    CalumaAnswerWriter,
    CalumaListAnswerWriter,
    CalumaPlotDataWriter,
    CaseMetaWriter,
    DossierWriter,
    EbauNumberWriter,
)
from camac.instance.domain_logic import SUBMIT_DATE_FORMAT, CreateInstanceLogic
from camac.instance.models import Form, Instance, InstanceState
from camac.instance.utils import set_construction_control
from camac.tags.models import Tags
from camac.user.models import Group, Location, User

APPLICANT_MAPPING = {
    "company": "name-juristische-person-gesuchstellerin",
    "last_name": "name-gesuchstellerin",
    "first_name": "vorname-gesuchstellerin",
    "street": "strasse-gesuchstellerin",
    "street_number": "nummer-gesuchstellerin",
    "zip": "plz-gesuchstellerin",
    "town": "ort-gesuchstellerin",
    "phone": "telefon-oder-mobile-gesuchstellerin",
    "email": "e-mail-gesuchstellerin",
}

LANDOWNER_MAPPING = {
    "company": "name-juristische-person-grundeigentuemerin",
    "last_name": "name-grundeigentuemerin",
    "first_name": "vorname-grundeigentuemerin",
    "street": "strasse-grundeigentuemerin",
    "street_number": "nummer-grundeigentuemerin",
    "zip": "plz-grundeigentuemerin",
    "town": "ort-grundeigentuemerin",
    "phone": "telefon-oder-mobile-grundeigentuemerin",
    "email": "e-mail-grundeigentuemerin",
}

PROJECTAUTHOR_MAPPING = {
    "company": "name-juristische-person-projektverfasserin",
    "last_name": "name-projektverfasserin",
    "first_name": "vorname-projektverfasserin",
    "street": "strasse-projektverfasserin",
    "street_number": "nummer-projektverfasserin",
    "zip": "plz-projektverfasserin",
    "town": "ort-projektverfasserin",
    "phone": "telefon-oder-mobile-projektverfasserin",
    "email": "e-mail-projektverfasserin",
}

PLOT_DATA_MAPPING = {
    "plot_number": "parzellennummer",
    "egrid_number": "e-grid-nr",
    "coord_east": "lagekoordinaten-ost",
    "coord_north": "lagekoordinaten-nord",
}


LOG_LEVEL_DEBUG = 0
LOG_LEVEL_INFO = 1
LOG_LEVEL_WARNING = 2
LOG_LEVEL_ERROR = 3


class ConfigurationError(Exception):
    pass


class KtBernDossierWriter(DossierWriter):
    """
    Dossier writer for importing dossiers from a ZIP archive.

    This writer assumes that the ZIP archive contains the following structure:

    - dossiers.xlsx containing metadata as well as form data (one line per dossier)
    - for each dossier: optionally a directory (named after the first column in dossier.xlsx)
      containing the documents to be attached to the dossier.
    """

    id: str = CalumaAnswerWriter(target="kommunale-gesuchsnummer")
    proposal = CalumaAnswerWriter(target="beschreibung-bauvorhaben")
    cantonal_id = EbauNumberWriter(target="ebau-number")
    plot_data = CalumaPlotDataWriter(
        target="parzelle", column_mapping=PLOT_DATA_MAPPING
    )
    usage = CalumaAnswerWriter(target="nutzungszone")
    application_type = CalumaAnswerWriter(target="geschaeftstyp-import")
    submit_date = CaseMetaWriter(target="submit-date", formatter="datetime-to-string")
    decision_date = CalumaAnswerWriter(
        target="decision-date", value_key="date", task="decision"
    )
    publication_date = CalumaAnswerWriter(target="datum-publikation", value_key="date")
    construction_start_date = CalumaAnswerWriter(
        target="datum-baubeginn", value_key="date"
    )
    profile_approval_date = CalumaAnswerWriter(
        target="datum-schnurgeruestabnahme", value_key="date"
    )
    final_approval_date = CalumaAnswerWriter(
        target="datum-schlussabnahme", value_key="date"
    )
    completion_date = CalumaAnswerWriter(target="bauende", value_key="date")
    link = CalumaAnswerWriter(target="link")
    custom_1 = CalumaAnswerWriter(target="freies-textfeld-1")
    custom_2 = CalumaAnswerWriter(target="freies-textfeld-2")
    street = CalumaAnswerWriter(target="strasse-flurname")
    street_number = CalumaAnswerWriter(target="nr")
    city = CalumaAnswerWriter(target="ort-grundstueck")
    applicant = CalumaListAnswerWriter(
        target="personalien-gesuchstellerin", column_mapping=APPLICANT_MAPPING
    )
    landowner = CalumaListAnswerWriter(
        target="personalien-grundeigentumerin", column_mapping=LANDOWNER_MAPPING
    )
    project_author = CalumaListAnswerWriter(
        target="personalien-projektverfasserin", column_mapping=PROJECTAUTHOR_MAPPING
    )
    is_paper = CalumaAnswerWriter(
        target="is-paper", value="is-paper-no"
    )  # static answer

    def __init__(
        self,
        user_id,
        group_id: int,
        location_id: int,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._user = user_id and User.objects.get(pk=user_id)
        self._group = Group.objects.get(pk=group_id)
        self._location = location_id and Location.objects.get(pk=location_id)

    def create_instance(self, dossier: Dossier) -> Instance:
        """Create a Camac NG Instance with a case.

        camac.instance.domain_logic.CreateInstanceLogic should be able to do the job and
        spit out a reasonably generic starting point.
        """
        instance_state_id = self._import_settings["INSTANCE_STATE_MAPPING"].get(
            dossier._meta.target_state
        )
        instance_state = instance_state_id and InstanceState.objects.get(
            pk=instance_state_id
        )
        creation_data = dict(
            instance_state=instance_state,
            previous_instance_state=instance_state,
            user=self._user,
            group=self._group,
            form=Form.objects.get(pk=self._import_settings["FORM_ID"]),
        )

        workflow_slug = {
            "BUILDINGPERMIT": "building-permit",
            "PRELIMINARY": "preliminary-clarification",
        }

        instance = CreateInstanceLogic.create(
            creation_data,
            caluma_user=BaseUser(username=self._user.username, group=self._group.pk),
            camac_user=self._user,
            group=self._group,
            caluma_form=CalumaForm.objects.get(
                pk=settings.APPLICATION["DOSSIER_IMPORT"]["CALUMA_FORM"]
            ),
            start_caluma=True,
            workflow_slug=workflow_slug[dossier._meta.workflow],
        )

        InstanceService.objects.create(
            instance=instance,
            service_id=self._group.service_id,
            active=1,
            activation_date=None,
        )
        meta = {
            "submit-date": dossier.submit_date.strftime(SUBMIT_DATE_FORMAT),
        }

        instance.case.meta.update(meta)
        instance.case.save()

        return instance

    @transaction.atomic
    def import_dossier(
        self, dossier: Dossier, import_session_id: str
    ) -> DossierSummary:
        dossier_summary = DossierSummary(
            dossier_id=dossier.id, status=DOSSIER_IMPORT_STATUS_SUCCESS, details=[]
        )

        # copy messages from loader to summary
        dossier_summary.details += dossier._meta.errors

        if dossier._meta.missing:
            dossier_summary.details.append(
                Message(
                    level=LOG_LEVEL_ERROR,
                    code=MessageCodes.MISSING_REQUIRED_VALUE_ERROR.value,
                    detail=f"missing values in required fields: {dossier._meta.missing}",
                )
            )
            dossier_summary.status = DOSSIER_IMPORT_STATUS_ERROR
            return dossier_summary

        tag = Tags.objects.filter(name=dossier.id, service=self._group.service).first()
        if tag:
            dossier_summary.details.append(
                Message(
                    level=LOG_LEVEL_WARNING,
                    code=MessageCodes.DUPLICATE_DOSSIER.value,
                    detail=f"Dossier with ID {dossier.id} already exists.",
                )
            )
            dossier_summary.status = DOSSIER_IMPORT_STATUS_ERROR
            return dossier_summary
        instance = self.create_instance(dossier)
        Tags.objects.create(
            name=dossier.id, service=self._group.service, instance=instance
        )
        instance.case.meta["import-id"] = import_session_id
        instance.case.save()
        dossier_summary.instance_id = instance.pk
        dossier_summary.details.append(
            Message(
                level=LOG_LEVEL_DEBUG,
                code=MessageCodes.INSTANCE_CREATED.value,
                detail=f"Instance created with ID:  {instance.pk}",
            )
        )
        q_municipality = Question.objects.get(slug="gemeinde")
        save_answer(
            document=instance.case.document,
            question=q_municipality,
            value=str(self._group.service_id),
            user=BaseUser(username=self._user.username, group=self._group.pk),
        )

        dossier_summary.details += self._create_dossier_attachments(dossier, instance)

        workflow_message = self._set_workflow_state(
            instance, dossier._meta.target_state, dossier
        )
        instance.history.all().delete()

        self.write_fields(instance, dossier)
        dossier_summary.details.append(
            Message(
                level=LOG_LEVEL_DEBUG,
                code=MessageCodes.FORM_DATA_WRITTEN.value,
                detail="Form data written.",
            )
        )

        dossier_summary.details.append(
            Message(
                level=get_message_max_level(workflow_message),
                code=MessageCodes.SET_WORKFLOW_STATE.value,
                detail=workflow_message,
            )
        )
        if (
            get_message_max_level(dossier_summary.details) == LOG_LEVEL_ERROR
        ):  # pragma: no cover
            dossier_summary.status = DOSSIER_IMPORT_STATUS_ERROR
        if get_message_max_level(dossier_summary.details) == LOG_LEVEL_WARNING:
            dossier_summary.status = DOSSIER_IMPORT_STATUS_WARNING  # pragma: no cover

        return dossier_summary

    def _set_workflow_state(  # noqa: C901
        self,
        instance: Instance,
        target_state,
        dossier,
        workflow_type: str = "BUILDINGPERMIT",
    ) -> List[Message]:
        """Advance instance's case through defined workflow sequence to target state.

        In order to advance to a specified worklow state after every flow all tasks need to be
        in a status other than ready so that the relevant work_item can be completed.

        Therefore every target_state needs to be informed on the sibling work-items and how to handle
        them before completion and progression to the next task in line.

        This is configured in the following:

        <TARGETSTATE> = [
            (<task_to_complete>: [<task_to_sikp>, ... ]),
            ...
        ]

        If required this could be extended with the option to handle sibling tasks differently on each stage, such
         as cancelling them instead of skipping.
        """
        messages = []

        # configure workflow state advance path and strategies (skip | cancel)
        SUBMITTED = ["submit"]
        APPROVED = SUBMITTED + ["ebau-number", "distribution", "decision"]
        DONE = APPROVED + ["sb1", "sb2", "complete"]

        if workflow_type == "PRELIMINARY":
            DONE = APPROVED

        path_to_state = {"SUBMITTED": SUBMITTED, "APPROVED": APPROVED, "DONE": DONE}

        default_context = {"no-notification": True, "no-history": True}

        caluma_user = BaseUser(username=self._user.username, group=self._group.pk)
        caluma_user.camac_group = self._group.pk

        # In order for a work item to be completed no sibling work items can be
        # in state ready. They have to be dealt with in advance.
        for task_id in path_to_state[target_state]:
            try:
                work_item = instance.case.work_items.get(task_id=task_id)
            except ObjectDoesNotExist as e:  # pragma: no cover
                messages.append(
                    Message(
                        level=LOG_LEVEL_WARNING,
                        code=MessageCodes.WORKFLOW_SKIP_ITEM_FAILED.value,
                        detail=f"Skip work item with task_id {task_id} failed with {ConfigurationError(e)}.",
                    )
                )
                continue

            if task_id == "decision":
                self.write_decision_form(work_item, dossier, workflow_type)

            config = get_caluma_setting("PRE_COMPLETE") and get_caluma_setting(
                "PRE_COMPLETE"
            ).get(work_item.task_id)
            if config:
                for action_name, tasks in config.items():
                    action = getattr(workflow_api, f"{action_name}_work_item")

                    for item in work_item.case.work_items.filter(
                        task_id__in=tasks, status=WorkItem.STATUS_READY
                    ):
                        action(item, caluma_user)
            skip_work_item(work_item, user=caluma_user, context=default_context)
            if task_id == "decision":
                set_construction_control(instance)
            if target_state == "SUBMITTED":
                if instance.case.meta.get("ebau-number"):
                    work_item = instance.case.work_items.get(task_id="ebau-number")
                    skip_work_item(work_item, user=caluma_user, context=default_context)
                    self.write_ebau_number_form(instance, work_item, dossier)
                    instance.instance_state = InstanceState.objects.get(
                        name="circulation_init"
                    )
                else:
                    instance.instance_state = InstanceState.objects.get(name="subm")
                instance.save()
        messages.append(  # pragma: no cover
            Message(
                level=LOG_LEVEL_DEBUG,
                code=MessageCodes.SET_WORKFLOW_STATE.value,
                detail=f"Workflow state set to {target_state}.",
            )
        )
        return messages

    def write_ebau_number_form(self, instance, ebau_number_work_item, dossier):
        document = ebau_number_work_item.document
        ebau_number_slug = "ebau-number-existing"
        question = Question.objects.get(slug=ebau_number_slug)
        value = instance.case.meta.get("ebau-number")
        try:
            save_answer(
                question=question,
                document=document,
                value=value,
                user=BaseUser(username=self._user.username, group=self._group.pk),
            )
        except CustomValidationError:  # pragma: no cover
            dossier._meta.errors.append(
                Message(
                    level=LOG_LEVEL_WARNING,
                    code=MessageCodes.FIELD_VALIDATION_ERROR.value,
                    detail=f"Failed to write {value} to {ebau_number_slug} for dossier {instance}",
                )
            )
            return
        exists_slug = "ebau-number-has-existing"
        question_exists = Question.objects.get(slug=exists_slug)
        try:
            save_answer(
                question=question_exists,
                document=document,
                value=f"{exists_slug}-yes",
                user=BaseUser(username=self._user.username, group=self._group.pk),
            )
        except CustomValidationError:  # pragma: no cover
            dossier._meta.errors.append(
                Message(
                    level=LOG_LEVEL_WARNING,
                    code=MessageCodes.FIELD_VALIDATION_ERROR.value,
                    detail=f"Failed to write '{exists_slug}-yes' to {exists_slug} for dossier {instance}",
                )
            )
            return

    def write_decision_form(self, decision_work_item, dossier, workflow_type):
        form_api.save_answer(
            document=decision_work_item.document,
            question=Question.objects.get(slug="decision-decision-assessment"),
            value=DECISIONS_BEWILLIGT
            if workflow_type == "BUILDINGPERMIT"
            else DECISIONS_POSITIVE,
        )
        if workflow_type == "BUILDINGPERMIT":
            form_api.save_answer(
                document=decision_work_item.document,
                question=Question.objects.get(pk="decision-approval-type"),
                value=DECISION_TYPE_UNKNOWN,
            )
