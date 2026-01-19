import base64
import copy
from abc import ABC, abstractmethod
from io import BytesIO
from itertools import chain
from typing import Literal

import qrcode
from alexandria.core import models as alexandria_models
from caluma.caluma_form.models import Answer, AnswerDocument, Document, Question
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.db.models import Exists, OuterRef, Q, Sum
from django.db.models.fields.files import ImageFieldFile
from django.utils import timezone
from django.utils.timezone import get_current_timezone
from django.utils.translation import get_language, gettext, gettext_noop as _
from PIL import Image
from rest_framework import serializers

from camac.alexandria.extensions.visibilities import (
    CustomVisibility as CustomAlexandriaVisibility,
)
from camac.billing.models import BillingV2Entry
from camac.caluma.models import Inquiry
from camac.caluma.utils import (
    find_answer,
    work_item_by_addressed_service_condition,
)
from camac.core.translations import get_translations_canton_aware
from camac.tags.models import Keyword
from camac.user.models import Service, User
from camac.utils import build_url, clean_join, get_dict_item

from .utils import (
    clean_and_add_full_name,
    get_person_address_1,
    get_person_address_2,
    get_person_first_name,
    get_person_last_name,
    get_person_name,
    human_readable_date,
    parse_person_row,
    row_to_person,
    to_configured_case,
)


class AliasedMixin:
    """
    DRF serializer field mixin for handling aliased placeholders.

    Aliases are generally translated and can be used to access the same field
    under different names in the respective language.

    Nested aliases are used to access fields of nested objects.
    """

    def __init__(
        self,
        aliases: list[str] | None = None,
        nested_aliases: dict[str, list[str]] | None = None,
        description: str = None,
        is_collection: bool = False,
        *args,
        **kwargs,
    ):
        """Initialize DRF field for aliased placeholder fields.

        Parameters:
        aliases (list | None): A list of aliases for the field.
        nested_aliases (dict[str, list[str]] | None): A dictionary of
            aliases for the fields objects' attribute names. Double nesting is supported
            by dot path notation.

            Example:
            {
                # single nesting
                'attr1': ['attr1_alias1', 'attr1_alias2'],
                # double nesting
                'attr2.attr1': ['attr1_alias1', 'attr1_alias2'],
                'attr2.attr2': ['attr2_alias1']
                }
            }

        description (str | None): Description displayed in user facing docs.
        is_collection (bool): Whether the field is a collection of values. Collections
            should be iterated over when used in templates and the docs should indicate
            this by suffixing the placeholder with `[]`. E. g. `some_list_of_values[]`.
            `is_collection` is set to True if at least one nested alias is provided.
        """
        super().__init__(*args, **kwargs)
        self._aliases = aliases or []
        self._nested_aliases = nested_aliases or {}
        self.description = description
        self.is_collection = is_collection or len(self._nested_aliases) > 0

    @property
    def aliases(self):
        return sorted(self._aliases)

    @property
    def nested_aliases(self):
        return self._nested_aliases

    @staticmethod
    def _get_alias_translations(
        alias: str | dict[Literal["default", *settings.APPLICATIONS.keys()], str],
        flat: bool = False,
    ) -> dict[Literal[*dict(settings.LANGUAGES).keys()], str] | list[str]:
        """Return alias' translations for available languages.

        Parameters:
            alias (str | dict): A simple str argument is translated for each language.
                If a dict is provided the "default" value of the dict is returned
                unless an override is configured in the current APPLICATION setting.
            flat (bool): return all aliases and translations in one list.

        Example:
        {
          "de": "EIN_PLATZHALER",
          "fr": "NIMPORTE_JOKER"
        }

        Nested example:
        [
            "de": "EIN_NEST.NAME"
            "fr": "UN_NIDS.NOM"
        ]


        """
        if flat:
            return set(
                [
                    to_configured_case(alias_t)
                    for alias_t in get_translations_canton_aware(alias).values()
                ]
            )

        return {
            lang: to_configured_case(alias_t)
            for lang, alias_t in get_translations_canton_aware(alias).items()
        }

    def get_docs(
        self,
    ) -> dict[Literal["aliases", "nested_aliases", "description"], list | dict]:
        """Create a dictionary of field docs for every available language."""
        return {
            "aliases": [self._get_alias_translations(alias) for alias in self.aliases],
            "nested_aliases": {
                nested_name: [
                    self._get_alias_translations(nested_alias)
                    for nested_alias in nested_aliases
                ]
                for nested_name, nested_aliases in self.nested_aliases.items()
            },
            "description": (
                get_translations_canton_aware(self.description)
                if self.description
                else None
            ),
        }

    def make_placeholders(self):
        """
        Create a flat list of every aliased placeholder available.

        Every placeholder is present as the literal name. Additionally
        for collections of literals or objects the trailing [] is
        added.

        | type               | description     | example name    |
        |--------------------|-----------------|-----------------|
        | Literal (default)  | int, float, str | SOME_NAME       |
        | Collection         | list, tuple     | SOME_COLL[]     |
        | Object collection  | list of dicts   | OBJECTS[].ATTR1 |

        The placeholder aliases are translated to every available language.

        Aliasing of nested object attribute names is supported (1 level deep)

        """

        # first make sure all placeholders are present
        available_placeholders = set(
            [
                translated_alias
                for translated_alias in chain(
                    *[
                        self._get_alias_translations(alias, flat=True)
                        for alias in self.aliases
                    ]
                )
            ]
        )

        # add collections with a trailing []
        if self.is_collection or len(self.nested_aliases):
            available_placeholders.update(
                [
                    f"{translated_alias}[]"
                    for translated_alias in chain(
                        *[
                            self._get_alias_translations(alias, flat=True)
                            for alias in self.aliases
                        ]
                    )
                ]
            )

        if not self.nested_aliases:
            return sorted(available_placeholders)

        names = copy.copy(available_placeholders)
        nested_names = set()
        for alias in names:
            # NOTE: Nested aliases like `nested.prefix.alias` are only added
            # added in their addition to `nested[].prefix[].alias`
            if not alias.endswith("]"):
                continue

            nested_base = alias
            nested_names.add(nested_base)
            for nested_name, nested_aliases_list in self.nested_aliases.items():
                nested_aliases_t = chain(
                    *[
                        self._get_alias_translations(alias).values()
                        for alias in nested_aliases_list
                    ]
                )
                base_prefix = nested_base

                if "." in nested_name:
                    # NOTE: The middle part of the nested placeholder is not translated
                    prefix, nested_name = nested_name.split(".")
                    base_prefix = f"{nested_base}.{prefix}[]"

                    nested_names.add(base_prefix)

                nested_names.update(
                    [f"{base_prefix}.{alias}" for alias in nested_aliases_t]
                )

                available_placeholders.update(nested_names)

        return sorted(available_placeholders)


