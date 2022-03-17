from copy import deepcopy
from typing import List

from caluma.caluma_form.models import Form as CalumaForm
from caluma.caluma_user.models import BaseUser
from caluma.caluma_workflow import api as workflow_api
from caluma.caluma_workflow.api import cancel_work_item, skip_work_item
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from camac.caluma.extensions.events.general import get_caluma_setting
from camac.dossier_import.dossier_classes import Dossier
from camac.dossier_import.messages import (
    DOSSIER_IMPORT_STATUS_ERROR,
    DOSSIER_IMPORT_STATUS_SUCCESS,
    DOSSIER_IMPORT_STATUS_WARNING,
    LOG_LEVEL_DEBUG,
    LOG_LEVEL_ERROR,
    LOG_LEVEL_WARNING,
    DossierSummary,
    Message,
    MessageCodes,
    get_message_max_level,
)
from camac.dossier_import.writers import (
    BuildingAuthorityRowWriter,
    CalumaAnswerWriter,
    CamacNgAnswerWriter,
    CamacNgListAnswerWriter,
    CamacNgPersonListAnswerWriter,
    CamacNgStreetWriter,
    DossierWriter,
    WorkflowEntryDateWriter,
)
from camac.instance.domain_logic import CreateInstanceLogic
from camac.instance.models import Form, Instance, InstanceState
from camac.user.models import Group, Location, User

PERSON_MAPPING = {
    "company": "firma",
    "last_name": "name",
    "first_name": "vorname",
    "street": "strasse",
    "zip": "plz",
    "town": "ort",
    "phone": "tel",
    "email": "email",
}

PARCEL_MAPPING = {"egrid": "egrid", "number": "number", "municipality": "municipality"}

COORDINATES_MAPPING = {"e": "lat", "n": "lng"}


class ConfigurationError(Exception):
    pass


