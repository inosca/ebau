import json
from dataclasses import dataclass, fields
from datetime import datetime
from logging import getLogger
from textwrap import dedent
from typing import Any, Callable, Dict, List, Optional

from caluma.caluma_form import api as form_api
from caluma.caluma_form.models import Form as CalumaForm, Question
from caluma.caluma_user.models import BaseUser
from caluma.caluma_workflow import api as workflow_api
from caluma.caluma_workflow.api import (
    complete_work_item,
    resume_work_item,
    skip_work_item,
)
from caluma.caluma_workflow.models import WorkItem
from codetiming import Timer
from django.conf import settings
from django.db.utils import IntegrityError
from django.utils import timezone
from django.utils.translation import gettext as _

from camac.applicants.models import ROLE_CHOICES, Applicant
from camac.caluma.extensions.events.general import get_caluma_setting
from camac.core.models import InstanceService
from camac.core.utils import generate_sort_key
from camac.deadlines.models import DeadlineType, InstanceDeadline
from camac.dossier_import.config.kt_ag_sap_migration.dossier_import.dossier_classes import (
    CantonComment,
    KtAargauDossier,
    Workflow,
)
from camac.dossier_import.config.kt_ag_sap_migration.dossier_import.dossier_loader import (
    date_from_yyyymmdd,
    datetime_from_long_number,
    datetime_from_yyyymmdd,
    noop,
)
from camac.dossier_import.config.kt_ag_sap_migration.dossier_import.writer_mappings import (
    APPLICATION_TYPE_MAPPING,
    BUILDING_MAPPING,
    CANTON_APPLICATION_CODES,
    DOSSIER_TYPE_MAPPING,
    DOSSIER_TYPE_TO_FORM_MAPPING,
    MUNICIPALITY_ID_AFB,
    OLD_MUNICIPALITIES,
    PATH_TO_STATE,
    PERSON_MAPPING,
    PERSON_VALUE_MAPPING,
    PLOT_DATA_MAPPING,
    SUBMISSION_REASON_MAP,
    CantonalState,
    map_target_state,
)
from camac.dossier_import.dossier_classes import Coordinates, Dossier, Person, PlotData
from camac.dossier_import.loaders import safe_join
from camac.dossier_import.messages import (
    DossierSummary,
    Message,
    MessageCodes,
    Severity,
)
from camac.dossier_import.models import MigrationDocumentStatus
from camac.dossier_import.writers import (
    CalumaAnswerWriter,
    CalumaListAnswerWriter,
    CaseMetaWriter,
    DossierWriter,
    FieldWriter,
)
from camac.instance.domain_logic import CreateInstanceLogic
from camac.instance.models import Form, Instance, InstanceState, JournalEntry
from camac.permissions.events import core as permissions_events
from camac.permissions.models import AccessLevel, InstanceACL
from camac.rulesets.utils import assign_responsible_user
from camac.tags.models import Keyword
from camac.user.models import Service

NBSP = "\u00a0"

log = getLogger(__name__)


def _add_keyword_if_needed(value: str | None, instance: Instance, service: Service):
    if not value:
        return

    keyword = Keyword.objects.filter(name=value, service=service).first()

    if keyword:  # pragma: no cover
        keyword.instances.add(instance)
    else:
        instance.keywords.create(name=value, service=service)


class KeywordWriter(FieldWriter):
    def __init__(self):
        super().__init__(target="")

    def write(self, instance, value):
        _add_keyword_if_needed(value, instance, instance.responsible_service())


@dataclass
class TextWithDate:
    date: datetime
    text: str


