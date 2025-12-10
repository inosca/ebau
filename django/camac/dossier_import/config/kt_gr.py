import json
from typing import List

from caluma.caluma_form import api as form_api
from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Form as CalumaForm, Question
from caluma.caluma_workflow import api as workflow_api
from caluma.caluma_workflow.api import skip_work_item
from caluma.caluma_workflow.models import Case, WorkItem
from django.conf import settings

from camac.caluma.extensions.events.general import get_caluma_setting
from camac.core.models import InstanceService
from camac.core.utils import generate_sort_key
from camac.dossier_import.dossier_classes import Dossier
from camac.dossier_import.loaders import safe_join
from camac.dossier_import.messages import (
    Message,
    MessageCodes,
    Severity,
)
from camac.dossier_import.utils import mark_work_items_as_imported
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
from camac.permissions import events as permissions_events
from camac.tags.models import Keyword

PERSON_VALUE_MAPPING = {
    "is_juristic_person": {
        True: "juristische-person-gesuchstellerin-ja",
        False: "juristische-person-gesuchstellerin-nein",
    }
}

PERSON_MAPPING = {
    "is_juristic_person": "juristische-person-gesuchstellerin",
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

PLOT_DATA_MAPPING = {
    "plot_number": "parzellennummer",
    "egrid_number": "e-grid-nr",
    "coord_east": "lagekoordinaten-ost",
    "coord_north": "lagekoordinaten-nord",
}


class CalumaCombinedStreetAndNumberWriter(CalumaAnswerWriter):
    """Combine street and street number into one field."""

    def __init__(
        self,
        fields: list[str] = [],
        *args,
        **kwargs,
    ):
        self.fields = fields
        super().__init__(*args, **kwargs)

    def write(self, instance, values):
        dossier = self.context.get("dossier")
        if dossier.street == settings.DOSSIER_IMPORT["DELETE_KEYWORD"]:
            combined_value = dossier.street
        else:
            combined_value = safe_join(
                (
                    getattr(dossier, field, "")
                    for field in self.fields
                    if getattr(dossier, field, None)
                ),
                separator=" ",
            )

        super().write(instance, combined_value)


class KtGraubundenDossierWriter(DossierWriter):
    id = CalumaAnswerWriter(
        target="kommunale-gesuchsnummer", formatter="to-string", protected=True
    )
    proposal = CalumaAnswerWriter(target="beschreibung-bauvorhaben", protected=True)
    cantonal_id = CalumaAnswerWriter(
        target="kantonale-gesuchsnummer", formatter="to-string"
    )
    plot_data = CalumaPlotDataWriter(
        target="parzelle", column_mapping=PLOT_DATA_MAPPING
    )
    usage = CalumaAnswerWriter(target="nutzungsplanung-grundnutzung")
    application_type = CalumaAnswerWriter(target="geschaeftstyp")
    submit_date = CaseMetaWriter(
        target="submit-date", formatter="datetime-to-string", protected=True
    )
    decision_date = CalumaAnswerWriter(target="decision-date", task="decision")
    publication_date = CalumaAnswerWriter(target="datum-publikation")
    construction_start_date = CalumaAnswerWriter(target="datum-baubeginn")
    profile_approval_date = CalumaAnswerWriter(target="datum-schnurgeruestabnahme")
    final_approval_date = CalumaAnswerWriter(target="datum-schlussabnahme")
    completion_date = CalumaAnswerWriter(target="bauende")
    link = CalumaAnswerWriter(target="link")
    custom_1 = CalumaAnswerWriter(target="freies-textfeld-1")
    custom_2 = CalumaAnswerWriter(target="freies-textfeld-2")
    street = CalumaCombinedStreetAndNumberWriter(
        target="street-and-housenumber",
        fields=["street", "street_number"],
    )
    city = CalumaAnswerWriter(target="ort-grundstueck")
    applicant = CalumaListAnswerWriter(
        target="personalien-gesuchstellerin",
        column_mapping=PERSON_MAPPING,
        value_mapping=PERSON_VALUE_MAPPING,
    )
    landowner = CalumaListAnswerWriter(
        target="personalien-grundeigentumerin",
        column_mapping=PERSON_MAPPING,
        value_mapping=PERSON_VALUE_MAPPING,
    )
    project_author = CalumaListAnswerWriter(
        target="personalien-projektverfasserin",
        column_mapping=PERSON_MAPPING,
        value_mapping=PERSON_VALUE_MAPPING,
    )

    def create_instance(self, dossier: Dossier) -> Instance:
        instance_state = InstanceState.objects.get(
            name=settings.DOSSIER_IMPORT["INSTANCE_STATE_MAPPING"].get(
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

        InstanceService.objects.create(
            instance=instance,
            service_id=self._group.service_id,
            active=1,
            activation_date=None,
        )

        dossier_number = CreateInstanceLogic.generate_identifier(
            instance, dossier.submit_date.year
        )

        instance.case.meta.update(
            {
                "dossier-number": dossier_number,
                "dossier-number-sort": generate_sort_key(dossier_number),
            }
        )
        instance.case.save()
        permissions_events.Trigger.instance_submitted(None, instance)
        return instance

    def get_existing_dossier_ids(self, dossier_ids):
        return list(
            Keyword.objects.filter(
                name__in=dossier_ids,
                service=self._group.service,
                instances__isnull=False,
            ).values_list("name", flat=True)
        )

    def find_existing_instance(self, dossier, user):
        keyword = Keyword.objects.filter(
            name=dossier.id, service=self._group.service
        ).first()

        return keyword.instances.first() if keyword else None

    def link_instance_and_dossier(self, instance, dossier, user):
        keyword = Keyword.objects.filter(
            name=dossier.id, service=self._group.service
        ).first()

        if keyword:  # pragma: no cover
            # This only happens after an import was undone
            keyword.instances.add(instance)
        else:
            instance.keywords.create(name=dossier.id, service=self._group.service)

    def _post_create_instance(self, instance: Instance, dossier: Dossier):
        save_answer(
            document=instance.case.document,
            question=Question.objects.get(slug="gemeinde"),
            value=str(self._group.service_id),
            user=self._caluma_user,
        )

    def _post_write_fields(self, instance, dossier):
        self._write_triage_fields(instance)
        self._write_gis_coordinates(instance, dossier)
        work_items = instance.case.work_items.all()
        mark_work_items_as_imported(work_items)

    def _write_triage_fields(self, instance: Instance):
        """Write triage answers for personal data.

        The table questions for landowner, and project author are only displayed if the multi-select contains these values.
        """

        extra_values = []
        for table_question in [
            "personalien-grundeigentumerin",
            "personalien-projektverfasserin",
        ]:
            table_answer = instance.case.document.answers.filter(
                question_id=table_question
            ).first()
            has_rows = table_answer.documents.exists() if table_answer else False
            if has_rows:
                if table_question == "personalien-grundeigentumerin":
                    extra_values.append("weitere-personen-grundeigentumerin")
                elif table_question == "personalien-projektverfasserin":
                    extra_values.append("weitere-personen-projektverfasserin")

        form_api.save_answer(
            document=instance.case.document,
            question=Question.objects.get(pk="weitere-personen"),
            value=extra_values,
            user=self._caluma_user,
        )

    def _write_gis_coordinates(self, instance: Instance, dossier: Dossier):
        coordinates = getattr(dossier, "coordinates", [])
        form_api.save_answer(
            document=instance.case.document,
            question=Question.objects.get(slug="gis-map"),
            value=json.dumps(
                {
                    "markers": [{"x": coord.e, "y": coord.n} for coord in coordinates],
                    "geometry": "POINT",
                }
            ),
            user=self._caluma_user,
        )

    def _set_workflow_state(self, instance: Instance, dossier) -> List[Message]:
        messages = []
        target_state = dossier._meta.target_state

        SUBMITTED = ["submit"]
        DECIDED = SUBMITTED + [
            "formal-exam",
            "distribution",
            "decision",
        ]
        REJECTED = DECIDED + ["create-manual-workitems"]
        DONE = (
            DECIDED
            + ["create-manual-workitems"]
            + (
                ["init-construction-monitoring"]
                if settings.CONSTRUCTION_MONITORING["ENABLED"]
                else ["construction-acceptance"]
            )
        )

        path_to_state = {
            TargetStatus.SUBMITTED.value: SUBMITTED,
            TargetStatus.APPROVED.value: DECIDED,
            TargetStatus.REJECTED.value: REJECTED,
            TargetStatus.DONE.value: DONE,
        }

        default_context = {"no-notification": True, "no-history": True, "skip": True}

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
                        detail=(
                            f"Skip work item with task_id {task_id} failed with "
                            f"{DossierWriter.ConfigurationError(e)}."
                        ),
                    )
                )
                continue

            if task_id == "decision":
                self.write_decision_form(work_item, dossier)
                permissions_events.Trigger.decision_decreed(None, instance)

            if config := get_caluma_setting("PRE_COMPLETE") and get_caluma_setting(
                "PRE_COMPLETE"
            ).get(work_item.task_id):
                for action_name, tasks in config.items():
                    action = getattr(workflow_api, f"{action_name}_work_item")

                    for item in work_item.case.work_items.filter(
                        task_id__in=tasks, status=WorkItem.STATUS_READY
                    ):
                        action(item, self._caluma_user)

            if work_item.case.status != Case.STATUS_RUNNING:  # pragma: no cover
                continue

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