class AliasedIntegerField(AliasedMixin, serializers.IntegerField):
    pass


class AliasedMethodField(AliasedMixin, serializers.SerializerMethodField):
    pass


class DeprecatedField(AliasedMixin, serializers.ReadOnlyField):
    def __init__(self, value=None, **kwargs):
        super().__init__(**kwargs)

        self.value = value

    def get_attribute(self, instance):
        return self.value


class ServiceField(ABC, AliasedMixin, serializers.ReadOnlyField):
    def __init__(
        self,
        source_args=[],
        remove_name_prefix=False,
        add_municipality_prefix=False,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.source_args = source_args
        self.remove_name_prefix = remove_name_prefix
        self.add_municipality_prefix = add_municipality_prefix

    @abstractmethod
    def get_service(instance):  # pragma: no cover
        ...

    def to_representation(self, value):
        value = super().to_representation(value)

        if isinstance(value, ImageFieldFile):
            if not value:  # pragma: no cover
                return None

            data = BytesIO(value.file.read())
            img = Image.open(data)
            img.save(data, "PNG")
            data_b64 = base64.b64encode(data.getvalue())
            return f"data:image/png;base64,{data_b64.decode('utf-8')}"

        if value and self.remove_name_prefix:
            # Municipalities and districts in BE all have a prefix which is
            # sometimes unwanted in certain placeholder.
            for prefix in [
                gettext("Authority"),
                gettext("Municipality"),
                gettext("District"),
                gettext("GBB"),
            ]:
                value = value.replace(prefix, "").strip()

        if value and self.add_municipality_prefix:
            value = clean_join(gettext("Municipality"), value)

        return value

    def get_attribute(self, instance):
        service = self.get_service(instance)
        value = getattr(service, self.source) if service else None
        return value(*self.source_args) if callable(value) else value


class MunicipalityField(ServiceField):
    def get_service(self, instance):
        return instance.municipality


class CurrentServiceField(ServiceField):
    def get_service(self, instance):
        return self.context["request"].group.service


class ResponsibleServiceField(ServiceField):
    def get_service(self, instance):
        return instance.responsible_service(filter_type="municipality")


class UserField(ABC, AliasedMixin, serializers.ReadOnlyField):
    @abstractmethod
    def get_user(instance):  # pragma: no cover
        ...

    def get_attribute(self, instance):
        user = self.get_user(instance)

        if not user:  # pragma: no cover
            return ""

        if self.source == "full_name":
            return clean_join(user.name, user.surname)

        return getattr(user, self.source)


class ResponsibleUserField(UserField):
    def get_user(self, instance):
        responsible_service = instance.responsible_services.filter(
            service=self.context["request"].group.service
        ).first()

        return responsible_service.responsible_user if responsible_service else None


class CurrentUserField(UserField):
    def get_user(self, instance):
        return self.context["request"].user


class BillingEntriesField(AliasedMixin, serializers.ReadOnlyField):
    def __init__(self, own=False, total=False, only_not_charged=False, **kwargs):
        super().__init__(**kwargs)

        self.own = own
        self.total = total
        self.only_not_charged = only_not_charged

    @property
    def nested_aliases(self):
        if self.total:
            return {}

        nested_aliases = {
            "POSITION": [_("BILLING_ENTRY_POSITION")],
            "BETRAG": [_("BILLING_ENTRY_AMOUNT")],
            "RECHTSGRUNDLAGE": [_("BILLING_ENTRY_LEGAL_BASIS")],
            "KOSTENSTELLE": [_("BILLING_ENTRY_COST_CENTER")],
            "STUNDEN": [_("BILLING_ENTRY_HOURS")],
            "STUNDENSATZ": [_("BILLING_ENTRY_HOURLY_RATE")],
            "ANTEIL_PROZENT": [_("BILLING_ENTRY_PERCENTAGE")],
            "GESAMTKOSTEN": [_("BILLING_ENTRY_TOTAL_COST")],
            "BERECHNUNG": [_("BILLING_ENTRY_CALCULATION")],
            "MEHRWERTSTEUER": [_("BILLING_ENTRY_VAT")],
            "ART": [_("BILLING_ENTRY_TYPE")],
            "VERRECHNUNG": [_("BILLING_ENTRY_BILLING_TYPE")],
            "VERRECHNET_AM": [_("BILLING_ENTRY_CHARGED_AT")],
            "BEMERKUNG": [_("BILLING_ENTRY_REMARK")],
            "ORGANISATION": [_("BILLING_ENTRY_ORGANISATION")],
        }

        return {
            k: v
            for k, v in nested_aliases.items()
            if k in settings.PLACEHOLDERS["BILLING_ENTRY_FIELDS"]
        }

    def format_rate(self, value):
        if value is None:
            return ""
        return f"{value:,.2f}".replace(",", "’")

    def to_representation(self, value):
        if self.total:
            return self.format_rate(
                value.aggregate(Sum("final_rate")).get("final_rate__sum")
                if value
                else 0
            )

        data = []

        for entry in value:
            data.append(
                {
                    field_name: self.get_entry_field(entry, field_name)
                    for field_name in settings.PLACEHOLDERS["BILLING_ENTRY_FIELDS"]
                }
            )

        return data

    def get_entry_field(self, entry, field_name):  # noqa: C901
        match field_name:
            case "POSITION":
                return entry.text
            case "BETRAG":
                return self.format_rate(entry.final_rate)
            case "RECHTSGRUNDLAGE":
                return entry.legal_basis
            case "KOSTENSTELLE":
                return entry.cost_center
            case "STUNDEN":
                return entry.hours
            case "STUNDENSATZ":
                return self.format_rate(entry.hourly_rate)
            case "ANTEIL_PROZENT":
                return entry.percentage
            case "GESAMTKOSTEN":
                return self.format_rate(entry.total_cost)
            case "BERECHNUNG":
                return self.get_choice_label(
                    BillingV2Entry.CalculationModes.choices, entry.calculation
                )
            case "MEHRWERTSTEUER":
                match entry.tax_mode:
                    case BillingV2Entry.TaxModes.TAX_MODE_EXEMPT:
                        return self.get_choice_label(
                            BillingV2Entry.TaxModes.choices, entry.tax_mode
                        )
                    case _:
                        translation_map = {
                            BillingV2Entry.TaxModes.TAX_MODE_INCLUSIVE: gettext(
                                "inclusive_short"
                            ),
                            BillingV2Entry.TaxModes.TAX_MODE_EXCLUSIVE: gettext(
                                "exclusive_short"
                            ),
                        }
                        tax_mode = self.get_choice_label(
                            BillingV2Entry.TaxModes.choices, entry.tax_mode
                        )

                        if entry.tax_mode in [
                            BillingV2Entry.TaxModes.TAX_MODE_INCLUSIVE,
                            BillingV2Entry.TaxModes.TAX_MODE_EXCLUSIVE,
                        ]:
                            tax_mode = translation_map.get(entry.tax_mode)

                        return gettext("%(tax_mode)s %(tax_rate)s%% VAT") % {
                            "tax_mode": tax_mode,
                            "tax_rate": entry.tax_rate.normalize(),
                        }
            case "ART":
                return self.get_choice_label(
                    BillingV2Entry.Organizations.choices, entry.organization
                )
            case "VERRECHNUNG":
                return self.get_choice_label(
                    BillingV2Entry.BillingTypes.choices, entry.billing_type
                )
            case "VERRECHNET_AM":
                return human_readable_date(entry.date_charged)
            case "BEMERKUNG":
                return entry.remark
            case "ORGANISATION":
                return (
                    entry.group.service.get_name()
                    if entry.group.service
                    else entry.group.get_name()
                )
            case _:  # pragma: no cover
                return None

    def get_choice_label(self, choices, value):
        for choice in choices:
            if choice[0] == value:
                return choice[1]

    def get_attribute(self, instance):
        service = self.context["request"].group.service

        queryset = BillingV2Entry.objects.visible_for(service).filter(instance=instance)

        if self.own:
            queryset = queryset.filter(group__service=service)

        if self.only_not_charged:
            queryset = queryset.filter(date_charged__isnull=True)

        return queryset.order_by("organization", "pk")


class PublicationField(AliasedMixin, serializers.ReadOnlyField):
    def __init__(
        self,
        value_key="value",
        parser=lambda value: value,
        only_own=True,
        all_publications=False,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.value_key = value_key
        self.parser = parser
        self.only_own = only_own
        self.all_publications = all_publications

    def to_representation(self, value):
        return self.parser(super().to_representation(value))

    def get_attribute(self, instance):
        work_items = instance.case.work_items.filter(
            task_id="fill-publication",
            status=WorkItem.STATUS_COMPLETED,
            **{"meta__is-published": True},
        )

        if self.only_own:
            work_items = work_items.filter(
                addressed_groups=[str(self.context["request"].group.service_id)]
            )

        if self.all_publications:
            return self.get_all_publications(work_items)

        work_item = work_items.order_by("-created_at").first()

        answer = (
            work_item.document.answers.filter(question_id=self.source).first()
            if work_item
            else None
        )

        return getattr(answer, self.value_key, "") if answer else ""

    def get_all_publications(self, work_items):
        parsed_work_items = []
        for work_item in work_items.order_by("-created_at"):
            parsed_work_item = {}
            for answer in work_item.document.answers.all():
                question = answer.question
                value = answer.value
                if question.pk == "publikation-organ":
                    value = [
                        {
                            "NAME": str(option.label),
                            "EMAIL": option.meta.get("email"),
                        }
                        for option in answer.selected_options
                    ]
                elif question.type == "date":
                    value = human_readable_date(answer.date)

                question_alias = question.pk.upper().replace("-", "_")
                parsed_work_item[question_alias] = value
            parsed_work_items.append(parsed_work_item)

        return parsed_work_items


class MasterDataField(AliasedMixin, serializers.ReadOnlyField):
    def __init__(
        self,
        join_by=None,
        sum_by=None,
        parser=lambda value: value,
        fallback_source=None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.join_by = join_by
        self.sum_by = sum_by
        self.parser = parser
        self.fallback_source = fallback_source

    def to_representation(self, value):
        if self.join_by and isinstance(value, list):
            return clean_join(*[self.parser(v) for v in value], separator=self.join_by)
        if self.sum_by and isinstance(value, list):

            def parse(v):
                try:
                    return int(v.get(self.sum_by))
                except (TypeError, ValueError):  # pragma: no cover
                    return None

            parsed_values = list(filter(None, [parse(v) for v in value]))

            return sum(parsed_values) if len(parsed_values) else ""
        return self.parser(super().to_representation(value))

    def _get_attribute(self, instance, source):
        if not get_dict_item(
            settings.MASTER_DATA, f"CONFIG.{source}", default=None
        ):  # pragma: no cover
            return None

        return getattr(instance._master_data, source)

    def get_attribute(self, instance):
        value = self._get_attribute(instance, self.source)

        if value in [None, []] and self.fallback_source is not None:
            value = self._get_attribute(instance, self.fallback_source)

        return value


class JointField(AliasedMixin, serializers.ReadOnlyField):
    def __init__(self, fields=[], separator=" ", **kwargs):
        super().__init__(**kwargs)

        self.fields = fields
        self.separator = separator

        for field in self.fields:
            field.bind(field_name="", parent=self)

    def get_attribute(self, instance):
        return clean_join(
            *[
                field.to_representation(field.get_attribute(instance))
                for field in self.fields
            ],
            separator=self.separator,
        )


class InquiriesField(AliasedMixin, serializers.ReadOnlyField):
    def __init__(
        self,
        only_own=False,
        only_own_controlling=None,
        props=None,
        join_by=None,
        service_group=None,
        status=None,
        **kwargs,
    ):
        if not props:
            props = settings.PLACEHOLDERS.get("INQUIRY_DEFAULT_FIELDS", [])

        all_nested_aliases = {
            "ANTWORT": [_("ANSWER")],
            "SACHBEARBEITUNG_ENTSCHEID": [_("CLERK_DECISION")],
            "BEANTWORTET": [_("ANSWERED")],
            "BEANTWORTET_TIMESTAMP": [_("ANSWERED_TIMESTAMP")],
            "ERSTELLT": [_("CREATED")],
            "ERSTELLT_TIMESTAMP": [_("CREATED_TIMESTAMP")],
            "FACHSTELLE": [_("SERVICE")],
            "FRIST": [_("DEADLINE")],
            "NAME": [_("NAME")],
            "BESCHREIBUNG": [_("DESCRIPTION")],
            "NEBENBESTIMMUNGEN": [_("ANCILLARY_CLAUSES")],
            "STELLUNGNAHME": [_("OPINION")],
            "TEXT": [_("TEXT")],
            "VON": [_("BY")],
            "RUECKMELDUNG_FAZIT": [_("FEEDBACK_CONCLUSION")],
            "ZUSTIMMENDE_BEURTEILUNGEN": [_("APPROVING_ASSESSMENTS")],
            "ABLEHNENDE_BEURTEILUNGEN": [_("REJECTING_ASSESSMENTS")],
            "NACHFORDERUNG": [_("ADDITIONAL_DEMAND")],
            "EINSPRACHEN": [_("OBJECTIONS")],
            "HINWEISE_AN_GESUCHSTELLERIN": [_("NOTES_TO_APPLICANT")],
            "HINWEISE_AN_LEITBEHOERDE": [_("NOTES_TO_AUTHORITY")],
            "HINWEISE_AN_LEITBEHOERDE_ARP": [_("NOTES_TO_AUTHORITY_ARP")],
            "VERSAND_ENTSCHEID_WEITERE_STELLEN": [
                _("DISPATCH_DECISION_FURTHER_SERVICES")
            ],
            "BEMERKUNGEN": [_("REMARKS")],
            "DATUM_START": [_("DATE_START")],
            "DATUM_ENDE": [_("DATE_END")],
            "SACHVERHALT": [_("SITUATION")],
            "ERWAEGUNGEN": [_("CONSIDERATIONS")],
            "BEURTEILUNG": [_("STATEMENT")],
        }

        nested_aliases = (
            {key: all_nested_aliases[key] for _, key in props}
            if all([isinstance(prop, tuple) for prop in props])
            else {}
        )

        super().__init__(nested_aliases=nested_aliases, **kwargs)

        self.only_own = only_own
        self.props = props
        self.join_by = join_by
        self.service_group = service_group
        self.only_own_controlling = only_own_controlling
        self.status = status

    def get_service(self, inquiry, type):
        return Service.objects.get(pk=int(getattr(inquiry, type)[0])).get_name()

    def get_service_description(self, inquiry, type):
        return Service.objects.get(pk=int(getattr(inquiry, type)[0])).get_description()

    def get_prop_key(self, prop):
        return prop[1] if isinstance(prop, tuple) else prop

    def get_prop_value(self, inquiry, prop):
        prop_mapping = {
            "service": lambda i: self.get_service(i, "addressed_groups"),
            "service_description": lambda i: self.get_service_description(
                i, "addressed_groups"
            ),
            "service_with_prefix": lambda i: f"- {self.get_service(i, 'addressed_groups')}",
            "deadline": lambda i: i.deadline.strftime("%d.%m.%Y"),
            "creation_date": lambda i: i.created_at.strftime("%d.%m.%Y"),
            "creation_date_timestamp": lambda i: i.created_at.astimezone(
                timezone.get_default_timezone()
            ).isoformat(),
            "completion_date": lambda i: (
                i.closed_at.strftime("%d.%m.%Y")
                if i.status == WorkItem.STATUS_COMPLETED
                else None
            ),
            "completion_date_timestamp": lambda i: (
                i.closed_at.astimezone(timezone.get_default_timezone()).isoformat()
                if i.status == WorkItem.STATUS_COMPLETED
                else None
            ),
            "start_date": lambda i: i.case.parent_work_item.created_at.strftime(
                "%d.%m.%Y"
            ),
            "end_date": lambda i: (
                i.case.parent_work_item.closed_at.strftime("%d.%m.%Y")
                if i.case.parent_work_item.status == WorkItem.STATUS_COMPLETED
                else None
            ),
        }

        if isinstance(prop, tuple):
            prop = prop[0]

        answer_type, slug = settings.PLACEHOLDERS["INQUIRY_FIELD_MAPPINGS"].get(
            prop, (None, None)
        )

        if answer_type == "inquiry":
            return find_answer(
                inquiry.document, settings.DISTRIBUTION["QUESTIONS"][slug]
            )
        elif answer_type == "inquiry-answer":
            return (
                find_answer(
                    inquiry.child_case.document,
                    settings.DISTRIBUTION["QUESTIONS"][slug],
                )
                if inquiry.child_case is not None
                else None
            )

        try:
            return prop_mapping.get(prop)(inquiry)
        except AttributeError:
            # child_case and deadline may be None on draft inquiries
            return ""

    def to_representation(self, value):
        mapped = [
            {
                self.get_prop_key(prop): self.get_prop_value(inquiry, prop)
                for prop in self.props
            }
            for inquiry in value
        ]

        if self.join_by:
            return clean_join(
                *[i.get(self.props[0]) for i in mapped], separator=self.join_by
            )

        return mapped

    def get_attribute(self, instance):
        service = self.context["request"].group.service

        if not service:  # pragma: no cover
            return None

        queryset = Inquiry.objects.for_instance(instance).for_status(
            *(
                [self.status]
                if self.status
                else [
                    WorkItem.STATUS_READY,
                    WorkItem.STATUS_COMPLETED,
                    WorkItem.STATUS_SUSPENDED,
                    WorkItem.STATUS_SKIPPED,
                ]
            ),
        )

        if self.only_own:
            queryset = queryset.exclude(status=WorkItem.STATUS_SUSPENDED).filter(
                addressed_groups__contains=[str(service.pk)]
            )
        elif self.only_own_controlling:
            queryset = queryset.filter(controlling_groups__contains=[str(service.pk)])
        else:
            # if we're not filtering based on addressed / controlling groups, make sure that addressed
            # service exists
            # TODO: do we really need this?!
            queryset = queryset.filter(
                work_item_by_addressed_service_condition(
                    Q(service_parent__isnull=True) | Q(service_parent_id=service.pk)
                )
            )

        if self.service_group:
            service_groups = self.service_group

            if not isinstance(service_groups, list):
                service_groups = [service_groups]

            queryset = queryset.filter(
                work_item_by_addressed_service_condition(
                    Q(service_group__name__in=service_groups)
                )
            )

        return queryset.order_by("created_at")


class LegalSubmissionField(AliasedMixin, serializers.ReadOnlyField):
    def __init__(self, type=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.type = type

    @property
    def nested_aliases(self):
        if settings.APPLICATION_NAME == "kt_so":
            return {
                "DATUM_POSTSTEMPEL": [_("DATE_POSTMARK")],
                "EINSPRECHER_NAME": [_("OPPOSING_NAME")],
                "EINSPRECHER_ADRESSE": [_("OPPOSING_ADDRESS")],
                "EINSPRECHER_ANREDE": [_("OPPOSING_SALUTATION")],
                "ALLE_EINSPRECHENDEN": [_("ALL_OPPOSING")],
                **{
                    f"ALLE_EINSPRECHENDEN.{k}": v
                    for k, v in MasterDataPersonObjectField.nested_aliases.items()
                },
            }

        nested_aliases = {
            "DATUM_DOKUMENT": [_("DATE_DOCUMENT")],
            "DATUM_EINGANG": [_("DATE_RECEIPT")],
            "RECHTSBEGEHRENDE": [_("LEGAL_CLAIMANTS")],
            "TITEL": [_("TITLE")],
        }

        if self.type == "legal-submission-type-objection":
            nested_aliases["RUEGEPUNKTE"] = [_("REPRIMANDS")]
        else:
            nested_aliases["ANLIEGEN"] = [_("REQUEST"), _("CONCERN")]

        return nested_aliases

    def to_representation(self, value):
        data = []

        for document in value:
            legal_claimants = []

            for claimant in find_answer(
                document,
                settings.PLACEHOLDERS["LEGAL_SUBMISSIONS"][
                    "LEGAL_CLAIMANTS_TABLE_QUESTION"
                ],
            ):
                legal_claimants.append(row_to_person(claimant))

            if settings.APPLICATION_NAME == "kt_bern":
                legal_submission = {
                    "DATUM_EINGANG": find_answer(
                        document, "legal-submission-receipt-date"
                    ),
                    "DATUM_DOKUMENT": find_answer(
                        document, "legal-submission-document-date"
                    ),
                    "TITEL": find_answer(document, "legal-submission-title"),
                    "RECHTSBEGEHRENDE": clean_join(
                        *[get_person_name(person) for person in legal_claimants],
                        separator=", ",
                    ),
                }
            elif settings.APPLICATION_NAME == "kt_so":
                legal_submission = {
                    "DATUM_POSTSTEMPEL": find_answer(document, "einsprache-datum"),
                    "EINSPRECHER_NAME": get_person_name(legal_claimants[0])
                    if len(legal_claimants)
                    else None,
                    "EINSPRECHER_ADRESSE": clean_join(
                        get_person_address_1(legal_claimants[0]),
                        get_person_address_2(legal_claimants[0]),
                        separator=", ",
                    )
                    if len(legal_claimants)
                    else None,
                    "EINSPRECHER_ANREDE": legal_claimants[0].get("salutation")
                    if len(legal_claimants)
                    else None,
                    "ALLE_EINSPRECHENDEN": [
                        parse_person_row(
                            person,
                            MasterDataPersonObjectField.nested_aliases.keys(),
                        )
                        for person in legal_claimants
                    ],
                }

            if self.type == "legal-submission-type-objection":
                legal_submission["RUEGEPUNKTE"] = find_answer(
                    document, "legal-submission-reprimands"
                )
            elif self.type == "legal-submission-type-load-compensation-request":
                legal_submission["ANLIEGEN"] = find_answer(
                    document, "legal-submission-request-load-compensation-request"
                )
            elif self.type == "legal-submission-type-legal-custody":
                legal_submission["ANLIEGEN"] = find_answer(
                    document, "legal-submission-request-legal-custody"
                )

            data.append(legal_submission)

        return data

    def get_attribute(self, instance):
        queryset = Document.objects.filter(
            form_id=settings.PLACEHOLDERS["LEGAL_SUBMISSIONS"]["FORM"],
            family__work_item__case__instance=instance,
        )

        if self.type:
            queryset = queryset.filter(
                Exists(
                    Answer.objects.filter(
                        question_id="legal-submission-type",
                        value__contains=self.type,
                        document_id=OuterRef("pk"),
                    )
                )
            )

        return queryset.prefetch_related("answers").order_by("-answerdocument__sort")


class LegalClaimantsField(AliasedMixin, serializers.ReadOnlyField):
    def __init__(self, type=None, *args, **kwargs):
        super().__init__(
            nested_aliases={"ADDRESS": [_("ADDRESS")], "NAME": [_("NAME")]},
            *args,
            **kwargs,
        )

        self.type = type

    def to_representation(self, value):
        data = []

        for claimant in value:
            serialized = clean_and_add_full_name(row_to_person(claimant))

            data.append(
                {
                    "ADDRESS": serialized["full_address"],
                    "NAME": serialized["full_name"],
                }
            )

        return data

    def get_attribute(self, instance):
        legal_submissions = Document.objects.filter(
            form_id=settings.PLACEHOLDERS["LEGAL_SUBMISSIONS"]["FORM"],
            family__work_item__case__instance=instance,
        )

        if self.type:
            legal_submissions = legal_submissions.filter(
                Exists(
                    Answer.objects.filter(
                        question_id="legal-submission-type",
                        value__contains=self.type,
                        document_id=OuterRef("pk"),
                    )
                )
            )

        return Document.objects.filter(
            pk__in=AnswerDocument.objects.filter(
                answer__document__in=legal_submissions,
                answer__question_id=settings.PLACEHOLDERS["LEGAL_SUBMISSIONS"][
                    "LEGAL_CLAIMANTS_TABLE_QUESTION"
                ],
            ).values("document")
        ).order_by("created_at")


class MasterDataPersonField(MasterDataField):
    def __init__(
        self,
        only_first=False,
        use_representative=False,
        fields=["juristic_name", "name"],
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.only_first = only_first
        self.use_representative = use_representative
        self.fields = (
            ["juristic_name", "name", "address_1", "address_2"]
            if fields == "__all__"
            else fields
        )

    def parse_row(self, row):
        has_representative = row.get("has_representative", False)

        if self.use_representative and not has_representative:
            return ""

        return clean_join(
            *[
                *self._parse_row_name_parts(row),
                *self._parse_row_address_parts(row),
                *self._parse_row_extra_parts(row),
            ],
            separator=", ",
        )

    def _parse_row_name_parts(self, row):
        parts = []

        if "salutation" in self.fields:
            parts.append(row.get("salutation"))

        if "juristic_name" in self.fields:
            parts.append(
                get_person_name(
                    row,
                    include_name=False,
                    include_juristic_name=True,
                    use_representative=self.use_representative,
                )
            )

        if "name" in self.fields:
            parts.append(
                get_person_name(
                    row,
                    include_name=True,
                    include_juristic_name=False,
                    use_representative=self.use_representative,
                )
            )

        if "first_name" in self.fields:
            parts.append(
                get_person_first_name(
                    row,
                    use_representative=self.use_representative,
                )
            )

        if "last_name" in self.fields:
            parts.append(
                get_person_last_name(
                    row,
                    use_representative=self.use_representative,
                )
            )

        return parts

    def _parse_row_address_parts(self, row):
        parts = []
        if "address_1" in self.fields:
            parts.append(
                get_person_address_1(
                    row,
                    use_representative=self.use_representative,
                )
            )

        if "address_2" in self.fields:
            parts.append(
                get_person_address_2(
                    row,
                    use_representative=self.use_representative,
                )
            )

        return parts

    def _parse_row_extra_parts(self, row):
        parts = []
        if "tel" in self.fields:
            parts.append(row.get("tel"))

        if "email" in self.fields:
            parts.append(row.get("email"))

        if "reference_number" in self.fields:
            parts.append(row.get("reference_number"))

        return parts

    def to_representation(self, value):
        if not value or not len(value):  # pragma: no cover
            return ""

        return clean_join(*[self.parse_row(row) for row in value], separator=", ")

    def get_attribute(self, instance):
        value = super().get_attribute(instance)

        return value[:1] if self.only_first and value else value


class MasterDataPersonObjectField(MasterDataField):
    nested_aliases = {
        "NAME": [_("NAME")],
        "ADDRESS": [_("ADDRESS")],
        "JURISTIC_NAME": [{"default": _("NAME_JURISTIC_PERSON"), "sz": _("COMPANY")}],
        "SALUTATION": [_("SALUTATION")],
        "TITLE": [_("TITLE")],
        "FIRST_NAME": [_("FIRST_NAME")],
        "LAST_NAME": [_("LAST_NAME")],
        "STREET": [_("STREET")],
        "STREET_NUMBER": [_("STREET_NUMBER")],
        "PO_BOX": [_("PO_BOX")],
        "ZIP": [_("ZIP")],
        "TOWN": [{"default": _("TOWN"), "sz": _("LOCATION")}],
        "TEL": [{"default": _("PHONE"), "sz": _("TEL")}],
        "EMAIL": [_("EMAIL")],
        "REPRESENTATIVE_NAME": [_("REPRESENTATIVE_NAME")],
        "REPRESENTATIVE_ADDRESS": [_("REPRESENTATIVE_ADDRESS")],
        "REPRESENTATIVE_JURISTIC_NAME": [_("REPRESENTATIVE_NAME_JURISTIC_PERSON")],
        "REPRESENTATIVE_SALUTATION": [_("REPRESENTATIVE_SALUTATION")],
        "REPRESENTATIVE_TITLE": [_("REPRESENTATIVE_TITLE")],
        "REPRESENTATIVE_FIRST_NAME": [_("REPRESENTATIVE_FIRST_NAME")],
        "REPRESENTATIVE_LAST_NAME": [_("REPRESENTATIVE_LAST_NAME")],
        "REPRESENTATIVE_STREET": [_("REPRESENTATIVE_STREET")],
        "REPRESENTATIVE_STREET_NUMBER": [_("REPRESENTATIVE_STREET_NUMBER")],
        "REPRESENTATIVE_PO_BOX": [_("REPRESENTATIVE_PO_BOX")],
        "REPRESENTATIVE_ZIP": [_("REPRESENTATIVE_ZIP")],
        "REPRESENTATIVE_TOWN": [_("REPRESENTATIVE_TOWN")],
        "REPRESENTATIVE_TEL": [_("REPRESENTATIVE_PHONE")],
        "REPRESENTATIVE_EMAIL": [_("REPRESENTATIVE_EMAIL")],
    }

    def to_representation(self, value):
        return [parse_person_row(row, self.nested_aliases.keys()) for row in value]


class InformationOfNeighborsField(AliasedMixin, serializers.ReadOnlyField):
    def __init__(
        self,
        type,
        **kwargs,
    ):
        nested_aliases = (
            {
                "ADDRESS_1": [_("ADDRESS_1")],
                "ADDRESS_2": [_("ADDRESS_2")],
                "NAME": [_("NAME")],
            }
            if type == "neighbors"
            else {}
        )

        super().__init__(
            nested_aliases=nested_aliases,
            **kwargs,
        )

        self.type = type

    def get_work_item(self, instance):
        return (
            instance.case.work_items.filter(
                task_id=settings.PUBLICATION["FILL_TASKS"]["NEIGHBORS"],
                status=WorkItem.STATUS_COMPLETED,
                addressed_groups=[str(self.context["request"].group.service_id)],
                **{"meta__is-published": True},
            )
            .order_by("-created_at")
            .first()
        )

    def get_attribute(self, instance):
        work_item = self.get_work_item(instance)

        if not work_item:
            return None

        if self.type in ["link", "qr_code"]:
            return build_url(
                settings.PUBLIC_BASE_URL,
                f"/public-instances/{instance.pk}/form?key={str(work_item.document.pk)[:7]}",
            )
        elif self.type == "neighbors":
            table = work_item.document.answers.filter(
                question_id=settings.PUBLICATION["NEIGHBORS_TABLE_QUESTION"]
            ).first()

            return [
                row_to_person(row)
                for row in (
                    table.documents.all().order_by("-answerdocument__sort")
                    if table
                    else []
                )
            ]

        return None  # pragma: no cover

    def to_representation(self, value):
        if value and self.type == "qr_code":
            data = BytesIO()
            img = qrcode.make(value)
            img.save(data, "PNG")
            data_b64 = base64.b64encode(data.getvalue())
            return f"data:image/png;base64,{data_b64.decode('utf-8')}"

        elif self.type == "neighbors":
            return [
                {
                    "NAME": get_person_name(person),
                    "ADDRESS_1": get_person_address_1(person),
                    "ADDRESS_2": get_person_address_2(person),
                }
                for person in value
            ]

        return value


class DecisionField(AliasedMixin, serializers.ReadOnlyField):
    def __init__(self, compare_to=None, use_identifier=False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.compare_to = compare_to
        self.use_identifier = use_identifier

    def get_attribute(self, instance):
        work_item = (
            WorkItem.objects.filter(task_id="decision", case__family__instance=instance)
            .exclude(status=WorkItem.STATUS_CANCELED)
            .order_by("-created_at")
            .first()
        )

        return (
            work_item.document.answers.filter(question_id=self.source).first()
            if work_item
            else None
        )

    def to_representation(self, answer):
        if self.compare_to:
            return answer.value in (
                self.compare_to
                if isinstance(self.compare_to, list)
                else [self.compare_to]
            )

        elif answer.question.type == Question.TYPE_CHOICE:
            option = answer.selected_options[0]

            if self.use_identifier:
                return option.meta["identifier"]

            return option.label[get_language()]

        return answer.value  # pragma: no cover


class AlexandriaDocumentField(AliasedMixin, serializers.ReadOnlyField):
    nested_aliases = {
        "NAME": [_("NAME")],
        "ORIGINAL_NAME": [_("ORIGINAL_NAME")],
        "DESCRIPTION": [_("DESCRIPTION")],
        "CREATED_AT": [_("CREATED_AT")],
        "CREATED_BY": [_("CREATED_BY")],
        "MODIFIED_AT": [_("MODIFIED_AT")],
        "MODIFIED_BY": [_("MODIFIED_BY")],
        "CATEGORY": [_("CATEGORY")],
        "MARKS": [_("MARKS")],
        "TAGS": [_("TAGS")],
    }

    def __init__(
        self,
        mark=None,
        category=None,
        include_child_categories=False,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.mark = mark
        self.category = category
        self.include_child_categories = include_child_categories

    def get_attribute(self, instance):
        queryset = alexandria_models.Document.objects.filter(
            instance_document__instance=instance
        ).order_by("title")

        if self.mark:
            queryset = queryset.filter(marks__pk__contains=self.mark)

        if self.category:
            filter = Q(category_id=self.category)

            if self.include_child_categories:
                filter |= Q(category__parent_id=self.category)

            queryset = queryset.filter(filter)

        return CustomAlexandriaVisibility().filter_queryset_for_document(
            queryset, self.context["request"]
        )

    def to_representation(self, documents):
        data = []

        for document in documents:
            system_generated = "system-generated" in document.metainfo
            created_by = ""
            modified_by = ""
            if not system_generated:
                if created_by_user := User.objects.filter(
                    pk=document.created_by_user
                ).first():
                    created_by = created_by_user.get_full_name()
                if modified_by_user := User.objects.filter(
                    pk=document.modified_by_user
                ).first():
                    modified_by = modified_by_user.get_full_name()

            timezone = get_current_timezone()
            data.append(
                {
                    "NAME": document.title,
                    "ORIGINAL_NAME": document.files.filter(variant="original")
                    .order_by("-created_at")
                    .first()
                    .name,
                    "DESCRIPTION": document.description,
                    "CREATED_AT": document.created_at.astimezone(timezone).strftime(
                        "%d.%m.%Y %H:%M"
                    ),
                    "CREATED_BY": created_by,
                    "MODIFIED_AT": document.modified_at.astimezone(timezone).strftime(
                        "%d.%m.%Y %H:%M"
                    ),
                    "MODIFIED_BY": modified_by,
                    "CATEGORY": document.category.slug,
                    "MARKS": list(document.marks.values_list("slug", flat=True)),
                    "TAGS": list(document.tags.values_list("name", flat=True)),
                }
            )

        return data


class AlexandriaSimpleDocumentField(AlexandriaDocumentField):
    nested_aliases = {}

    def to_representation(self, documents):
        return ",\n".join(
            [
                gettext(
                    "%(title)s (submitted as %(original_title)s on %(date)s at %(time)s)"
                )
                % {
                    "title": document.title,
                    "original_title": document.files.filter(variant="original")
                    .order_by("-created_at")
                    .first()
                    .name,
                    "date": document.created_at.strftime("%d.%m.%Y"),
                    "time": document.created_at.astimezone(
                        timezone.get_current_timezone()
                    ).strftime("%H:%M"),
                }
                for document in documents
            ]
        )


class KeywordsField(AliasedMixin, serializers.ReadOnlyField):
    def __init__(self, join_by=", ", *args, **kwargs):
        super().__init__(**kwargs)
        self.join_by = join_by

    def to_representation(self, value):
        keywords = [keyword.get("name") for keyword in value]

        return clean_join(*keywords, separator=self.join_by)

    def get_attribute(self, instance):
        return (
            Keyword.objects.filter(instances=instance).values("name").order_by("name")
        )