class JournalWriter(FieldWriter):
    def __init__(
        self,
        convert_entry: Callable[[Any], TextWithDate],
        visibility: Optional[str] = "own_organization",
        service: Optional[Service] = None,
        identify_by_text_only: Optional[bool] = False,
    ):
        """Initialize journal writer for importing historical entries.

        Args:
            convert_entry: Function to convert input value to TextWithDate object
            visibility: Journal entry visibility setting, defaults to "own_organization"
            service: the service owning the journal entry
            identify_by_text_only: If True, identifies duplicates by text only, ignoring date
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

    def _create_entry(
        self, value: Optional[TextWithDate], instance, responsible_service
    ):
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


class TransformingWriter(FieldWriter):
    def __init__(
        self, delegate: FieldWriter, transform: Callable[[Any, Dossier, BaseUser], Any]
    ):
        super().__init__(target="")
        self.transform = transform
        self.delegate = delegate

    def write(self, instance, value):
        self.delegate.owner = self.owner
        self.delegate.context = self.context
        dossier = self.context.get("dossier")
        caluma_user = self.context.get("caluma_user")
        self.delegate.write(instance, self.transform(value, dossier, caluma_user))


class MultipleTargetsWriter(FieldWriter):
    def __init__(self, delegates: List[FieldWriter]):
        super().__init__(target="")
        self.delegates = delegates

    def write(self, instance, value):
        for delegate in self.delegates:
            delegate.owner = self.owner
            delegate.context = self.context
            delegate.write(instance, value)


_SERVICE_CACHE = {}


def _lookup_service_by_slug(slug):
    if slug not in _SERVICE_CACHE:
        service = Service.objects.filter(slug=slug)
        if service:
            _SERVICE_CACHE[slug] = service[0]
        else:
            raise ValueError(f"Service with slug {slug} not found")  # pragma: no cover

    return _SERVICE_CACHE[slug]


def _lookup_service_by_bfs(bfs_number):
    try:
        return Service.objects.get(external_identifier=bfs_number)
    except Exception:
        raise ValueError(f"Could not find municipality with BFS number '{bfs_number}'")


def _lookup_service_by_id(id):
    try:
        return Service.objects.get(service_id=id)
    except Exception:  # pragma: no cover
        raise ValueError(f"Could not find municipality with id '{id}'")


def lookup_municipality_id_by_bfs_number(bfs_number: str) -> str:
    service = _lookup_service_by_bfs(bfs_number)

    return str(service.service_id)


def _get_first_non_afb(other_municipalities):
    if not other_municipalities:
        return None

    return next(
        (m.value for m in other_municipalities if m.value != MUNICIPALITY_ID_AFB), None
    )


def effective_municipality_id(bfs_number: str, dossier: KtAargauDossier, _=None):
    bfs_number = OLD_MUNICIPALITIES.get(bfs_number, bfs_number)

    if bfs_number == MUNICIPALITY_ID_AFB:
        other = _get_first_non_afb(dossier.other_municipalities)
        if other:
            return effective_municipality_id(other, dossier)
        else:
            return None

    return lookup_municipality_id_by_bfs_number(bfs_number)


def lookup_responsible_service(
    bfs_number: str, dossier: KtAargauDossier, _=None
) -> Service:
    if bfs_number == MUNICIPALITY_ID_AFB:  # pragma: no cover
        return _lookup_service_by_slug("pgv")

    return _lookup_service_by_id(effective_municipality_id(bfs_number, dossier))


class Table:
    def __init__(
        self,
        max_cols: Optional[int] = 4,
        width: Optional[int] = 120,
        padding_char: Optional[str] = NBSP,
    ):
        self.col_width = width // max_cols
        self.padding_char = padding_char
        self.buffer = ""

    def row(self, cols: Optional[List[str]] = []):
        for col in cols:
            col = str(col) if col else ""
            self.buffer += col.ljust(self.col_width, self.padding_char)
        self.buffer += "\n"
        return self

    def __str__(self):
        return self.buffer


def _transform_workflows(workflows: List[Workflow], dossier: Dossier, _: BaseUser):
    """Transform and consolidate workflows with their documents and recipients.

    For each workflow:
    - Assign documents without recipient_id directly to workflow
    - Assign documents with recipient_id to matching recipient
    - Only include docs/recipients matching workflow_id
    """
    dossier: KtAargauDossier
    result = []

    for workflow in workflows:
        # Get matching docs and recipients for this workflow
        matching_docs = [
            doc for doc in dossier.workflow_docs if doc.workflow_id == workflow.id
        ]
        matching_recipients = [
            recipient
            for recipient in dossier.workflow_recipients
            if recipient.workflow_id == workflow.id
        ]

        # Split docs into those with/without recipient
        docs_without_recipient = [doc for doc in matching_docs if not doc.recipient_id]

        # Assign docs to recipients where recipient_id matches
        for recipient in matching_recipients:
            recipient.docs = [
                doc for doc in matching_docs if doc.recipient_id == recipient.id
            ]

        # Add consolidated data to workflow
        workflow.docs = docs_without_recipient
        workflow.recipients = matching_recipients

        # Convert workflow to TextWithDate object in 6 possible columns, each of width 20 chars
        text = (
            Table()
            .row([workflow.workflow_type.upper()])
            .row(
                [
                    f"Status: {workflow.status or '-'}",
                    f"Zugriff: {'aktiv' if workflow.active else 'inaktiv'}",
                ]
            )
        )

        # Add docs section if documents exist
        if workflow.docs:
            _add_docs(workflow.docs, 0, text)

        # Add recipients section if recipients exist
        if workflow.recipients:
            text.row().row(["Empfänger:"])

            for recipient in workflow.recipients:
                text.row(
                    [
                        f"• {recipient.user_name or ''} ({recipient.user_id or ''} {recipient.user_email or ''})"
                    ]
                )
                text.row(
                    [
                        f"{NBSP * 3}Status: {recipient.status or ''}",
                        f"Aktiv: {_check(recipient.active)}",
                        f"Manuell hinzugefügt: {_check(recipient.manually_added) or ''}",
                        f"Datum: {_datetime_with_time_str(recipient.date) or ''}",
                    ]
                )
                text.row(
                    [f"{NBSP * 3}Anfrage: {recipient.request or ''}"]
                ) if recipient.request else None
                text.row(
                    [f"{NBSP * 3}Grund: {recipient.reason or ''}"]
                ) if recipient.reason else None
                text.row(
                    [f"{NBSP * 3}Bemerkung: {recipient.remark or ''}"]
                ) if recipient.remark else None

                if recipient.docs:  # pragma: no cover
                    _add_docs(workflow.docs, 1, text)

        result.append(TextWithDate(date=workflow.date, text=str(text)))

    return result


def _add_docs(docs, indent, text):
    indent1 = 3 * indent
    indent2 = 3 * (indent + 1)
    text.row(["Dokumente:"])
    for doc in docs:
        text.row(
            [
                f"{NBSP * indent1}• ID: {doc.dms_id} (Version: {doc.dms_version or '-'}, Typ: {doc.doc_type or '-'}, Date: {_datetime_with_time_str(doc.date)})"
            ]
        )
        text.row([f"{NBSP * indent2}Bemerkung: {doc.remark or '-'}"])


def _datetime_with_time_str(date: datetime) -> Optional[str]:
    if not date:  # pragma: no cover
        return None
    return date.strftime("%d.%m.%Y %H:%M")


def _datetime_date_str(date: datetime) -> Optional[str]:
    if not date:
        return None
    return date.strftime("%d.%m.%Y")


UNIX_EPOCH = timezone.make_aware(datetime(1970, 1, 1))


def _is_empty_or_date_before_1970(d: Optional[datetime | str]) -> bool:
    if not d:  # pragma: no cover
        return True
    if isinstance(d, str):
        d = datetime_from_yyyymmdd(d)
    return d < UNIX_EPOCH


def _replace_invalid_date_with_unix_epoch(
    d: Optional[datetime],
) -> Optional[datetime]:  # pragma: no cover
    if _is_empty_or_date_before_1970(d):
        return UNIX_EPOCH

    return d


def _check(checked):
    return "✓" if checked else "-"


def _transform_municipality_in_plots(
    plots: List[PlotData], dossier: KtAargauDossier, user: BaseUser
):
    result = []
    for plot in plots:
        if plot.municipality == MUNICIPALITY_ID_AFB:
            continue

        plot.municipality = lookup_municipality_id_by_bfs_number(
            OLD_MUNICIPALITIES.get(plot.municipality, plot.municipality)
        )

        result.append(plot)

    return result


def _transform_coordinates(coordinates):
    if not coordinates:  # pragma: no cover
        return None
    c: Coordinates = coordinates[0]
    if not c.e or not c.n:  # pragma: no cover
        return None
    return json.dumps({"markers": [{"x": c.e, "y": c.n}], "geometry": "POINT"})


def _clean_phone_numbers(persons: List[Person], dossier: Dossier, user: BaseUser):
    for p in persons:
        p.phone = "".join(c for c in p.phone or "" if c.isprintable())

    return persons


def _sap_date_to_datetime(value: Optional[str]):
    return datetime.strptime(value, "%Y%m%d") if value else None


def _converted_value_if_not_draft(converter: Callable, value: Any, dossier: Dossier):
    if dossier._meta.target_state != "Gesuch in Erfassung":
        return converter(value)
    return None  # pragma: no cover


def _empty_if_diba_light(value: Any, dossier: KtAargauDossier):  # pragma: no cover
    if dossier.is_municipality_light:
        return None
    return value


def _get_multi_selected_options(option_conditions: Dict[str, bool]) -> List[str]:
    return [option for option, condition in option_conditions.items() if condition]


def _get_selected_option(answer_conditions: Dict[str, bool]) -> Optional[str]:
    return next(
        (answer for answer, condition in answer_conditions.items() if condition), None
    )


def _remove_lines_with_None(text: str) -> str:
    return "\n".join(filter(lambda line: "None" not in line, text.split("\n")))


class KtAargauDossierWriter(DossierWriter):
    responsible_municipality = TransformingWriter(
        delegate=CalumaAnswerWriter(target="gemeinde"),
        transform=effective_municipality_id,
    )

    other_municipalities = TransformingWriter(
        delegate=CalumaAnswerWriter(target="weitere-gemeinden"),
        transform=lambda value, dossier, user: [
            lookup_municipality_id_by_bfs_number(
                OLD_MUNICIPALITIES.get(municipality.value, municipality.value)
            )
            for municipality in value
        ],
    )

    proposal = CalumaAnswerWriter(target="beschreibung-bauvorhaben", protected=True)

    description = CalumaAnswerWriter(target="beschreibung-bauvorhaben-details")

    cantonal_id = KeywordWriter()

    municipal_id = KeywordWriter()

    procedural_status = JournalWriter(
        lambda ps_entry: TextWithDate(
            ps_entry.timestamp,
            dedent(f"""\
                VERFAHRENSSTAND
                Aktion: {ps_entry.action or "-"}
                Schritt: {ps_entry.step or "-"}
                Wer: {ps_entry.username or "-"}
                Kommentar: {ps_entry.comment or "-"}
                """),
        )
    )

    comments = JournalWriter(
        lambda comment: TextWithDate(
            comment.timestamp,
            dedent(f"""\
                KOMMENTAR
                Sachbearbeiter: {comment.username} ({comment.userid})
                Kommentar: {comment.text or "-"}
                """),
        )
    )

    decisions = MultipleTargetsWriter(
        [
            JournalWriter(
                lambda d: TextWithDate(
                    _replace_invalid_date_with_unix_epoch(d.decision_date),
                    _remove_lines_with_None(
                        dedent(f"""\
                            ENTSCHEID
                            Entscheidung: {d.type}
                            Verfügungsdatum: {_datetime_date_str(d.decision_date)}
                            Rechtskraftdatum: {_datetime_date_str(d.legal_binding_date)}
                            Rechtsmittel ergriffen am: {_datetime_date_str(d.legal_remedy_taken_date)}
                            Bemerkung: {d.remark}
                    """)
                    ),
                )
            ),
            TransformingWriter(
                # transform to single Decision with latest decision_date
                transform=lambda decisions_value, _d, _u: max(
                    decisions_value, key=lambda d: d.decision_date, default=None
                ),
                delegate=MultipleTargetsWriter(
                    [
                        TransformingWriter(
                            delegate=CalumaAnswerWriter(
                                target="entscheid-entscheid", task="decision"
                            ),
                            transform=lambda decision, dossier, _u: (
                                "entscheid-entscheid-rueckzug"
                                if dossier.municipal_status == "Gesuch zurückgezogen"
                                else "entscheid-entscheid-abschreibung"
                                if dossier.municipal_status == "Gesuch abgeschrieben"
                                else {
                                    "Bewilligung": "entscheid-entscheid-baubewilligung-erteilt",
                                    "Abschreibung": "entscheid-entscheid-abschreibung",
                                    "Nichteintreten": "entscheid-entscheid-abschreibung",
                                    "Abweisung": "entscheid-entscheid-abweisung",
                                    "Teilabweisung": "entscheid-entscheid-teilbaubewilligung",
                                    "Antwort auf Anfrage": "entscheid-entscheid-kenntnisnahme",
                                }.get(decision.type)
                                if decision
                                else None
                            ),
                        ),
                        TransformingWriter(
                            delegate=CalumaAnswerWriter(
                                target="entscheid-datum",
                                task="decision",
                            ),
                            transform=lambda decision, dossier, _u: (
                                UNIX_EPOCH
                                if (not decision or not decision.decision_date)
                                and dossier.municipal_status == "Gesuch abgeschrieben"
                                else _replace_invalid_date_with_unix_epoch(
                                    decision.decision_date
                                )
                                if decision
                                else None
                            ),
                        ),
                        CalumaAnswerWriter(
                            target="entscheid-bemerkungen",
                            task="decision",
                            formatter=lambda decision: (
                                _remove_lines_with_None(
                                    dedent(f"""\
                                    {decision.remark}
                                    Verfügungsdatum: {_datetime_date_str(decision.decision_date)}
                                    Rechtskraftdatum: {_datetime_date_str(decision.legal_binding_date)}
                                    Rechtsmittel ergriffen am: {_datetime_date_str(decision.legal_remedy_taken_date)}
                                """)
                                )
                                if decision
                                else None
                            ),
                        ),
                    ]
                ),
            ),
        ]
    )

    workflows = TransformingWriter(
        delegate=JournalWriter(noop),
        transform=_transform_workflows,
    )

    deadlines = JournalWriter(
        lambda d: TextWithDate(
            d.date_from,
            str(
                Table(4, 120)
                .row([d.type.upper()])
                .row(
                    [
                        f"Von: {_datetime_date_str(d.date_from) or ''}",
                        f"Bis: {_datetime_date_str(d.date_to) or ''}",
                        f"Abgeschlossen: {_check(d.completed)}",
                    ]
                )
                .row([f"Bemerkung: {d.notice or ''}"])
                .row([f"Grund: {d.reason or ''}"])
            ),
        )
    )

    submit_date = CaseMetaWriter(
        target="submit-date", formatter="datetime-to-string", protected=True
    )

    street = TransformingWriter(
        delegate=CalumaAnswerWriter(target="street-and-housenumber"),
        transform=lambda street, dossier, _: (
            safe_join((street, dossier.street_number))
            if (
                dossier.street
                and dossier.street_number
                and not dossier.street.endswith(dossier.street_number)
            )
            else dossier.street
        ),
    )

    zip = CalumaAnswerWriter(target="plz", formatter=int)
    city = CalumaAnswerWriter(target="ort-grundstueck")

    plot_data = TransformingWriter(
        delegate=CalumaListAnswerWriter(
            target="parzelle", column_mapping=PLOT_DATA_MAPPING
        ),
        transform=_transform_municipality_in_plots,
    )

    coordinates = CalumaAnswerWriter(target="gis-map", formatter=_transform_coordinates)

    building = CalumaListAnswerWriter(
        target="gebaeude", column_mapping=BUILDING_MAPPING
    )

    applicant = TransformingWriter(
        delegate=CalumaListAnswerWriter(
            target="personalien-gesuchstellerin",
            column_mapping=PERSON_MAPPING,
            value_mapping=PERSON_VALUE_MAPPING,
        ),
        transform=_clean_phone_numbers,
    )

    landowner = TransformingWriter(
        delegate=CalumaListAnswerWriter(
            target="personalien-grundeigentumerin",
            column_mapping=PERSON_MAPPING,
            value_mapping=PERSON_VALUE_MAPPING,
        ),
        transform=_clean_phone_numbers,
    )

    project_author = TransformingWriter(
        delegate=CalumaListAnswerWriter(
            target="personalien-projektverfasserin",
            column_mapping=PERSON_MAPPING,
            value_mapping=PERSON_VALUE_MAPPING,
        ),
        transform=_clean_phone_numbers,
    )

    invoice_recipient = TransformingWriter(
        delegate=CalumaListAnswerWriter(
            target="personalien-rechnungsempfaenger",
            column_mapping=PERSON_MAPPING,
            value_mapping=PERSON_VALUE_MAPPING,
        ),
        transform=_clean_phone_numbers,
    )

    legal_representative = TransformingWriter(
        delegate=CalumaListAnswerWriter(
            target="vertreterin-mit-vollmacht",
            column_mapping=PERSON_MAPPING,
            value_mapping=PERSON_VALUE_MAPPING,
        ),
        transform=_clean_phone_numbers,
    )

    application_type = TransformingWriter(
        delegate=CalumaAnswerWriter(
            target="vorlaeufige-pruefung-verfahrensart", task="formal-exam"
        ),
        transform=lambda value, dossier, _: _empty_if_diba_light(
            _converted_value_if_not_draft(APPLICATION_TYPE_MAPPING.get, value, dossier),
            dossier,
        ),
    )

    submission_reason = CalumaAnswerWriter(
        target="erfassungsgrund", formatter=SUBMISSION_REASON_MAP.get
    )

    dossier_types = TransformingWriter(
        delegate=CalumaAnswerWriter(target="art-des-gesuchs"),
        transform=lambda dt, _d, _u: [
            DOSSIER_TYPE_MAPPING.get(f.name) for f in fields(dt) if getattr(dt, f.name)
        ],
    )

    profiling = MultipleTargetsWriter(
        [
            CalumaAnswerWriter(
                target="baugespann",
                formatter={
                    True: "baugespann-ja",
                    False: "baugespann-nein",
                }.get,
            ),
            TransformingWriter(
                delegate=CalumaAnswerWriter(
                    target="vorlaeufige-pruefung-profilierung", task="formal-exam"
                ),
                transform=lambda value, dossier, _: _empty_if_diba_light(
                    _converted_value_if_not_draft(
                        {
                            True: "vorlaeufige-pruefung-profilierung-ja",
                            False: "vorlaeufige-pruefung-profilierung-nein",
                        }.get,
                        value,
                        dossier,
                    ),
                    dossier,
                ),
            ),
        ]
    )

    profiling_date = MultipleTargetsWriter(
        [
            CalumaAnswerWriter(
                target="baugespann-erstellt-am", formatter=_sap_date_to_datetime
            ),
            TransformingWriter(
                delegate=CalumaAnswerWriter(
                    target="vorlaeufige-pruefung-profilierungsdatum", task="formal-exam"
                ),
                transform=lambda value, dossier, _: _empty_if_diba_light(
                    _converted_value_if_not_draft(
                        converter=_sap_date_to_datetime,
                        value=value,
                        dossier=dossier,
                    ),
                    dossier,
                ),
            ),
        ]
    )

    profile_approval_date = TransformingWriter(
        delegate=CalumaAnswerWriter(
            target="vorlaeufige-pruefung-kontrolle-profilierung", task="formal-exam"
        ),
        transform=lambda value, dossier, _: _empty_if_diba_light(
            _converted_value_if_not_draft(
                converter=_sap_date_to_datetime,
                value=value,
                dossier=dossier,
            ),
            dossier,
        ),
    )

    profiling_reasoning = CalumaAnswerWriter(target="profilierung-nein-begruendung")

    # Zweckbestimmung

    # residential_use
    # commercial_and_industrial_use
    # agricultural_use
    other_buildings = TransformingWriter(
        delegate=CalumaAnswerWriter(
            target="zweckbestimmung-migration",
        ),
        transform=lambda _v, dossier, _u: _get_multi_selected_options(
            {
                "zweckbestimmung-migration-wohnnutzung": dossier.residential_use,
                "zweckbestimmung-migration-gewerbliche-und-industrielle-nutzung": dossier.commercial_and_industrial_use,
                "zweckbestimmung-migration-landwirtschaftliche-nutzung": dossier.agricultural_use,
                "zweckbestimmung-migration-andere-bauten": dossier.other_buildings,
            }
        ),
    )

    residence = CalumaListAnswerWriter(
        target="wohnungen-migration",
        column_mapping={
            "number_of_residential_units": "anzahl-wohnungen-tabelle",
            "number_of_rooms": "wohnhaus-anzahl-zimmer",
            "of_which_second_homes": "zweitwohnungen",
        },
    )

    commercial_and_industrial_type_of_use = CalumaAnswerWriter(
        target="nutzungsart-migration",
        formatter={
            "Dienstleistung": "nutzungsart-migration-dienstleistung",
            "Gewerbe": "nutzungsart-migration-gewerbe",
            "Industrie": "nutzungsart-migration-industrie",
        }.get,
    )

    commercial_and_industrial_sector = CalumaAnswerWriter(
        target="branche-migration",
    )
    owned_land_total_ha = CalumaAnswerWriter(
        target="eigenland-total-migration",
    )
    leased_land_total_ha = CalumaAnswerWriter(
        target="pachtland-total-migration",
    )
    existing_livestock = CalumaAnswerWriter(
        target="tierbestand-in-gve-bestehend-migration",
    )
    new_livestock = CalumaAnswerWriter(
        target="tierbestand-in-gve-neu-migration",
    )
    other_buildings_designation = CalumaAnswerWriter(
        target="bezeichnung-andere-bauten-migration",
    )
    other_buildings_type_of_use = CalumaAnswerWriter(
        target="nutzungsart-andere-bauten-migration",
    )

    # Gebäudehülle
    building_envelope_exterior_wall_material = CalumaAnswerWriter(
        target="aussenwaende-migration",
    )

    building_envelope_exterior_wall_color = CalumaAnswerWriter(
        target="farbe-der-aussenwaende-migration",
    )

    building_envelope_roof_covering_material = CalumaAnswerWriter(
        target="dachbelag-migration",
    )

    building_envelope_roof_covering_color = CalumaAnswerWriter(
        target="farbe-des-dachbelags-migration",
    )

    # parking spaces
    parking_affected = CalumaAnswerWriter(
        target="parkplaetze-betroffen",
        formatter={
            True: "parkplaetze-betroffen-ja",
            False: "parkplaetze-betroffen-nein",
        }.get,
    )
    existing_parking_spaces = CalumaAnswerWriter(
        target="anzahl-bestehende-parkplaetze-migration",
    )
    existing_mandatory_spaces = CalumaAnswerWriter(
        target="davon-pflichtparkplaetze-bestehend-migration",
    )
    existing_non_mandatory_spaces = CalumaAnswerWriter(
        target="davon-nicht-pflichtparkplaetze-bestehend-migration",
    )
    new_parking_spaces = CalumaAnswerWriter(
        target="anzahl-neue-parkplaetze-migration",
    )
    new_mandatory_spaces = CalumaAnswerWriter(
        target="davon-pflichtparkplaetze-neu-migration",
    )
    new_non_mandatory_spaces = CalumaAnswerWriter(
        target="davon-nicht-pflichtparkplaetze-neu-migration",
    )

    # Gebäudeheizung und Energie

    # building_heating_none
    # building_heating_existing
    # building_heating_new
    # building_heating_replacement
    building_heating_unknown = TransformingWriter(
        delegate=CalumaAnswerWriter(
            target="gebaeudeheizung-typ-migration",
        ),
        transform=lambda _v, dossier, _u: _get_multi_selected_options(
            {
                "gebaeudeheizung-typ-migration-keine": dossier.building_heating_none,
                "gebaeudeheizung-typ-migration-bestehend": dossier.building_heating_existing,
                "gebaeudeheizung-typ-migration-neu-kw": dossier.building_heating_new,
                "gebaeudeheizung-typ-migration-ersatz-kw": dossier.building_heating_replacement,
                "gebaeudeheizung-typ-migration-noch-nicht-bekannt": dossier.building_heating_unknown,
            }
        ),
    )

    building_heating_new_kw = CalumaAnswerWriter(
        target="kw-der-neuen-gebaeudeheizung-migration",
    )

    building_heating_replacement_kw = CalumaAnswerWriter(
        target="kw-der-ersatz-gebaeudeheizung-migration",
    )

    building_heating_unknown_explanation = CalumaAnswerWriter(
        target="begruendung-bei-nicht-bekannt-migration",
    )

    # building_heating_type_oil
    # building_heating_type_oil_new
    # building_heating_type_gas
    # building_heating_type_wood
    # building_heating_type_electric
    # building_heating_type_district
    # building_heating_type_heatpump
    # building_heating_type_heatpump_ground_water
    # building_heating_type_heatpump_air
    # building_heating_type_other
    building_heating_type_other_text = TransformingWriter(
        delegate=CalumaListAnswerWriter(
            target="heizung-migration-tabelle-form",
        ),
        transform=lambda _v, d, _u: list(
            filter(
                None,
                [
                    {
                        "typ-der-heizung": "typ-der-heizung-oel",
                        "bestand-planung": _get_selected_option(
                            {
                                "bestand-planung-neu": d.building_heating_type_oil_new,
                                "bestand-planung-bestehend": not d.building_heating_type_oil_new,
                            }
                        ),
                    }
                    if d.building_heating_type_oil
                    else None,
                    {
                        "typ-der-heizung": "typ-der-heizung-gas",
                    }
                    if d.building_heating_type_gas
                    else None,
                    {
                        "typ-der-heizung": "typ-der-heizung-holz",
                    }
                    if d.building_heating_type_wood
                    else None,
                    {
                        "typ-der-heizung": "typ-der-heizung-elektrisch",
                    }
                    if d.building_heating_type_electric
                    else None,
                    {
                        "typ-der-heizung": "typ-der-heizung-fernheizung",
                    }
                    if d.building_heating_type_district
                    else None,
                    {
                        "typ-der-heizung": "typ-der-heizung-waermepumpe",
                        "typ-der-waermepumpe-heizung": _get_selected_option(
                            {
                                "typ-der-waermepumpe-heizung-bodenwasser": d.building_heating_type_heatpump_ground_water
                                and not d.building_heating_type_heatpump_air,
                                "typ-der-waermepumpe-heizung-luftandere": not d.building_heating_type_heatpump_ground_water
                                and d.building_heating_type_heatpump_air,
                                "typ-der-waermepumpe-heizung-beides": d.building_heating_type_heatpump_ground_water
                                and d.building_heating_type_heatpump_air,
                            }
                        ),
                    }
                    if d.building_heating_type_heatpump
                    else None,
                    {
                        "typ-der-heizung": "typ-der-heizung-andere",
                        "andere-heizungstyp": d.building_heating_type_other_text,
                    }
                    if d.building_heating_type_other
                    else None,
                ],
            )
        ),
    )

    # Bauzonen
    zoning_area = CalumaAnswerWriter(
        target="bauzonen-auswahl-migration",
        formatter={
            "innerhalb rechtskräftiger Bauzone": "bauzonen-auswahl-migration-innerhalb-rechtskraeftiger-bauzone",
            "ausserhalb rechtskräftiger Bauzone": "bauzonen-auswahl-migration-ausserhalb-rechtskraeftiger-bauzone",
            "teilweise innerhalb / teilweise ausserhalb Bauzone": "bauzonen-auswahl-migration-teilweise-innerhalb-teilweise-ausserhalb-bauzone",
            "übriges Gebiet": "bauzonen-auswahl-migration-uebriges-gebiet",
        }.get,
    )

    usage_zone = CalumaAnswerWriter(
        target="zonenplan",
    )

    overlapping_zone = CalumaAnswerWriter(
        target="ueberlagerte-schutzzonen-und-schutzobjekte",
    )

    special_use_plan = CalumaAnswerWriter(
        target="sondernutzungsplanung-migration",
    )

    # Dichteziffern
    ratio_utilization_zone_regulation = CalumaAnswerWriter(
        target="ausnuetzungsziffer-gemaess-zonenordnung-migration",
    )

    ratio_utilization_building_project = CalumaAnswerWriter(
        target="ausnuetzungsziffer-gemaess-bauprojekt-migration",
    )

    ratio_volume_zone_regulation = CalumaAnswerWriter(
        target="baumassenziffer-gemaess-zonenordnung-migration",
    )

    ratio_volume_building_project = CalumaAnswerWriter(
        target="baumassenziffer-gemaess-bauprojekt-migration",
    )

    ratio_green_area_zone_regulation = CalumaAnswerWriter(
        target="gruenflaechenziffer-gemaess-zonenordnung-migration",
    )

    ratio_green_area_building_project = CalumaAnswerWriter(
        target="gruenflaechenziffer-gemaess-bauprojekt-migration",
    )

    ratio_floor_area_zone_regulation = CalumaAnswerWriter(
        target="geschossflaechenziffer-gemaess-zonenordnung-migration",
    )

    ratio_floor_area_building_project = CalumaAnswerWriter(
        target="geschossflaechenziffer-gemaess-bauprojekt-migration",
    )

    ratio_coverage_zone_regulation = CalumaAnswerWriter(
        target="ueberbauungsziffer-gemaess-zonenordnung-migration",
    )

    ratio_coverage_building_project = CalumaAnswerWriter(
        target="ueberbauungsziffer-gemaess-bauprojekt-migration",
    )

    # Bauzonen - weitere Angaben
    # zone_water_protection_area_au
    # zone_water_protection_area_bc
    zone_spring_capture_area = TransformingWriter(
        delegate=CalumaAnswerWriter(
            target="gewaesserschutzbereich-auswahl-migration",
        ),
        transform=lambda _v, d, _u: _get_multi_selected_options(
            {
                "gewaesserschutzbereich-auswahl-migration-au-a": d.zone_water_protection_area_au,
                "gewaesserschutzbereich-auswahl-migration-uebrige-bereiche": d.zone_water_protection_area_bc,
                "gewaesserschutzbereich-auswahl-migration-quellfassungsbereiche": d.zone_spring_capture_area,
            }
        ),
    )

    zone_flood_hazard = CalumaAnswerWriter(
        target="hochwassergefaehrdung-auswahl-migration",
        formatter={
            True: "hochwassergefaehrdung-auswahl-migration-ja",
            False: "hochwassergefaehrdung-auswahl-migration-nein",
        }.get,
    )

    zone_seismic_compliance = CalumaAnswerWriter(
        target="erdbebenkonformitaetserklaerung-migration",
        formatter={
            "nicht erforderlich": "erdbebenkonformitaetserklaerung-migration-nicht-erforderlich",
            "erforderlich und liegt bei": "erdbebenkonformitaetserklaerung-migration-erforderlich-und-liegt-bei",
            "erforderlich und wird vor Baubeginn eingereicht": "erdbebenkonformitaetserklaerung-migration-erforderlich-und-wird-vor-baubeginn-eingereicht",
        }.get,
    )

    zone_sensitivity_level = CalumaAnswerWriter(
        target="empfindlichkeits-stufe-gemaess-bau-und-nutzungsordnung-migration",
        formatter={
            "1": "empfindlichkeits-stufe-gemaess-bau-und-nutzungsordnung-migration-i",
            "2": "empfindlichkeits-stufe-gemaess-bau-und-nutzungsordnung-migration-ii",
            "3": "empfindlichkeits-stufe-gemaess-bau-und-nutzungsordnung-migration-iii",
            "4": "empfindlichkeits-stufe-gemaess-bau-und-nutzungsordnung-migration-iv",
        }.get,
    )

    # Kanalisation & Entwässerung

    # sewage_connection_property
    sewage_connection_property_presence = TransformingWriter(
        delegate=CalumaAnswerWriter(
            target="liegenschaft-migration",
        ),
        transform=lambda _v, dossier, _u: _get_selected_option(
            {
                "liegenschaft-migration-nicht-benoetigt": not dossier.sewage_connection_property,
                "liegenschaft-migration-bestehend": dossier.sewage_connection_property
                and dossier.sewage_connection_property_presence == "bestehend",
                "liegenschaft-migration-neu": dossier.sewage_connection_property
                and dossier.sewage_connection_property_presence == "neu",
                "liegenschaft-migration-nicht-angeschlossen": dossier.sewage_connection_property
                and dossier.sewage_connection_property_presence
                == "nicht angeschlossen",
            }
        ),
    )

    # sewage_connection_construction
    sewage_connection_construction_presence = TransformingWriter(
        delegate=CalumaAnswerWriter(
            target="bauobjekt-kanalisation-migration",
        ),
        transform=lambda _v, dossier, _u: _get_selected_option(
            {
                "bauobjekt-kanalisation-migration-nicht-benoetigt": not dossier.sewage_connection_construction,
                "bauobjekt-kanalisation-migration-bestehend": dossier.sewage_connection_construction
                and dossier.sewage_connection_construction_presence == "bestehend",
                "bauobjekt-kanalisation-migration-neu": dossier.sewage_connection_construction
                and dossier.sewage_connection_construction_presence == "neu",
                "bauobjekt-kanalisation-migration-nicht-angeschlossen": dossier.sewage_connection_construction
                and dossier.sewage_connection_construction_presence
                == "nicht angeschlossen",
            }
        ),
    )

    # stormwater_infiltration
    stormwater_infiltration_new = TransformingWriter(
        delegate=CalumaAnswerWriter(
            target="versickerung",
        ),
        transform=lambda _v, dossier, _u: _get_selected_option(
            {
                "versickerung-nicht-betroffen": not dossier.stormwater_infiltration,
                "versickerung-bestehend": dossier.stormwater_infiltration
                and not dossier.stormwater_infiltration_new,
                "versickerung-neu": dossier.stormwater_infiltration
                and dossier.stormwater_infiltration_new,
            }
        ),
    )

    # stormwater_public_water
    stormwater_public_water_new = TransformingWriter(
        delegate=CalumaAnswerWriter(
            target="in-oeffentliches-gewaesser",
        ),
        transform=lambda _v, dossier, _u: _get_selected_option(
            {
                "in-oeffentliches-gewaesser-nicht-betroffen": not dossier.stormwater_public_water,
                "in-oeffentliches-gewaesser-bestehend": dossier.stormwater_public_water
                and not dossier.stormwater_public_water_new,
                "in-oeffentliches-gewaesser-neu": dossier.stormwater_public_water
                and dossier.stormwater_public_water_new,
            }
        ),
    )

    # stormwater_sewage
    stormwater_sewage_new = TransformingWriter(
        delegate=CalumaAnswerWriter(
            target="kanalisation",
        ),
        transform=lambda _v, dossier, _u: _get_selected_option(
            {
                "kanalisation-nicht-betroffen": not dossier.stormwater_sewage,
                "kanalisation-bestehend": dossier.stormwater_sewage
                and not dossier.stormwater_sewage_new,
                "kanalisation-neu": dossier.stormwater_sewage
                and dossier.stormwater_sewage_new,
            }
        ),
    )

    stormwater_self_use = CalumaAnswerWriter(
        target="eigenverwendung-migration",
        formatter={
            True: "eigenverwendung-migration-ja",
            False: "eigenverwendung-migration-nein",
        }.get,
    )

    # Umweltrechtliche Angaben
    environmental_geothermal_probes_planned = CalumaAnswerWriter(
        target="sind-erdsonden-geplant-migration",
        formatter={
            True: "sind-erdsonden-geplant-ja",
            False: "sind-erdsonden-geplant-nein",
        }.get,
    )

    environmental_special_drilling_or_pump_tests = CalumaAnswerWriter(
        target="sind-sondierbohrungen-oder-pumpversuche-vorgesehen-migration",
        formatter={
            True: "sind-sondierbohrungen-oder-pumpversuche-vorgesehen-migration-ja",
            False: "sind-sondierbohrungen-oder-pumpversuche-vorgesehen-migration-nein",
        }.get,
    )

    environmental_solar_installation_planned = CalumaAnswerWriter(
        target="solaranlage-photovoltaikanalge-geplant",
        formatter={
            True: "solaranlage-photovoltaikanalge-geplant-ja",
            False: "solaranlage-photovoltaikanalge-geplant-nein",
        }.get,
    )

    environmental_contaminated_site_affected = CalumaAnswerWriter(
        target="sind-altlasten-betroffen-migration",
        formatter={
            True: "sind-altlasten-betroffen-ja",
            False: "sind-altlasten-betroffen-nein",
        }.get,
    )

    environmental_groundwater_intervention_required = CalumaAnswerWriter(
        target="grundwasserabsenkungen-bauwasserhaltung-erforderlich-migration",
        formatter={
            True: "grundwasserabsenkungen-bauwasserhaltung-erforderlich-migration-ja",
            False: "grundwasserabsenkungen-bauwasserhaltung-erforderlich-migration-nein",
        }.get,
    )

    environmental_soil_intervention_planned = CalumaAnswerWriter(
        target="sind-eingriffe-in-den-boden-geplant-migration",
        formatter={
            True: "sind-eingriffe-in-den-boden-geplant-migration-ja",
            False: "sind-eingriffe-in-den-boden-geplant-migration-nein",
        }.get,
    )

    environmental_noise_protection_required = CalumaAnswerWriter(
        target="sind-laermschutzmassnahmen-erforderlich-migration",
        formatter={
            True: "sind-laermschutzmassnahmen-erforderlich-ja",
            False: "sind-laermschutzmassnahmen-erforderlich-nein",
        }.get,
    )

    environmental_material_extraction_planned = CalumaAnswerWriter(
        target="ist-ein-materialabbau-geplant-migration",
        formatter={
            True: "ist-ein-materialabbau-geplant-migration-ja",
            False: "ist-ein-materialabbau-geplant-migration-nein",
        }.get,
    )

    environmental_sewer_construction_or_change = CalumaAnswerWriter(
        target="soll-eine-oeffentliche-kanalisation-gebaut-oder-geaendert-werden-migration",
        formatter={
            True: "soll-eine-oeffentliche-kanalisation-gebaut-oder-geaendert-werden-migration-ja",
            False: "soll-eine-oeffentliche-kanalisation-gebaut-oder-geaendert-werden-migration-nein",
        }.get,
    )

    environmental_energy_certificate_required = CalumaAnswerWriter(
        target="energienachweis-erforderlich",
        formatter={
            True: "energienachweis-erforderlich-ja",
            False: "energienachweis-erforderlich-nein",
        }.get,
    )

    # Angaben zur Sicherheit
    safety_fire_protection_canton_required = CalumaAnswerWriter(
        target="ist-eine-kantonale-brandschutzbewilligung-erforderlich-migration",
        formatter={
            True: "ist-eine-kantonale-brandschutzbewilligung-erforderlich-migration-ja",
            False: "ist-eine-kantonale-brandschutzbewilligung-erforderlich-migration-nein",
        }.get,
    )
    safety_fire_protection_heating_required = CalumaAnswerWriter(
        target="kantonale-brandschutzbewilligung-fuer-eine-feuerungsanlage-migration",
        formatter={
            True: "kantonale-brandschutzbewilligung-fuer-eine-feuerungsanlage-migration-ja",
            False: "kantonale-brandschutzbewilligung-fuer-eine-feuerungsanlage-migration-nein",
        }.get,
    )
    safety_fire_protection_communal_required = CalumaAnswerWriter(
        target="kommunale-randschutzbewilligung-erforderlich-migration",
        formatter={
            True: "kommunale-randschutzbewilligung-erforderlich-migration-ja",
            False: "kommunale-randschutzbewilligung-erforderlich-migration-nein",
        }.get,
    )
    safety_employees_affected = CalumaAnswerWriter(
        target="ist-betrieb-betroffen-beschaeftigt-der-betrieb-arbeitnehmende-migration",
        formatter={
            True: "ist-betrieb-betroffen-beschaeftigt-der-betrieb-arbeitnehmende-migration-ja",
            False: "ist-betrieb-betroffen-beschaeftigt-der-betrieb-arbeitnehmende-migration-nein",
        }.get,
    )
    safety_incident_zone_or_infrastructure = CalumaAnswerWriter(
        target="stoerfallverordnung-migration",
        formatter={
            True: "stoerfallverordnung-migration-ja",
            False: "stoerfallverordnung-migration-nein",
        }.get,
    )
    safety_flood_prone_area = CalumaAnswerWriter(
        target="liegt-das-bauvorhaben-in-einem-hochwassergefaehrdeten-gebiet-migration",
        formatter={
            True: "liegt-das-bauvorhaben-in-einem-hochwassergefaehrdeten-gebiet-migration-ja",
            False: "liegt-das-bauvorhaben-in-einem-hochwassergefaehrdeten-gebiet-migration-nein",
        }.get,
    )
    safety_shelter_obligation = CalumaAnswerWriter(
        target="schutzraumbaupflicht-ersatzabgabepflicht-migration",
        formatter={
            True: "schutzraumbaupflicht-ersatzabgabepflicht-migration-ja",
            False: "schutzraumbaupflicht-ersatzabgabepflicht-migration-nein",
        }.get,
    )

    # Kantonsstrasse, Wald

    street_highway_affected = CalumaAnswerWriter(
        target="kantonsstrassen",
        formatter={True: "kantonsstrassen-ja", False: "kantonsstrassen-nein"}.get,
    )

    street_min_distance_undershot = CalumaAnswerWriter(
        target="wird-der-mindestabstand-zur-kantonsstrasse-ueberschritten-migration",
        formatter={
            True: "wird-der-mindestabstand-zur-kantonsstrasse-ueberschritten-migration-ja",
            False: "wird-der-mindestabstand-zur-kantonsstrasse-ueberschritten-migration-nein",
        }.get,
    )

    street_min_distance_reasoning = CalumaAnswerWriter(
        target="begruendung-fuer-die-unterschreitung-kantonsstrasse-migration"
    )

    street_new_or_intensified_access = CalumaAnswerWriter(
        target="ist-eine-neue-erschliessung-an-die-kantonsstrasse-geplant-migration",
        formatter={
            True: "ist-eine-neue-erschliessung-an-die-kantonsstrasse-geplant-migration-ja",
            False: "ist-eine-neue-erschliessung-an-die-kantonsstrasse-geplant-migration-nein",
        }.get,
    )

    street_advertising_planned = CalumaAnswerWriter(
        target="sind-reklamen-im-einflussbereich-der-kantonsstrasse-geplant-migration",
        formatter={
            True: "sind-reklamen-im-einflussbereich-der-kantonsstrasse-geplant-migration-ja",
            False: "sind-reklamen-im-einflussbereich-der-kantonsstrasse-geplant-migration-nein",
        }.get,
    )

    # Wald
    forest_min_distance_undershot = CalumaAnswerWriter(
        target="wird-der-mindestabstand-zum-wald-4-unterschritten-migration",
        formatter={
            True: "wird-der-mindestabstand-zum-wald-4-unterschritten-migration-ja",
            False: "wird-der-mindestabstand-zum-wald-4-unterschritten-migration-nein",
        }.get,
    )

    forest_min_distance_reasoning = CalumaAnswerWriter(
        target="begruendung-fuer-die-unterschreitung-wald-migration"
    )

    forest_project_in_forest = CalumaAnswerWriter(
        target="befindet-sich-das-geplante-bauvorhaben-im-wald-migration",
        formatter={
            True: "befindet-sich-das-geplante-bauvorhaben-im-wald-migration-ja",
            False: "befindet-sich-das-geplante-bauvorhaben-im-wald-migration-nein",
        }.get,
    )

    # Bauen ausserhalb der Bauzone
    outside_building_zone_agricultural_use = CalumaAnswerWriter(
        target="handelt-es-sich-um-einen-landwirtschaftlichen-betrieb-migration",
        formatter={
            True: "handelt-es-sich-um-einen-landwirtschaftlichen-betrieb-migration-ja",
            False: "handelt-es-sich-um-einen-landwirtschaftlichen-betrieb-migration-nein",
        }.get,
    )

    outside_building_zone_legal_nonconforming_use = CalumaAnswerWriter(
        target="handelt-es-sich-um-eine-besitzstandsgeschuetzte-liegenschaft-migration",
        formatter={
            True: "handelt-es-sich-um-eine-besitzstandsgeschuetzte-liegenschaft-migration-ja",
            False: "handelt-es-sich-um-eine-besitzstandsgeschuetzte-liegenschaft-migration-nein",
        }.get,
    )

    outside_building_zone_other_project = CalumaAnswerWriter(
        target="oben-nicht-genanntes-bauvorhaben-ausserhalb-der-bauzone-migration",
        formatter={
            True: "oben-nicht-genanntes-bauvorhaben-ausserhalb-der-bauzone-migration-ja",
            False: "oben-nicht-genanntes-bauvorhaben-ausserhalb-der-bauzone-migration-nein",
        }.get,
    )

    outside_building_zone_terrain_modification = CalumaAnswerWriter(
        target="sind-terrainveraenderungen-ausserhalb-der-bauzone-geplant-migration",
        formatter={
            True: "sind-terrainveraenderungen-ausserhalb-der-bauzone-geplant-migration-ja",
            False: "sind-terrainveraenderungen-ausserhalb-der-bauzone-geplant-migration-nein",
        }.get,
    )

    # Weitere Angaben, Gewässer ...
    special_public_water_body_affected = CalumaAnswerWriter(
        target="ist-mit-dem-vorhaben-ein-oeffentliches-gewaesser-betroffen-migration",
        formatter={
            True: "ist-mit-dem-vorhaben-ein-oeffentliches-gewaesser-betroffen-migration-ja",
            False: "ist-mit-dem-vorhaben-ein-oeffentliches-gewaesser-betroffen-migration-nein",
        }.get,
    )

    special_water_body_name = CalumaAnswerWriter(target="gewaessername-migration")

    special_water_distance_undershot = CalumaAnswerWriter(
        target="ist-mit-dem-vorhaben-der-gewaesserabstand-unterschritten",
        formatter={
            True: "ist-mit-dem-vorhaben-der-gewaesserabstand-unterschritten-ja",
            False: "ist-mit-dem-vorhaben-der-gewaesserabstand-unterschritten-nein",
        }.get,
    )

    special_water_distance_reasoning = CalumaAnswerWriter(
        target="begruendung-fuer-die-unterschreitung-gewaesserabstand"
    )

    special_water_intervention_planned = CalumaAnswerWriter(
        target="einleitung-querung-und-oder-wasserentnahme-migration",
        formatter={
            True: "einleitung-querung-und-oder-wasserentnahme-migration-ja",
            False: "einleitung-querung-und-oder-wasserentnahme-migration-nein",
        }.get,
    )

    special_monument_or_visibility_affected = CalumaAnswerWriter(
        target="denkmalschutzobjekt-oder-steht-ein-denkmalschutz-in-sichtbeziehung-migration",
        formatter={
            True: "denkmalschutzobjekt-oder-steht-ein-denkmalschutz-in-sichtbeziehung-migration-ja",
            False: "denkmalschutzobjekt-oder-steht-ein-denkmalschutz-in-sichtbeziehung-migration-nein",
        }.get,
    )

    special_airspace_obstacle_planned = CalumaAnswerWriter(
        target="ist-ein-luftfahrthindernis-geplant-migration",
        formatter={
            True: "ist-ein-luftfahrthindernis-geplant-migration-ja",
            False: "ist-ein-luftfahrthindernis-geplant-migration-nein",
        }.get,
    )

    # Baukosten

    cost_building_without_land = CalumaAnswerWriter(
        target="baukosten-ohne-land-inkl-allfaellige-abbruchkosten-in-chf-migration"
    )

    cost_environmental_works = CalumaAnswerWriter(
        target="umgebungsarbeiten-in-chf-migration"
    )

    cost_total = CalumaAnswerWriter(target="total-in-chf-migration")

    # Weitere Angaben - Bemerkungen

    notes_comments = CalumaAnswerWriter(target="bemerkungen-und-hinweise-migration")

    # eBau extended

    canton_entry_date = TransformingWriter(
        transform=lambda entry_date, d_, _u: datetime_from_yyyymmdd(entry_date),
        delegate=CaseMetaWriter(
            target="canton-entry-date", formatter="datetime-to-string"
        ),
    )

    # canton_internal_deadline
    # canton_group
    # canton_group_name
    # canton_assignee
    # canton_provisional_closure_date
    # canton_closure_code
    # canton_processing_duration_days
    canton_lwag_number = TransformingWriter(
        delegate=CalumaAnswerWriter(
            target="kantonale-pruefung-migriert-von-ebau-extended", task="cantonal-exam"
        ),
        transform=lambda _v, dossier, _u: (
            dedent(f"""\
                Eingang AfB: {_datetime_date_str(datetime_from_yyyymmdd(dossier.canton_entry_date)) or "-"}
                Bearbeitungsfrist AfB: {_datetime_date_str(datetime_from_yyyymmdd(dossier.canton_internal_deadline)) or "-"}
                Gruppe: {dossier.canton_group or "-"}
                Gruppenbezeichnung: {dossier.canton_group_name or "-"}
                Sachbearbeiter: {dossier.canton_assignee or "-"}
                Vorläufiges Abschlussdatum: {_datetime_date_str(datetime_from_yyyymmdd(dossier.canton_provisional_closure_date)) or "-"}
                Abschlusscode: {dossier.canton_closure_code or "-"}
                Bearbeitungsdauer: {dossier.canton_processing_duration_days or "-"}
                """)
            if dossier.cantonal_status
            else None
        ),
    )

    canton_internal_deadline = CalumaAnswerWriter(
        task="cantonal-exam",
        target="kantonale-pruefung-frist",
        formatter=datetime_from_yyyymmdd,
    )

    canton_status_history = JournalWriter(
        lambda history_entry: TextWithDate(
            datetime_from_long_number(history_entry.timestamp),
            dedent(f"""\
                    {history_entry.action_text.upper()}
                    Schritt: {history_entry.step_text or "-"}
                    Wer: {history_entry.who_text or "-"}
                    Kommentar: {history_entry.comment or "-"}
                    """),
        ),
        service=_lookup_service_by_slug("afb"),
    )

    canton_comments: Optional[List[CantonComment]] = JournalWriter(
        lambda c: TextWithDate(
            datetime_from_long_number(c.timestamp),
            dedent(f"""\
                KOMMENTAR
                {c.user_id}: {c.text or "-"}
                """),
        ),
        service=_lookup_service_by_slug("afb"),
    )

    # all properties from AfB data go to this single Journal entry
    canton_usage_zones = TransformingWriter(
        delegate=JournalWriter(
            lambda journal_text: TextWithDate(timezone.now(), journal_text),
            service=_lookup_service_by_slug("afb"),
            identify_by_text_only=True,
        ),
        transform=lambda _v, dossier, _u: (
            dedent(f"""\
            AFB DATEN

            Nutzungszonen:
            {
                chr(10).join([f"• {vh.value}" for vh in dossier.canton_usage_zones])
                if dossier.canton_usage_zones
                else "-"
            }

            Schutzzonen:
            {
                chr(10).join(
                    [f"• {vh.value}" for vh in dossier.canton_protection_zones]
                )
                if dossier.canton_protection_zones
                else "-"
            }

            Kantonsstrasse betroffen: {_check(dossier.canton_cantonal_road_affected)}
            Strassen:
            {
                chr(10).join([f"• {vh.value}" for vh in dossier.canton_roads])
                if dossier.canton_roads
                else "-"
            }

            Bahnen:
            {
                chr(10).join([f"• {vh.value}" for vh in dossier.canton_railways])
                if dossier.canton_railways
                else "-"
            }

            Gewässer betroffen: {_check(dossier.canton_water_affected)}
            Gewässer:
            {
                chr(10).join([f"• {vh.value}" for vh in dossier.canton_waters])
                if dossier.canton_waters
                else "-"
            }

            Waldabstand: {_check(dossier.canton_forest_distance)}
            Sonderfall Entw.: {_check(dossier.canton_special_case_dev)}
            Grundwasserabsenkung geplant: {
                _check(dossier.canton_groundwater_lowering_planned)
            }
            AWA: {_check(dossier.canton_awa)}
            Altlasten: {_check(dossier.environmental_contaminated_site_affected)}
            Bauvorhaben im Wald: {_check(dossier.canton_construction_project_in_forest)}
            Hochwassergefährdung: {_check(dossier.canton_flood_hazard)}
            Denkmalschutz: {_check(dossier.canton_monument_protection)}
            Wanderwege: {_check(dossier.canton_hiking_trails)}
            Ortsbildschutz: {_check(dossier.canton_townscape_protection)}
            Störfallverordnung betroffen: {
                _check(dossier.canton_major_accident_ordinance_affected)
            }
            Archäologie: {_check(dossier.canton_archaeology)}
            Verkehr: {_check(dossier.canton_traffic)}
            Lärmschutz: {_check(dossier.canton_noise_protection)}
            Materialabbau: {_check(dossier.canton_material_extraction)}
            AGV: {_check(dossier.canton_agv)}
            Radwege: {_check(dossier.canton_cycle_paths)}

            Kanalisation: {dossier.canton_sewerage if dossier.canton_sewerage else "-"}
            Flächenverbrauch: {
                dossier.canton_area_consumption
                if dossier.canton_area_consumption
                else "-"
            }
            KoKo Datum: {
                _datetime_date_str(datetime_from_yyyymmdd(dossier.canton_koko_date))
                if dossier.canton_koko_date
                else "-"
            }
            KoKo-Status: {
                dossier.canton_koko_status if dossier.canton_koko_status else "-"
            }
            Beschluss Gem: {
                _datetime_date_str(
                    datetime_from_yyyymmdd(dossier.canton_municipal_decision)
                )
                if dossier.canton_municipal_decision
                else "-"
            }
            Beschluss Art: {
                dossier.canton_decision_type if dossier.canton_decision_type else "-"
            }
            Verzögerung durch: {
                dossier.canton_delay_caused_by
                if dossier.canton_delay_caused_by
                else "-"
            }
            Begründung: {
                dossier.canton_justification if dossier.canton_justification else "-"
            }
            Nachträgliches Gesuch: {_check(dossier.canton_subsequent_application)}
            """)
            if dossier.cantonal_status
            else None
        ),
    )

    canton_fees = TransformingWriter(
        delegate=JournalWriter(
            lambda fees_entry: (
                TextWithDate(timezone.now(), fees_entry) if fees_entry else None
            ),
            identify_by_text_only=True,
            service=_lookup_service_by_slug("afb"),
        ),
        transform=lambda _v, dossier, _u: (
            (
                "GEBÜHREN\n\n"
                + chr(10).join(
                    [
                        dedent(f"""\
                        Preiskondition: {fee.cost_type or "-"}
                        Beschreibung: {fee.description or "-"}
                        Schema: {fee.calculation_scheme or "-"}
                        Schemastelle: {fee.calc_scheme_position or "-"}
                        Aufgaben-ID: {fee.request_task_id or "-"}
                        Stückpreis: {fee.unit_price or "-"}
                        Menge: {fee.amount or "-"}
                        Messeinheit: {fee.msehi or "-"}
                        Gesamtpreis: {float(fee.unit_price or 0) * float(fee.amount or 0):.2f}
                        Verwenden: {_check(fee.take)}
                        Anzeigen in GV: {_check(fee.show_in_gv)}
                        Bemerkung FS: {fee.comment_fs or "-"}
                        Bemerkung AfB: {fee.comment_afb or "-"}
                        """)
                        for fee in dossier.canton_fees
                    ],
                )
            )
            if dossier.canton_fees
            else ""
        ),
    )

    canton_application_codes = CalumaAnswerWriter(
        target="kantonale-pruefung-gesuchscodes",
        task="cantonal-exam",
        formatter=lambda codes: (
            [CANTON_APPLICATION_CODES.get(code.value) for code in codes]
            if codes
            else None
        ),
    )

    cantonal_status = JournalWriter(
        lambda status: TextWithDate(
            timezone.now(),
            dedent(
                f"""\
                STATUS
                Letzter Kantonsstatus: '{status}'
                """
                if status
                else None,
            ),
        ),
        service=_lookup_service_by_slug("afb"),
        identify_by_text_only=True,
    )

    #################################################################################################
    # end of writer declarations
    #################################################################################################

    @Timer("import_dossier", logger=None)
    def import_dossier(
        self, dossier: KtAargauDossier, import_session_id: str, skip_existing=False
    ) -> DossierSummary:
        try:
            map_target_state(dossier)
            self._fix_fields(dossier)
        except Exception as e:  # pragma: no cover
            log.warning(e, exc_info=True)
            self._add_warning(MessageCodes.UNHANDLED_EXCEPTION, str(e), dossier)

        return super().import_dossier(dossier, import_session_id, skip_existing)

    def _fix_fields(self, dossier: KtAargauDossier):
        self._fix_submit_date_if_needed(dossier)

    def _fix_submit_date_if_needed(self, dossier):
        if _is_empty_or_date_before_1970(dossier.submit_date):  # pragma: no cover
            self._add_warning(
                MessageCodes.FIELD_VALIDATION_ERROR,
                f"Einreichdatum ungültig: '{dossier.submit_date}', ersetzt mit dem 01.01.1970 .",
                dossier,
            )
        dossier.submit_date = _replace_invalid_date_with_unix_epoch(
            datetime_from_yyyymmdd(dossier.submit_date)
        )

    def create_instance(self, dossier: KtAargauDossier) -> Instance:
        instance_state = InstanceState.objects.get(name=dossier._meta.target_state)
        creation_data = dict(
            instance_state=instance_state,
            previous_instance_state=instance_state,
            user=self._user,
            group=self._group,
            form=Form.objects.get(pk=settings.DOSSIER_IMPORT["FORM_ID"]),
        )

        dossier_types = dossier.dossier_types
        caluma_form_id = self._map_to_caluma_form_id(dossier_types)

        service = lookup_responsible_service(dossier.responsible_municipality, dossier)
        self.set_is_paper(dossier)

        instance = CreateInstanceLogic.create(
            creation_data,
            caluma_user=self._caluma_user,
            camac_user=self._user,
            group=service.groups.filter(role__name="municipality-lead").first(),
            caluma_form=CalumaForm.objects.get(  # noqa: F821
                pk=caluma_form_id or settings.DOSSIER_IMPORT["CALUMA_FORM"]
            ),
            start_caluma=True,
            skip_applicant_creation=True,
            is_paper=dossier.is_paper,
        )

        # only for paper dossiers the responsible service is set after creation, else only
        if not instance.responsible_service():
            InstanceService.objects.create(
                instance=instance,
                service=service,
                active=1,
                activation_date=None,
            )

        self.set_dossier_number(dossier.submit_date, instance)

        self.create_applicants_from_authorizations(dossier, instance)
        permissions_events.Trigger.instance_submitted(None, instance)

        self._create_document_status(dossier, instance)
        self._set_municipality_light_if_needed(dossier, instance)

        return instance

    def _set_municipality_light_if_needed(self, dossier, instance):
        if (
            instance
            and instance.responsible_service().service_group.name
            == "municipality-light"
        ):  # pragma: no cover
            dossier.is_municipality_light = True

    def _create_document_status(self, dossier: KtAargauDossier, instance: Instance):
        for ds in dossier.document_statuses:
            if ds.status in ["ungültig", "bewilligt"]:
                db_status, created = MigrationDocumentStatus.objects.get_or_create(
                    instance=instance,
                    dms_id=ds.dms_id,
                    dms_version=ds.dms_version if ds.dms_version is not None else "",
                    status=ds.status,
                )
                if not created:  # pragma: no cover
                    self._add_warning(
                        MessageCodes.DUPLICATE_IDENTFIER_ERROR,
                        f"Duplikater Dokumentstatus für {db_status.dms_id} und {db_status.dms_version} "
                        f"schon verhanden als {db_status.status}. Nicht gesetzter Status: {ds.status}",
                        dossier,
                    )

    def _map_to_caluma_form_id(self, dossier_types):
        actual_types = [
            f.name for f in fields(dossier_types) if getattr(dossier_types, f.name)
        ]
        # the keys in the DOSSIER_TYPE_TO_FORM_MAPPING dict are sorted by priority to map the first match
        first_matching_mapping_key = next(
            (dt for dt in DOSSIER_TYPE_TO_FORM_MAPPING if dt in actual_types),
            None,
        )
        caluma_form_id = DOSSIER_TYPE_TO_FORM_MAPPING.get(first_matching_mapping_key)
        return caluma_form_id

    def set_dossier_number(self, submit_date: Optional[datetime], instance):
        dossier_number = CreateInstanceLogic.generate_identifier(
            instance,
            submit_date.year if submit_date else None,
        )
        instance.case.meta.update(
            {
                "dossier-number": dossier_number,
                "dossier-number-sort": generate_sort_key(dossier_number),
            }
        )
        instance.case.save()

    def set_is_paper(self, dossier: KtAargauDossier):
        dossier.is_paper = True
        if any(
            auth.userid and auth.permission in ["R", "W"]
            for auth in dossier.authorizations
        ):
            dossier.is_paper = False

    def create_applicants_from_authorizations(self, dossier, instance) -> None:
        authorizations = dossier.authorizations
        user_permissions = {}

        # Build dict of userids and their permissions
        for auth in authorizations:
            if auth.userid:
                if auth.userid not in user_permissions:
                    user_permissions[auth.userid] = set()
                if auth.permission in ["R", "W"]:
                    user_permissions[auth.userid].add(auth.permission)

        # Create applicants based on permissions
        for userid, permissions in user_permissions.items():
            if permissions:
                Applicant.objects.create(
                    instance=instance,
                    user=instance.user,
                    username=userid,
                    role=ROLE_CHOICES.ADMIN.value
                    if "W" in permissions
                    else ROLE_CHOICES.READ_ONLY.value,
                )

    def _update_dossier_from_instance(self, dossier: KtAargauDossier, instance):
        dossier.caluma_form_id = instance.case.document.form.name.de
        dossier.dossier_number = instance.case.meta.get("dossier-number")
        dossier.instance_state = str(instance.instance_state)

    def find_existing_instance(self, dossier: KtAargauDossier, user: BaseUser):
        keyword = Keyword.objects.filter(
            name=dossier.id,
            service=lookup_responsible_service(
                dossier.responsible_municipality, dossier, user
            ),
        ).first()

        instance = keyword.instances.first() if keyword else None

        self._set_municipality_light_if_needed(dossier, instance)

        return instance

    def link_instance_and_dossier(
        self, instance: Instance, dossier: KtAargauDossier, user: BaseUser
    ):
        try:
            instance.keywords.create(
                name=dossier.id,
                service=instance.responsible_service(),
            )
        except IntegrityError as e:  # pragma: no cover
            log.warning(e, exc_info=True)

    def _add_warnings(self, dossier: KtAargauDossier):  # pragma: no cover
        for decicion in dossier.decisions:
            if _is_empty_or_date_before_1970(decicion.decision_date):
                self._add_warning(
                    MessageCodes.FIELD_VALIDATION_ERROR,
                    f"Verfügungsdatum ungültig: '{_datetime_date_str(decicion.decision_date)}', ersetzt mit dem 01.01.1970 .",
                    dossier,
                )

    def _add_warning(
        self, message_code: MessageCodes, detail_message: str, dossier: KtAargauDossier
    ):  # pragma: no cover
        dossier._meta.warnings.append(
            Message(
                level=Severity.WARNING,
                code=message_code,
                detail=detail_message,
            )
        )

    def write_fields(self, instance: Instance, dossier: Dossier):
        self._authorize_afb_if_needed(dossier, instance)
        super().write_fields(instance, dossier)

    def _post_write_fields(self, instance, dossier):
        self._write_triage_fields(instance)
        self._update_dossier_from_instance(dossier, instance)
        afb_service = _lookup_service_by_slug("afb")
        assign_responsible_user(instance, afb_service)
        self._add_warnings(dossier)

    def _authorize_afb_if_needed(self, dossier: KtAargauDossier, instance):
        if not dossier.cantonal_status:
            return

        dossier_context = f"'{dossier.id}' from '{dossier.city}' with cantonal status '{dossier.cantonal_status}'"

        afb_service = _lookup_service_by_slug("afb")
        if InstanceACL.objects.filter(
            instance=instance, service=afb_service
        ).exists():  # pragma: no cover
            log.info(f"AfB already authorized for dossier {dossier_context}")
            return

        _add_keyword_if_needed(dossier.id, instance, afb_service)
        _add_keyword_if_needed(dossier.cantonal_id, instance, afb_service)
        _add_keyword_if_needed(dossier.municipal_id, instance, afb_service)

        self._process_deadline_and_suspensions(instance, dossier, afb_service)

        # after the circulation is finished (i.e. it is part of PATH_TO_STATE) we just
        # add an instance ACL for AfB. We don't have to look at the case where the circulation
        # has not been started, because in this case there can not be any AfB involvement meaning
        # there can not be a cantonal status (-> early return).
        if "distribution" in PATH_TO_STATE.get(dossier._meta.target_state):
            InstanceACL.objects.create(
                instance=instance,
                service=afb_service,
                grant_type="SERVICE",
                access_level=AccessLevel.objects.get(slug="distribution-service"),
                created_by_event="inquiry-sent",
            )
            log.info(f"Granted AfB access to dossier {dossier_context}")
            return

        # start distribution and invite AfB
        try:
            distribution_case = (
                instance.case.work_items.filter(task_id="distribution")
                .first()
                .child_case
            )
            create_inquiry_work_item = distribution_case.work_items.filter(
                task_id="create-inquiry", status="ready"
            ).first()

            complete_work_item(
                create_inquiry_work_item,
                self._caluma_user,
                context={
                    "addressed_groups": [afb_service.service_id],
                    "created_at": dossier.canton_entry_date,
                },
            )

            # 2. "send actual inquiry to AfB"
            inquiry_work_item = distribution_case.work_items.filter(
                task_id="inquiry", status="suspended"
            ).first()
            resume_work_item(inquiry_work_item, self._caluma_user, None)
            log.info(f"Invited AfB to inquiry for dossier {dossier_context}")

            default_context = {
                "no-notification": True,
                "no-history": True,
                "skip": True,
            }

            # 3. if not neues Gesuch => skip "cantonal_exam"
            if dossier.cantonal_status != CantonalState.NEW:  # pragma: no cover
                cantonal_exam = instance.case.work_items.get(task_id="cantonal-exam")
                skip_work_item(
                    work_item=cantonal_exam,
                    user=self._caluma_user,
                    context=default_context,
                )
                log.info(f"Skipped cantonal exam for dossier {dossier_context}")

            # 4. if "vorläufiger Abschluss" => skip inquiry_work_item => trigger-billing wird autom. hinzugefügt
            if (
                dossier.cantonal_status == CantonalState.PROVISIONAL_COMPLETION
            ):  # pragma: no cover
                skip_work_item(
                    work_item=inquiry_work_item,
                    user=self._caluma_user,
                    context=default_context,
                )
                log.info(f"Skipped inquiry for dossier {dossier_context}")

            # 5. "Sistiert" => suspensions

            # 6. "Definitiver Abschluss" oder "Zurückgewiesen" => skip inquiry_work_item und dann "trigger-billing"
            if dossier.cantonal_status in [
                CantonalState.DEFINITIVE_COMPLETION,
                CantonalState.REJECTED,
            ]:  # pragma: no cover
                skip_work_item(
                    work_item=inquiry_work_item,
                    user=self._caluma_user,
                    context=default_context,
                )
                log.info(f"Skipped inquiry for dossier {dossier_context}")
                trigger_billing = distribution_case.work_items.get(
                    task_id="trigger-billing"
                )
                skip_work_item(
                    work_item=trigger_billing,
                    user=self._caluma_user,
                    context=default_context,
                )
                log.info(f"Skipped billing for dossier {dossier_context}")

        except Exception as e:  # pragma: no cover
            log.warning(e, exc_info=True)
            self._add_warning(
                MessageCodes.INCONSISTENT_WORKFLOW_STATE,
                _(
                    "Error when inviting AfB and preparation of appropriate tasks: %(error)s."
                )
                % {"error": e},
                dossier,
            )

    def _process_deadline_and_suspensions(
        self, instance, dossier: KtAargauDossier, afb_service
    ):
        if not dossier.canton_entry_date:  # pragma: no cover
            return

        deadline_start = date_from_yyyymmdd(dossier.canton_entry_date)
        deadline_end = date_from_yyyymmdd(dossier.canton_provisional_closure_date)

        if InstanceDeadline.objects.filter(
            instance=instance,
            service=afb_service,
            start_date=deadline_start,
        ).exists():  # pragma: no cover
            log.info(f"Deadline already set for dossier {dossier.id}")
            return

        deadline = InstanceDeadline.objects.create(
            instance=instance,
            service=afb_service,
            start_date=deadline_start,
            deadline_type=DeadlineType.objects.get_default(afb_service, instance),
            process_deadline_date=deadline_end,
            process_deadline_date_override=bool(deadline_end),
        )

        for susp in dossier.canton_suspensions:
            deadline.suspensions.create(
                start_date=datetime_from_yyyymmdd(susp.start_date),
                end_date=datetime_from_yyyymmdd(susp.resume_date),
                created_at=datetime_from_yyyymmdd(susp.creation_date),
                reason_text=(f"{susp.reason}\nVorheriger Status: {susp.prev_status}\n")
                + (f"Bemerkung: {susp.note}" if susp.note else ""),
            )

        deadline.recalculate_progression()

    def _write_triage_fields(self, instance: Instance):
        """Write triage answers for personal data.

        The table questions for landowner, project author, ... are only displayed
        if the associated multi-choice question is answered with the additional person types .
        This method checks if there is any data in the personal table and adds the answer to the triage question
         accordingly.
        """

        answers = []
        for table_question, answer_option in [
            ("personalien-grundeigentumerin", "weitere-personen-grundeigentumerin"),
            ("personalien-projektverfasserin", "weitere-personen-projektverfasserin"),
            ("vertreterin-mit-vollmacht", "weitere-personen-vertreterin-mit-vollmacht"),
            ("personalien-rechnungsempfaenger", "weitere-personen-rechnungsempfaenger"),
        ]:
            table_answer = instance.case.document.answers.filter(
                question_id=table_question
            ).first()
            has_rows = table_answer.documents.exists() if table_answer else False
            if has_rows:
                answers.append(answer_option)

        form_api.save_answer(  # noqa: F821
            document=instance.case.document,
            question=Question.objects.get(pk="weitere-personen"),
            value=answers,
            user=self._caluma_user,
        )

    def _set_workflow_state(
        self, instance: Instance, dossier: KtAargauDossier
    ) -> List[Message]:
        messages = []
        target_state = dossier._meta.target_state

        default_context = {"no-notification": True, "no-history": True, "skip": True}

        # In order for a work item to be completed no sibling work items can be
        # in state ready. They have to be dealt with in advance.
        for task_id in PATH_TO_STATE.get(target_state):
            try:
                work_item = instance.case.work_items.get(task_id=task_id)
            except WorkItem.DoesNotExist as e:  # pragma: no cover
                # init-construction-monitoring might not exist, if there was no or a negative decision
                # formal-examl might not exist, if it is a municipality-light
                if task_id == "init-construction-monitoring" or (
                    task_id == "formal-exam" and dossier.is_municipality_light
                ):
                    continue

                messages.append(
                    Message(
                        level=Severity.ERROR.value,
                        code=MessageCodes.WORKFLOW_SKIP_ITEM_FAILED.value,
                        detail=_(
                            "Skip work item with task_id %(task_id)s failed with %(error)s."
                        )
                        % {
                            "task_id": task_id,
                            "error": DossierWriter.ConfigurationError(e),
                        },
                    )
                )
                continue

            # the decission form already has been written in the mapping of the KtAargauDossierWriter.decisions field
            # => only trigger decision_decreed
            if task_id == "decision" and dossier.decisions:
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

            skip_work_item(work_item, user=self._caluma_user, context=default_context)

        messages.append(  # pragma: no cover
            Message(
                level=Severity.DEBUG.value,
                code=MessageCodes.SET_WORKFLOW_STATE.value,
                detail=_("Workflow state set to %(state)s.") % {"state": target_state},
            )
        )

        return messages