class KtSchwyzDossierWriter(DossierWriter):
    """
    Dossier writer for importing dossiers from a ZIP archive.

    This writer assumes that the ZIP archive contains the following structure:

    - dossiers.xlsx containing metadata as well as form data (one line per dossier)
    - for each dossier: optionally a directory (named after the first column in dossier.xlsx)
      containing the documents to be attached to the dossier.
    """

    id: str = CamacNgAnswerWriter(target="kommunale-gesuchsnummer")
    proposal = CamacNgAnswerWriter(target="bezeichnung")
    cantonal_id = CamacNgAnswerWriter(target="kantonale-gesuchsnummer")
    plot_data = CamacNgListAnswerWriter(
        target="parzellen", column_mapping=PARCEL_MAPPING
    )
    coordinates = CamacNgListAnswerWriter(
        target="punkte", column_mapping=COORDINATES_MAPPING
    )
    usage = CamacNgAnswerWriter(target="betroffene-nutzungszonen")
    application_type = CamacNgAnswerWriter(target="verfahrensart-migriertes-dossier")
    submit_date = WorkflowEntryDateWriter(target=10, name="einreichedatum")
    publication_date = WorkflowEntryDateWriter(name="publikationsdatum", target=15)

    construction_start_date = BuildingAuthorityRowWriter(
        name="datum-baubeginn",
        target="baukontrolle-realisierung-baubeginn",
        value_key="date",
    )
    profile_approval_date = BuildingAuthorityRowWriter(
        name="datum-schnurgeruestabnahme",
        target="baukontrolle-realisierung-schnurgeruestabnahme",
        value_key="date",
    )
    decision_date = CalumaAnswerWriter(
        name="tb-datum",
        target="bewilligungsverfahren-gr-sitzung-bewilligungsdatum",
        value_key="date",
        task="building-authority",
    )
    final_approval_date = BuildingAuthorityRowWriter(
        name="datum-schlussabnahme",
        target="baukontrolle-realisierung-schlussabnahme",
        value_key="date",
    )
    completion_date = BuildingAuthorityRowWriter(
        name="datum-bauende",
        target="baukontrolle-realisierung-bauende",
        value_key="date",
    )
    link = CamacNgAnswerWriter(target="link")
    custom_1 = CamacNgAnswerWriter(target="freies-textfeld-1")
    custom_2 = CamacNgAnswerWriter(target="freies-textfeld-2")
    street = CamacNgStreetWriter(
        target="ortsbezeichnung-des-vorhabens",
    )
    city = CamacNgAnswerWriter(target="standort-ort")
    applicant = CamacNgPersonListAnswerWriter(
        target="bauherrschaft", column_mapping=PERSON_MAPPING
    )
    landowner = CamacNgPersonListAnswerWriter(
        target="grundeigentumerschaft", column_mapping=PERSON_MAPPING
    )
    project_author = CamacNgPersonListAnswerWriter(
        target="projektverfasser-planer", column_mapping=PERSON_MAPPING
    )

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
        self._location = Location.objects.get(pk=location_id)

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
        instance = CreateInstanceLogic.create(
            creation_data,
            caluma_user=BaseUser(),
            camac_user=self._user,
            group=self._group,
            caluma_form=CalumaForm.objects.get(
                pk=settings.APPLICATION["DOSSIER_IMPORT"]["CALUMA_FORM"]
            ),
            start_caluma=False,
        )
        instance.location = self._location
        CreateInstanceLogic.update_instance_location(instance)
        instance.identifier = CreateInstanceLogic.generate_identifier(
            instance, prefix="IM", seq_zero_padding=4, year=dossier.submit_date.year
        )
        instance.save()
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
                    detail=dossier._meta.missing,
                )
            )
            dossier_summary.status = DOSSIER_IMPORT_STATUS_ERROR
            return dossier_summary
        if not self._import_settings["INSTANCE_STATE_MAPPING"].get(
            dossier._meta.target_state
        ):  # pragma: no cover
            dossier_summary.details.append(
                Message(
                    level=LOG_LEVEL_ERROR,
                    code=MessageCodes.STATUS_CHOICE_VALIDATION_ERROR.value,
                    detail=dossier._meta.target_state,
                )
            )
        if Instance.objects.filter(
            fields__name="kommunale-gesuchsnummer",
            fields__value=dossier.id,
            group_id=self._group.pk,
        ).first():
            dossier_summary.details.append(
                Message(
                    level=LOG_LEVEL_WARNING,
                    code=MessageCodes.DUPLICATE_DOSSIER.value,
                    detail=None,
                )
            )
            dossier_summary.status = DOSSIER_IMPORT_STATUS_ERROR
            return dossier_summary
        instance = self.create_instance(dossier)
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
        workflow_message = self._set_workflow_state(
            instance, dossier._meta.target_state
        )
        dossier_summary.details.append(
            Message(
                level=get_message_max_level(workflow_message),
                code=MessageCodes.SET_WORKFLOW_STATE.value,
                detail=workflow_message,
            )
        )
        self.write_fields(instance, dossier)

        dossier_summary.details.append(
            Message(
                level=LOG_LEVEL_DEBUG,
                code=MessageCodes.FORM_DATA_WRITTEN.value,
                detail="Form data written.",
            )
        )
        dossier_summary.details += self._create_dossier_attachments(dossier, instance)
        instance.history.all().delete()
        if (
            get_message_max_level(dossier_summary.details) == LOG_LEVEL_ERROR
        ):  # pragma: no cover
            dossier_summary.status = DOSSIER_IMPORT_STATUS_ERROR
        if (
            get_message_max_level(dossier_summary.details) == LOG_LEVEL_WARNING
        ):  # pragma: no cover
            dossier_summary.status = DOSSIER_IMPORT_STATUS_WARNING

        return dossier_summary

    def _set_workflow_state(self, instance: Instance, target_state) -> List[Message]:
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

        # configure workflow state advance path and strategies
        SUBMITTED = ["submit"]
        APPROVED = SUBMITTED + [
            "complete-check",
            "skip-circulation",
            "make-decision",
        ]
        DONE = APPROVED + ["archive-instance"]

        path_to_state = {"SUBMITTED": SUBMITTED, "APPROVED": APPROVED, "DONE": DONE}

        default_context = {"no-notification": True, "no-history": True}

        camac_user = self._user

        caluma_user = BaseUser(username=camac_user.name, group=self._group.pk)
        caluma_user.camac_group = self._group.pk

        # In order for a work item to be completed no sibling work items can be
        # in state ready. They have to be dealt with in advance.
        for task_id in path_to_state[target_state]:
            try:
                work_item = instance.case.work_items.get(task_id=task_id)
            except ObjectDoesNotExist as e:
                messages.append(
                    Message(
                        level=LOG_LEVEL_WARNING,
                        code=MessageCodes.WORKFLOW_SKIP_ITEM_FAILED.value,
                        detail=f"Skip work item with task_id {task_id} failed with {ConfigurationError(e)}.",
                    )
                )
                continue
            # overwrite side effects for import
            config = deepcopy(get_caluma_setting("PRE_COMPLETE"))
            # skip side effects in task `make-decision`
            config and config.pop("depreciate-case", None)
            if config.get("make-decision"):
                config["make-decision"]["cancel"].append("publication")
            config = config and config.get(work_item.task_id)
            if config:
                for action_name, tasks in config.items():
                    action = getattr(workflow_api, f"{action_name}_work_item")

                    for item in work_item.case.work_items.filter(
                        task_id__in=tasks, status=WorkItem.STATUS_READY
                    ):
                        action(item, caluma_user)
            skip_work_item(work_item, user=caluma_user, context=default_context)
            # post complete submit
            if task_id == "submit":
                item = work_item.case.work_items.filter(
                    task_id="reject-form", status=WorkItem.STATUS_READY
                ).first()
                item and cancel_work_item(
                    item, user=caluma_user, context=default_context
                )
        messages.append(
            Message(
                level=LOG_LEVEL_DEBUG,
                code=MessageCodes.SET_WORKFLOW_STATE.value,
                detail=f"Workflow state set to {target_state}.",
            )
        )
        return messages
