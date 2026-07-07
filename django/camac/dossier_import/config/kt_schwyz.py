import weakref
from copy import deepcopy

from caluma.caluma_form.models import Form as CalumaForm
from caluma.caluma_workflow.api import cancel_work_item
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings

from camac.caluma.extensions.events.construction_monitoring import (
    can_perform_construction_monitoring,
)
from camac.dossier_import.dossier_classes import Dossier
from camac.dossier_import.validation import TargetStatus
from camac.dossier_import.writers import (
    BuildingAuthorityRowWriter,
    CalumaAnswerWriter,
    CamacNgAnswerWriter,
    CamacNgListAnswerWriter,
    CamacNgPersonListAnswerWriter,
    CamacNgPointsWriter,
    CamacNgStreetWriter,
    DossierWriter,
    WorkflowEntryDateWriter,
)
from camac.instance.domain_logic import CreateInstanceLogic
from camac.instance.models import Form, FormField, Instance, InstanceState
from camac.permissions.events import core as permissions_events
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
    coordinates = CamacNgPointsWriter(
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
        creation_data = {
            "instance_state": instance_state,
            "previous_instance_state": instance_state,
            "user": self._user,
            "group": self._group,
            "form": Form.objects.get(pk=settings.DOSSIER_IMPORT["FORM_ID"]),
        }
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

    def find_existing_instance(self, dossier, user):
        return Instance.objects.filter(
            fields__name="kommunale-gesuchsnummer",
            fields__value=dossier.id,
            group_id=self._group.pk,
        ).first()

    def link_instance_and_dossier(self, instance, dossier, user):
        """Make the instance retrievable by dossier_id.

        This config achieves that by calling `write_fields`. The
        method is still implemented to make it explicit and allow
        for better testing.
        :param user:
        """
        self.cantonal_id.owner = weakref.proxy(self)
        self.cantonal_id.write(instance, dossier.id)

    def get_workflow_skip_path(self, instance: Instance, dossier: Dossier) -> list[str]:
        """Return the skip path per target state.

        A written-off dossier depreciates the case right after submission
        instead of going through the decision. Construction monitoring is only
        initialized for a `DONE` dossier when the instance is eligible for it.
        """
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

        return {
            TargetStatus.SUBMITTED.value: SUBMITTED,
            TargetStatus.APPROVED.value: APPROVED,
            TargetStatus.DONE.value: DONE,
            TargetStatus.WRITTEN_OFF.value: WRITTEN_OFF,
        }[dossier._meta.target_state]

    def get_pre_complete_config(self, dossier: Dossier) -> dict:
        """Tweak the `PRE_COMPLETE` side effects for the import.

        The `depreciate-case` side effect is only kept for written-off dossiers,
        and the `publication` work item is additionally cancelled when the
        `make-decision` task is completed.
        """
        # deepcopy to not mutate any global settings
        config = deepcopy(super().get_pre_complete_config(dossier))

        if dossier._meta.target_state != TargetStatus.WRITTEN_OFF.value:
            config.pop("depreciate-case", None)
        if config.get("make-decision"):
            config["make-decision"]["cancel"].append("publication")

        return config

    def after_skip_work_item(
        self, work_item: WorkItem, instance: Instance, dossier: Dossier
    ):
        """Cancel the reject form once the submit work item has been skipped.

        Imported dossiers can't be rejected as there is no applicant involved
        that could react on it.
        """
        if work_item.task_id == "submit":
            reject_form = work_item.case.work_items.filter(
                task_id="reject-form", status=WorkItem.STATUS_READY
            ).first()
            if reject_form:
                cancel_work_item(
                    reject_form,
                    user=self._caluma_user,
                    context=self.get_skip_context(reject_form),
                )

        # SZ decides in the `make-decision` task instead of the regular
        # `decision` task, so the base class doesn't trigger this event for us.
        # This can be removed once SZ uses the regular decision form.
        if work_item.task_id == "make-decision":
            permissions_events.Trigger.decision_decreed(None, instance)

        super().after_skip_work_item(work_item, instance, dossier)
