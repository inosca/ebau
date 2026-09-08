import json
import os
import re
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import (
    Question,
)
from caluma.caluma_user.models import BaseUser
from django.utils import timezone
from django.utils.translation import gettext as _

from camac.dossier_import.dossier_classes import Dossier
from camac.dossier_import.messages import (
    Message,
    MessageCodes,
    Severity,
)
from camac.dossier_import.utils import mark_work_items_as_imported
from camac.dossier_import.validation import TargetStatus
from camac.dossier_import.writers import (
    CalumaAnswerWriter,
    CalumaCombinedStreetAndNumberWriter,
    CalumaTableAnswerWriter,
    DossierWriter,
    FieldWriter,
    ResponsibleUserWriter,
    SubmitDateWriter,
)
from camac.instance.models import Instance, JournalEntry
from camac.tags.models import Keyword
from camac.user.models import Service

PERSON_VALUE_MAPPING = {
    "is_juristic_person": {
        True: "juristische-person-gesuchstellerin-ja",
        False: "juristische-person-gesuchstellerin-nein",
    }
}

PERSON_MAPPING = {
    "first_name": "vorname-gesuchstellerin",
    "last_name": "name-gesuchstellerin",
    "is_juristic_person": "juristische-person-gesuchstellerin",
    "company": "name-juristische-person-gesuchstellerin",
    "street": "strasse-gesuchstellerin",
    "street_number": "nummer-gesuchstellerin",
    "zip": "plz-gesuchstellerin",
    "town": "ort-gesuchstellerin",
    "phone": "telefon-oder-mobile-gesuchstellerin",
    "email": "e-mail-gesuchstellerin",
}

PLOT_DATA_MAPPING = {
    "number": "parzellennummer",
    "egrid": "e-grid-nr",
    "municipality": "gemeinde",
}


class KeywordWriter(FieldWriter):
    """A field writer that creates or associates a keyword with an instance.

    This writer handles the creation of new keywords or the association of existing
    keywords with an instance. Keywords are service-specific and are looked up or
    created within the scope of the instance's responsible service.

    If the keyword with the given value already exists for the service (only happens after an import was undone),
    it adds the instance to that keyword's instances. Otherwise, it creates a new keyword for the instance.
    """

    def __init__(self):
        super().__init__(target="")

    def write(self, instance, value):
        if not value:
            return

        service = instance.responsible_service()
        keyword = Keyword.objects.filter(name=value, service=service).first()

        if keyword:  # pragma: no cover
            keyword.instances.add(instance)
        else:
            instance.keywords.create(name=value, service=service)


@dataclass
class TextWithDate:
    text: str
    date: datetime = field(default_factory=timezone.now)


class JournalWriter(FieldWriter):
    def __init__(
        self,
        convert_entry: Callable[[Any], TextWithDate],
        visibility: str = "own_organization",
        service: Service | None = None,
        identify_by_text_only: bool = False,
    ):
        """Initialize journal writer for importing historical entries.

        Args:
            convert_entry: Function to convert input value to TextWithDate object.
                           If the dossier field value to be written is a list,
                           the convert function is called for each element of the list.
            visibility: Journal entry visibility setting, defaults to "own_organization"
            service: the service owning the journal entry, defaults to responsible_service of the instance
            identify_by_text_only: If True, identifies existing journal entries by text only, ignoring date
        """

        super().__init__(target="")
        self.convert = convert_entry
        self.visibility = visibility
        self.service = service
        self.identify_by_text_only = identify_by_text_only

    def write(self, instance, value):
        if not value:
            return

        responsible_service = self.service

        if not responsible_service:
            responsible_service = instance.responsible_service()

        if isinstance(value, list):
            errors = []
            for v in value:
                try:
                    converted = self.convert(v)
                    self._create_entry(converted, instance, responsible_service)
                except ValueError as e:  # pragma: no cover
                    errors.append(e)
            if errors:  # pragma: no cover
                raise ValueError(f"Could not convert some values: {errors}")
        else:
            self._create_entry(self.convert(value), instance, responsible_service)

    def _create_entry(self, value: TextWithDate | None, instance, responsible_service):
        if value and value.text and value.date:
            existing_entry = (
                JournalEntry.objects.filter(instance=instance, text=value.text).first()
                if self.identify_by_text_only
                else JournalEntry.objects.filter(
                    instance=instance, creation_date=value.date, text=value.text
                ).first()
            )

            if existing_entry:
                existing_entry.service = responsible_service
                existing_entry.visibility = self.visibility
                existing_entry.user = instance.user
                existing_entry.save()
            else:
                JournalEntry.objects.create(
                    instance=instance,
                    service=responsible_service,
                    user=instance.user,
                    text=value.text,
                    creation_date=value.date,
                    modification_date=value.date,
                    visibility=self.visibility,
                )


