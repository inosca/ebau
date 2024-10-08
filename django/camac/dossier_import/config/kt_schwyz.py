import weakref
from copy import deepcopy
from typing import List

from caluma.caluma_form.models import Form as CalumaForm
from caluma.caluma_workflow import api as workflow_api
from caluma.caluma_workflow.api import cancel_work_item, skip_work_item
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings

from camac.caluma.extensions.events.construction_monitoring import (
    can_perform_construction_monitoring,
)
from camac.caluma.extensions.events.general import get_caluma_setting
from camac.dossier_import.dossier_classes import Dossier
from camac.dossier_import.messages import (
    Message,
    MessageCodes,
    Severity,
)
from camac.dossier_import.validation import TargetStatus
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
from camac.instance.models import Form, FormField, Instance, InstanceState
from camac.permissions import events as permissions_events
from camac.user.models import Location

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

    id = CamacNgAnswerWriter(target="kommunale-gesuchsnummer", protected=True)
    proposal = CamacNgAnswerWriter(target="bezeichnung", protected=True)
    cantonal_id = CamacNgAnswerWriter(target="kantonale-gesuchsnummer")
    plot_data = CamacNgListAnswerWriter(
        target="parzellen", column_mapping=PARCEL_MAPPING
    )
    coordinates = CamacNgListAnswerWriter(
        target="punkte", column_mapping=COORDINATES_MAPPING
    )
    usage = CamacNgAnswerWriter(target="betroffene-nutzungszonen")
    application_type = CamacNgAnswerWriter(target="verfahrensart-migriertes-dossier")
    submit_date = WorkflowEntryDateWriter(
        target=10, name="einreichedatum", protected=True
    )
    publication_date = WorkflowEntryDateWriter(name="publikationsdatum", target=15)

    construction_start_date = BuildingAuthorityRowWriter(
        name="datum-baubeginn",
        target="baukontrolle-realisierung-baubeginn",
    )
    profile_approval_date = BuildingAuthorityRowWriter(
        name="datum-schnurgeruestabnahme",
        target="baukontrolle-realisierung-schnurgeruestabnahme",
    )
    decision_date = CalumaAnswerWriter(
        name="tb-datum",
        target="bewilligungsverfahren-gr-sitzung-bewilligungsdatum",
        task="building-authority",
    )
    final_approval_date = BuildingAuthorityRowWriter(
        name="datum-schlussabnahme",
        target="baukontrolle-realisierung-schlussabnahme",
    )
    completion_date = BuildingAuthorityRowWriter(
        name="datum-bauende",
        target="baukontrolle-realisierung-bauende",
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
        location_id: int,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._location = Location.objects.get(pk=location_id)

    def create_instance(self, dossier: Dossier) -> Instance:
        """Create a Camac NG Instance with a case.

        camac.instance.domain_logic.CreateInstanceLogic should be able to do the job and
        spit out a reasonably generic starting point.
        """
        instance_state_id = settings.DOSSIER_IMPORT["INSTANCE_STATE_MAPPING"].get(
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
            start_caluma=False,
        )
        instance.location = self._location
        CreateInstanceLogic.update_instance_location(instance)
        instance.identifier = CreateInstanceLogic.generate_identifier(
            instance, prefix="IM", seq_zero_padding=4, year=dossier.submit_date.year
        )
        instance.save()
        permissions_events.Trigger.instance_submitted(None, instance)
        return instance

    def get_existing_dossier_ids(self, dossier_ids):
        return list(
            FormField.objects.filter(
                name="kommunale-gesuchsnummer",
                value__in=dossier_ids,
                instance__group_id=self._group.pk,
            ).values_list("value", flat=True)
        )

    def existing_dossier(self, dossier_id):
        return Instance.objects.filter(
            fields__name="kommunale-gesuchsnummer",
            fields__value=dossier_id,
            group_id=self._group.pk,
        ).first()

    def set_dossier_id(self, instance, dossier_id):
        """Make the instance retrievable by dossier_id.

        This config achieves that by calling `write_fields`. The
        method is still implemented to make it explicit and allow
        for better testing.
        """
        self.cantonal_id.owner = weakref.proxy(self)
        self.cantonal_id.write(instance, dossier_id)

    def _set_workflow_state(
        self, instance: Instance, dossier: Dossier
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

        target_state = dossier._meta.target_state

        # configure workflow state advance path and strategies
        SUBMITTED = ["submit"]
        APPROVED = SUBMITTED + [
            "complete-check",
            "distribution",
            "make-decision",
        ]
        DONE = (
            APPROVED
            + (
                ["init-construction-monitoring"]
                if can_perform_construction_monitoring(instance)
                else []
            )
            + [
                "complete-instance",
                "archive-instance",
            ]
        )
        WRITTEN_OFF = SUBMITTED + ["depreciate-case"]

        path_to_state = {
            TargetStatus.SUBMITTED.value: SUBMITTED,
            TargetStatus.APPROVED.value: APPROVED,
            TargetStatus.DONE.value: DONE,
            TargetStatus.WRITTEN_OFF.value: WRITTEN_OFF,
        }

        default_context = {"no-notification": True, "no-history": True, "skip": True}

        # In order for a work item to be completed no sibling work items can be
        # in state ready. They have to be dealt with in advance.
        for task_id in path_to_state[target_state]:
            try:
                work_item = instance.case.work_items.get(task_id=task_id)
            except WorkItem.DoesNotExist as e:
                messages.append(
                    Message(
                        level=Severity.ERROR.value,
                        code=MessageCodes.WORKFLOW_SKIP_ITEM_FAILED.value,
                        detail=(
                            f"Skip work item with task_id {task_id} "
                            f"failed with {ConfigurationError(e)}."
                        ),
                    )
                )
                continue
            # overwrite side effects for import
            config = deepcopy(get_caluma_setting("PRE_COMPLETE"))
            # skip side effects in task `make-decision`
            if config and target_state != TargetStatus.WRITTEN_OFF.value:
                config.pop("depreciate-case", None)
            if config.get("make-decision"):
                config["make-decision"]["cancel"] = config["make-decision"][
                    "cancel"
                ] + ["publication"]
                permissions_events.Trigger.decision_decreed(None, instance)
            config = config and config.get(work_item.task_id)
            if config:
                for action_name, tasks in config.items():
                    action = getattr(workflow_api, f"{action_name}_work_item")

                    for item in work_item.case.work_items.filter(
                        task_id__in=tasks, status=WorkItem.STATUS_READY
                    ):
                        action(item, self._caluma_user)
            skip_work_item(work_item, user=self._caluma_user, context=default_context)
            # post complete submit
            if task_id == "submit":
                item = work_item.case.work_items.filter(
                    task_id="reject-form", status=WorkItem.STATUS_READY
                ).first()
                item and cancel_work_item(
                    item, user=self._caluma_user, context=default_context
                )
        messages.append(
            Message(
                level=Severity.DEBUG.value,
                code=MessageCodes.SET_WORKFLOW_STATE.value,
                detail=f"Workflow state set to {target_state}.",
            )
        )
        return messages