class Transform(FieldWriter):
    """A field writer that transforms values before delegating to another writer.

    This writer applies a transformation function to the input value before
    passing it to a delegate writer. The transformation function receives the
    value, dossier, and caluma_user from the context.

    Args:
        writer: The FieldWriter to delegate the transformed value to
        transform: A callable that transforms the value, taking (value, dossier, caluma_user, instance)
                   as arguments and returning the transformed value
    """

    def __init__(
        self,
        transform: Callable[[Any, Dossier, BaseUser, Instance], Any],
        writer: FieldWriter,
    ):
        super().__init__(target="")
        self.transform = transform
        self.writer = writer

    def write(self, instance, value):
        self.writer.owner = self.owner
        self.writer.context = self.context
        dossier = self.context.get("dossier")
        caluma_user = self.context.get("caluma_user")
        try:
            self.writer.write(
                instance, self.transform(value, dossier, caluma_user, instance)
            )
        except ValueError as e:
            dossier._meta.errors.append(
                Message(
                    level=Severity.WARNING.value,
                    code=MessageCodes.FIELD_VALIDATION_ERROR.value,
                    detail=_("Failed to write %(value)s: %(error)s")
                    % {"value": value, "error": e},
                )
            )


class MultipleTargetsWriter(FieldWriter):
    """A field writer that delegates the same value to multiple target writers.

    This writer allows writing a single source value to multiple destinations
    by delegating to a list of FieldWriter instances. Each delegate writer
    receives the same value and can write it to its own target.

    Args:
        writers: A list of FieldWriter instances that will each receive the value
        one_successfull_sufficient: optional, default: False. If True, only one delegate needs to succeed for the write to be considered successful and no reporting to be added
    """

    def __init__(
        self, writers: list[FieldWriter], one_successfull_sufficient: bool = False
    ):
        super().__init__(target="")
        self.writers = writers
        self.one_successfull_sufficient = one_successfull_sufficient

    def write(self, instance, value):
        all_errors = []
        for delegate in self.writers:
            try:
                delegate.owner = self.owner
                delegate.context = self.context
                delegate.write(instance, value)
            except Exception as e:
                all_errors.append(e)

        self._handle_errors(all_errors, value)

    def _handle_errors(self, all_errors, value):
        if len(all_errors) == len(self.writers) or not self.one_successfull_sufficient:
            dossier = self.context.get("dossier")
            for error in all_errors:
                dossier._meta.errors.append(
                    Message(
                        level=Severity.WARNING.value,
                        code=MessageCodes.UNHANDLED_EXCEPTION.value,
                        detail=_("Failed to write %(value)s: %(error)s")
                        % {"value": value, "error": error},
                    )
                )


class KtAargauDossierWriter(DossierWriter):
    cantonal_id = KeywordWriter()

    plot_data = CalumaTableAnswerWriter(
        target="parzelle", column_mapping=PLOT_DATA_MAPPING
    )

    coordinates = CalumaAnswerWriter(
        target="gis-map",
        formatter=lambda coords: (
            json.dumps(
                {
                    "markers": [{"x": c.e, "y": c.n} for c in coords if c.e and c.n],
                    "geometry": "POINT",
                }
            )
            if coords
            else None
        ),
    )

    proposal = CalumaAnswerWriter(target="beschreibung-bauvorhaben", protected=True)

    street = CalumaCombinedStreetAndNumberWriter(
        target="street-and-housenumber",
        fields=["street", "street_number"],
    )

    zip = CalumaAnswerWriter(target="plz", formatter=int)

    city = CalumaAnswerWriter(target="ort-grundstueck")

    usage = CalumaAnswerWriter(target="zonenplan")

    application_type = Transform(
        transform=lambda value, _, __, instance: (
            value
            if instance.case.document.form.slug == "importiertes-dossier"
            else None
        ),
        writer=CalumaAnswerWriter(target="geschaeftstyp-import"),
    )

    submit_date = SubmitDateWriter()

    publication_date = JournalWriter(
        lambda v: TextWithDate(text=f"Publikationsdatum: {v}") if v else None,
        identify_by_text_only=True,
    )

    decision_date = MultipleTargetsWriter(
        [
            JournalWriter(
                lambda v: TextWithDate(text=f"Datum Entscheid: {v}") if v else None,
                identify_by_text_only=True,
            ),
            CalumaAnswerWriter(target="entscheid-datum", task="decision"),
        ]
    )

    construction_start_date = JournalWriter(
        lambda v: TextWithDate(text=f"Datum Baubeginn: {v}") if v else None,
        identify_by_text_only=True,
    )

    profile_approval_date = JournalWriter(
        lambda v: TextWithDate(text=f"Datum Schnurgerüstabnahme: {v}") if v else None,
        identify_by_text_only=True,
    )

    final_approval_date = JournalWriter(
        lambda v: TextWithDate(text=f"Datum Schlussabnahme: {v}") if v else None,
        identify_by_text_only=True,
    )

    completion_date = JournalWriter(
        lambda v: TextWithDate(text=f"Datum Bauende: {v}") if v else None,
        identify_by_text_only=True,
    )

    custom_1 = JournalWriter(
        lambda v: TextWithDate(text=f"Freies Textfeld 1: {v}") if v else None,
        identify_by_text_only=True,
    )

    custom_2 = JournalWriter(
        lambda v: TextWithDate(text=f"Freies Textfeld 2: {v}") if v else None,
        identify_by_text_only=True,
    )

    project_cost = MultipleTargetsWriter(
        writers=[
            CalumaAnswerWriter(target="total-in-chf-migration", formatter=float),
            CalumaAnswerWriter(target="baukosten", formatter=int),
        ],
        one_successfull_sufficient=True,
    )

    link = JournalWriter(
        lambda v: TextWithDate(text=f"Link: {v}") if v else None,
        identify_by_text_only=True,
    )

    applicant = CalumaTableAnswerWriter(
        target="personalien-gesuchstellerin",
        column_mapping=PERSON_MAPPING,
        value_mapping=PERSON_VALUE_MAPPING,
    )

    landowner = CalumaTableAnswerWriter(
        target="personalien-grundeigentumerin",
        column_mapping=PERSON_MAPPING,
        value_mapping=PERSON_VALUE_MAPPING,
    )

    project_author = CalumaTableAnswerWriter(
        target="personalien-projektverfasserin",
        column_mapping=PERSON_MAPPING,
        value_mapping=PERSON_VALUE_MAPPING,
    )

    responsible = ResponsibleUserWriter(target="responsible")

    def create_instance(self, dossier: Dossier, is_paper=False) -> Instance:
        return super().create_instance(dossier, True)

    def find_existing_instance(self, dossier, user):
        # 1. directly check for dossier.id in the keywords (formerly migrated or imported dossier with that communal id)
        k = super().find_existing_instance(dossier, user)

        if k:
            return k

        if dossier.cantonal_id:
            # 2. consider cantonal_id from earlier SAP migration if it starts with "BVUAFB"
            if dossier.cantonal_id.startswith("BVUAFB"):
                k = Keyword.objects.filter(
                    name=dossier.cantonal_id, service=self._group.service
                ).first()

                if k:
                    return k.instances.first()

            # 3. consider cantonal_id as id from DIBA light dossier
            if re.match(r"^2\d{3}-\d+$", dossier.cantonal_id):
                instance = (
                    Instance.objects.filter(
                        **{"case__meta__dossier-number": dossier.cantonal_id}
                    )
                    .filter(group__service=self._group.service)
                    .first()
                )

                if instance:
                    return instance

            # report this dossier
            if os.getenv("KEYCLOAK_CLIENT", "") == "diba-prod-intern":
                raise DossierWriter.ConfigurationError(
                    f"Dossier with cantonal_id {dossier.cantonal_id} not found"
                )

        return None

    def _post_write_fields(self, instance, dossier):
        self._write_triage_fields(instance)
        work_items = instance.case.work_items.all()
        mark_work_items_as_imported(work_items)
        # handle case, that keyword for dossier id is not yet there, because instance already was there and was matched
        # with dossier.cantonal_id
        self.link_instance_and_dossier(instance, dossier, self._user)

    def _lookup_service(self, municipality_name):
        """Look up service ID by municipality name.

        Args:
            municipality_name: Name of the municipality to look up

        Returns:
            Service ID as string if found, None otherwise
        """
        if not municipality_name:
            return None

        service = Service.objects.filter(name=municipality_name).first()
        return str(service.pk) if service else None

    def _write_triage_fields(self, instance: Instance):
        """Write triage answers for personal data.

        The table questions for landowner, and project author are only displayed if the multi-select contains these values.
        """

        answers = []
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
                    answers.append("weitere-personen-grundeigentumerin")
                elif table_question == "personalien-projektverfasserin":
                    answers.append("weitere-personen-projektverfasserin")

        save_answer(
            document=instance.case.document,
            question=Question.objects.get(slug="weitere-personen"),
            value=answers,
            user=self._caluma_user,
        )

    def get_workflow_skip_path(self, instance: Instance, dossier: Dossier) -> list[str]:
        """Return the skip path per target state."""
        SUBMITTED = ["submit"]
        DECIDED = SUBMITTED + [
            "formal-exam",
            "cantonal-exam",
            "distribution",
            "decision",
        ]
        REJECTED = DECIDED + [
            "create-manual-workitems",
            "complete-instance",
            "archive-instance",
        ]
        DONE = DECIDED + [
            "create-manual-workitems",
            "init-construction-monitoring",
            "complete-instance",
            "archive-instance",
        ]

        return {
            TargetStatus.SUBMITTED.value: SUBMITTED,
            TargetStatus.APPROVED.value: DECIDED,
            TargetStatus.REJECTED.value: REJECTED,
            TargetStatus.WRITTEN_OFF.value: DECIDED,
            TargetStatus.DONE.value: DONE,
        }[dossier._meta.target_state]

    def get_existing_and_new_dossier_ids(
        self, dossier_and_cantonal_ids: list[tuple[str, str]]
    ) -> tuple[set[str], set[str], Mapping[str, str]]:
        """Set-based implementation of AG-specific validation code for find_existing_dossier."""

        ids_excel = {dossier_id for dossier_id, _ in dossier_and_cantonal_ids}
        cantonal_ids_excel = {
            cantonal_id for _, cantonal_id in dossier_and_cantonal_ids
        }
        all_ids_excel = ids_excel.union(cantonal_ids_excel)

        keyword_to_dossier_number = dict(
            list(
                Keyword.objects.filter(
                    name__in=all_ids_excel,
                    service=self._group.service,
                    instances__isnull=False,
                ).values_list("name", "instances__case__meta__dossier-number")
            )
        )
        all_keywords_from_db = set(keyword_to_dossier_number.keys())

        # 1. ids from Excel that are not yet in the database with a keyword
        new_ids = ids_excel - all_keywords_from_db

        # 2. remove ids from Excel where the additional cantonal_id already is in the database, as a keyword
        mapped_excel_ids = {}
        for dossier_id, cantonal_id in dossier_and_cantonal_ids:
            if (
                cantonal_id
                and cantonal_id.startswith("BVUAFB")
                and cantonal_id in all_keywords_from_db
            ):
                new_ids.discard(dossier_id)
                mapped_excel_ids[keyword_to_dossier_number[cantonal_id]] = dossier_id

        # 3. remove ids from Excel where the cantonal_id already is in the database, as an dossier_id
        all_existing_dossier_numbers_from_db = set(
            Instance.objects.filter(
                case__meta__has_key="dossier-number",
                group__service=self._group.service,
            ).values_list("case__meta__dossier-number", flat=True)
        )
        for dossier_id, cantonal_id in dossier_and_cantonal_ids:
            if (
                cantonal_id
                and re.match(r"^2\d{3}-\d+$", cantonal_id)
                and cantonal_id in all_existing_dossier_numbers_from_db
            ):
                new_ids.discard(dossier_id)
                mapped_excel_ids[cantonal_id] = dossier_id

        return ids_excel - new_ids, new_ids, mapped_excel_ids
