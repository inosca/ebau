from dataclasses import dataclass, field
from logging import getLogger
from operator import attrgetter
from typing import List, Optional, TypeVar
from uuid import UUID

from caluma.caluma_form.models import Document
from caluma.caluma_form.structure import FastLoader
from caluma.caluma_form.validators import DocumentValidator
from caluma.caluma_workflow.models import Case, WorkItem
from dateutil.parser import ParserError, parse as dateutil_parse
from django.conf import settings
from django.db.models import Prefetch, QuerySet
from django.utils.translation import get_language

from camac.core.models import MultilingualModel
from camac.utils import get_dict_item

log = getLogger(__name__)

T = TypeVar("T", bound="MasterData")


@dataclass
class MasterData(object):
    """Helper class to access common information on a case (municipality, dossier number, etc.).

    Master data should be used to access common information of a case in the
    codebase to avoid duplicated code. The properties of this class can be
    configured per canton in the respective settings modules:
    `camac/settings/modules/master_data.py`.

    To get an instance of master data, in most cases it makes sense to use the
    factory method `.from_case_id` which will prefetch most of the related data
    needed for populating the data. It can also be instantiated via regular
    constructor (`MasterData(my_case)`). However, this only makes sense if you
    are sure that you only need a single property of master data and performance
    doesn't matter that much (so only actions, no list or detail views).

    If you use master data in a list view, make sure to prefetch your queryset
    using `.prefetch_entities_for_queryset` and use the constructor directly in
    combination with the `MultipleCaseMasterdata` class. An example for this is
    the `camac.instance.views.PublicCalumaInstanceView`.
    """

    case: Case
    validation_context: dict = field(default_factory=dict)
    _fastloader: Optional[FastLoader] = field(default=None)

    @classmethod
    def from_case_id(cls, case_id: UUID) -> T:
        queryset = MasterData.prefetch_entities_for_queryset(Case.objects)
        return MasterData(queryset.get(pk=case_id))

    def __getattr__(self, lookup_key):
        config = get_dict_item(
            settings.MASTER_DATA, f"CONFIG.{lookup_key}", default=None
        )

        if not config:
            available_keys = ", ".join(settings.MASTER_DATA["CONFIG"].keys())
            raise AttributeError(
                f"Key '{lookup_key}' is not configured in master data config. "
                f"Available keys are: {available_keys}"
            )

        resolver, *args = config
        fn = getattr(self, f"{resolver}_resolver", None)

        if not fn:
            raise AttributeError(
                f"Resolver '{resolver}' used in key '{lookup_key}' is not defined in master data class"
            )

        if len(args) == 0:
            return fn()

        lookup = args[0]
        kwargs = args[1] if len(args) > 1 else {}

        return fn(lookup, **kwargs)

    def _parse_value(
        self, value, default=None, value_parser=None, answer=None, field=None, **kwargs
    ):
        if not value_parser or not value:
            return value if value else default

        options = {}

        if isinstance(value_parser, tuple):
            parser_name, options = value_parser
        else:
            parser_name = value_parser

        parser = getattr(self, f"{parser_name}_parser", None)

        if not parser:
            raise AttributeError(
                f"Parser '{parser_name}' is not defined in master data class"
            )

        return parser(
            value, default=default, field=field, answer=answer, **options, **kwargs
        )

    def _build_cell_value(self, row, lookup_config):
        options = {}

        if lookup_config == "pk":
            return str(row._document.pk)
        elif isinstance(lookup_config, tuple):
            lookup, options = lookup_config
        else:
            lookup = lookup_config

        if lookup == "default":
            return options.get("default")

        try:
            return self.struc_field_resolver(lookup, row, **options)
        except Exception:  # pragma: todo cover
            return self._parse_value(None, **options)

    def struc_field_resolver(self, lookup, fieldset, **options):
        field = fieldset.get_field(lookup)
        if not field:
            log.warning("Field %s does not exist in %s", lookup, fieldset.get_path())
            return None

        return self._parse_value(field.get_value(), field=field, **options)

    def _get_ng_cell_value(self, row, lookup_config):
        options = {}

        if isinstance(lookup_config, tuple):
            lookup, options = lookup_config
            if lookup == "static":
                return options
        else:
            lookup = lookup_config

        return self._parse_value(row.get(lookup), **options)

    def _get_structure(self, document):
        if document.pk not in self.validation_context:
            self.validation_context[document.pk] = self._build_structure(document)
        return self.validation_context[document.pk]

    def _build_structure(self, document):
        return DocumentValidator().get_validation_context(
            document, _fastloader=self._fastloader
        )

    def static_resolver(self, value):
        """Resolve static value for a master data key.

        Example configuration for a static value:

        MASTER_DATA = {
            "demo": {
                "CONFIG": {
                    "some_string": ("static", "my-string")
                }
            }
        }
        """
        return value

    def form_name_resolver(self):
        return self.case.document.form.name.translate()

    def _get_document(self, document_from_work_item=None):
        # TODO: Fallback to case docu if not found? Or return None instead?
        if document_from_work_item:
            work_item = next(
                filter(
                    lambda work_item: work_item.task_id == document_from_work_item,
                    self.case.work_items.all(),
                ),
                None,
            )
            return work_item.document if work_item else None
        return self.case.document

    def answer_resolver(
        self,
        lookup,
        value_key="value",
        document=None,
        document_from_work_item=None,
        **kwargs,
    ):
        """Resolve data from caluma answers.

        Example configuration for a "normal" value:

        MASTER_DATA = {
            "demo": {
                "CONFIG": {
                    "some_string": (
                        "answer",
                        # question slug of the answer, can also be multiple
                        "my-string"
                    )
                }
            }
        }

        Example configuration for a date value:

        MASTER_DATA = {
            "demo": {
                "CONFIG": {
                    "some_date": (
                        "answer",
                        "my-date",
                        {
                            "value_key": "date",
                            "default": datetime.date(2021, 8, 13)
                        }
                    )
                }
            }
        }

        Example configuration for a choice question:

        MASTER_DATA = {
            "demo": {
                "CONFIG": {
                    "some_choice": (
                        "answer",
                        "my-choice",
                        {
                            "value_parser": (
                                {
                                    "mapping": {
                                        "my-choice-yes": True,
                                        "my-choice-no": False,
                                    }
                                }
                            ),
                            "default": False
                        }
                    )
                }
            }
        }
        """
        if not isinstance(lookup, list):
            lookup = [lookup]

        document = document or self._get_document(document_from_work_item)

        if not document:
            # Requested document likely is from a workitem that may not have
            # started yet, and that's ok
            return None

        struc = self._get_structure(document)
        field = next(
            filter(
                lambda f: f is not None and f.is_visible(),
                (struc.get_field(slug) for slug in lookup),
            ),
            None,
        )

        # Field may be None if the question is hidden for example. Just
        # fallback to None instead
        answer = field.answer if field else None

        return self._parse_value(
            getattr(answer, value_key, None) if answer else None,
            answer=answer,
            field=field,
            **kwargs,
        )

    def case_meta_resolver(self, lookup, **kwargs):
        """Resolve data from the case meta.

        Example configuration:

        MASTER_DATA = {
            "demo": {
                "CONFIG": {
                    "identifier": (
                        "case_meta",
                        "some-date",
                        {
                            "value_parser": "date"
                        }
                    )
                }
            }
        }
        """
        return self._parse_value(self.case.meta.get(lookup), **kwargs)

    def table_resolver(self, lookup, column_mapping={}, **kwargs):
        """Resolve data from caluma table answers.

        Example configuration:

        MASTER_DATA = {
            "demo": {
                "CONFIG": {
                    "applicant": (
                        "table",
                        "applicant",
                        {
                            "column_mapping": {
                                "first_name": "first-name",
                                "last_name": "last-name",
                                "is_juristic_person": (
                                    "is-juristic-person",
                                    {
                                        "value_parser": (
                                            "value_mapping",
                                            {
                                                "mapping": {
                                                    "is-juristic-person-yes": True,
                                                    "is-juristic-person-no": False,
                                                }
                                            }
                                        )
                                    }
                                )
                            }
                        }
                    )
                }
            }
        }
        """

        document = self._get_document(kwargs.get("document_from_work_item"))
        if not document:
            return []

        struc = self._get_structure(document)
        table_field = struc.get_field(lookup)

        if not table_field:
            log.warning(
                "Table %s not found in document with form %s", lookup, document.form_id
            )
            return []
        if table_field.is_empty():
            # Hidden or empty - don't return anything
            return []

        return [
            {
                key: self._build_cell_value(row, lookup_config)
                for key, lookup_config in column_mapping.items()
            }
            for row in table_field.children()
        ]

    def baukontrolle_resolver(self, lookup, column_mapping={}, **kwargs):
        """Find a specific date from the "Baukontrolle" caluma table.

        This goes through all rows and returns the first non-empty value.

        Example configuration:

        MASTER_DATA = {
            "final_approval_date": (
                "baukontrolle", "baukontrolle-realisierung-schlussabnahme"
            }
        }
        """

        rows = self.table_resolver(
            "baukontrolle-realisierung-table",
            column_mapping={"value": (lookup, {"value_key": "date"})},
            document_from_work_item="building-authority",
        )
        if len(rows) == 0:
            return None

        return next((r["value"] for r in rows if r["value"]), None)

    def first_workflow_entry_resolver(self, lookup, default=None, **kwargs):
        """Resolve data from the first workflow entry.

        Example configuration:

        MASTER_DATA = {
            "demo": {
                "CONFIG": {
                    "submit_date": (
                        "first_workflow_entry",
                        # IDs of the workflow items
                        [10]
                    )
                }
            }
        }
        """
        entry = next(
            filter(
                lambda entry: entry.workflow_item_id in lookup,
                self.case.instance.workflowentry_set.all(),
            ),
            None,
        )

        return self._parse_value(entry.workflow_date if entry else default, **kwargs)

    def last_workflow_entry_resolver(self, lookup, default=None, **kwargs):
        """Resolve data from the last workflow entry.

        Example configuration:

        MASTER_DATA = {
            "demo": {
                "CONFIG": {
                    "submit_date": (
                        "last_workflow_entry",
                        # ID of the workflow item, can also be multiple
                        10
                    )
                }
            }
        }
        """
        if not isinstance(lookup, list):
            lookup = [lookup]  # pragma: no cover

        entries = list(
            filter(
                lambda entry: entry.workflow_item_id in lookup,
                self.case.instance.workflowentry_set.all(),
            )
        )

        entry = max(entries, key=lambda entry: entry.group, default=default)
        return self._parse_value(entry.workflow_date if entry else default, **kwargs)

    def php_answer_resolver(self, lookup, default=None, **kwargs):
        """Resolve data from old school camac answers.

        Example configuration:

        MASTER_DATA = {
            "demo": {
                "CONFIG": {
                    "some_string": (
                        "php_answer",
                        # question ID
                        123
                    )
                }
            }
        }
        """
        answer = next(
            filter(
                lambda answer: answer.question_id == lookup,
                self.case.instance.answers.all(),
            ),
            None,
        )

        return self._parse_value(answer.answer if answer else default, **kwargs)

    def ng_answer_resolver(self, lookup, default=None, **kwargs):
        """Resolve data from camac-ng fields.

        Example configuration for a "normal" value:

        MASTER_DATA = {
            "demo": {
                "CONFIG": {
                    "some_string": (
                        "ng_answer",
                        # name of the field
                        "my-field"
                    )
                }
            }
        }

        Example configuration for a value with a potential override:

        MASTER_DATA = {
            "demo": {
                "CONFIG": {
                    "some_string": (
                        "ng_answer",
                        # name of the field and override field
                        ["my-field", "my-field-override"],
                    )
                }
            }
        }
        """
        lookup_previous = None
        if isinstance(lookup, list):
            *lookup_previous, lookup = lookup

        field = next(
            filter(
                lambda field: field.name == lookup,
                self.case.instance.fields.all(),
            ),
            None,
        )

        if not field and lookup_previous:
            field = next(
                filter(
                    lambda field: field.name in lookup_previous,
                    self.case.instance.fields.all(),
                ),
                None,
            )

        parsed_value = self._parse_value(field.value if field else None, **kwargs)
        return parsed_value if parsed_value else default

    def ng_table_resolver(self, lookup, column_mapping={}, **kwargs):
        """Resolve data from camac-ng table fields.

        Example configuration for a camac-ng table with potential table override:

        MASTER_DATA = {
            "demo": {
                "CONFIG": {
                    "applicant": (
                        "ng_table",
                        ["bauherrschaft", "bauherrschaft-override"],
                        {
                            "column_mapping": {
                                "last_name": "name",
                                "first_name": "vorname",
                                "street": "strasse",
                                "zip": "plz",
                                "town": "ort",
                                "is_juristic_person": (
                                    "anrede",
                                    {
                                        "value_parser": (
                                            "value_mapping",
                                            {
                                                "mapping": {
                                                    "Herr": False,
                                                    "Frau": False,
                                                    "Firma": True,
                                                }
                                            }
                                        )
                                    }
                                )
                            }
                        }
                    )
                }
            }
        }

        Example configuration for a camac-ng table with list value:

        MASTER_DATA = {
            "demo": {
                "CONFIG": {
                    "buildings": (
                        "ng_table",
                        "gwr-v2",
                        {
                            "column_mapping": {
                                "name": "gebaeudebezeichnung",
                                "dwellings": (
                                    "wohnungen",
                                    {
                                        "value_parser": (
                                            "list_mapping",
                                            {
                                                "mapping": {
                                                    "location_on_floor": "lage",
                                                }
                                            }
                                        )
                                    }
                                )
                            }
                        }
                    )
                }
            }
        }
        """
        return [
            {
                key: self._get_ng_cell_value(row, lookup_config)
                for key, lookup_config in column_mapping.items()
            }
            for row in self.ng_answer_resolver(lookup, default=[])
        ]

    def instance_property_resolver(self, lookup):
        """Take a lookup path to the property to return final value.

        '__' separate nested properties

        If the target hits a MultilingualModel value the name is translated
        with `get_name`.

        """
        lookup_attr_of = attrgetter(lookup.replace("__", "."))

        try:
            value = lookup_attr_of(self.case.instance)
        except AttributeError as e:
            raise AttributeError(
                f"Instance property lookup failed for lookup `{lookup}` with {e}."
            )

        if isinstance(value, MultilingualModel):
            value = value.get_name()
        return value

    def datetime_parser(self, value, default, **kwargs):
        try:
            return dateutil_parse(value)
        except ParserError:  # pragma: no cover
            return default

    def date_parser(self, value, default, **kwargs):
        try:
            return dateutil_parse(value).date()
        except ParserError:  # pragma: no cover
            return default

    def value_mapping_parser(self, value, default, mapping={}, **kwargs):
        if isinstance(value, list):
            return [
                self.value_mapping_parser(v, default, mapping=mapping) for v in value
            ]

        return mapping.get(value, default)

    def human_readable_date_parser(self, value, default, **kwargs):
        from camac.instance.placeholders.utils import human_readable_date

        return human_readable_date(value) if value else default

    def list_mapping_parser(self, value, default, mapping={}, **kwargs):
        return [
            {
                key: (
                    self._parse_value(
                        next(
                            filter(
                                None,
                                (
                                    item.get(f)
                                    for f in (
                                        field[0]
                                        if isinstance(field[0], list)
                                        else [field[0]]
                                    )
                                ),
                            )
                        ),
                        **field[1],
                    )
                    if isinstance(field, tuple)
                    else item.get(field)
                )
                for key, field in mapping.items()
            }
            for item in value
        ]

    def _return_option(self, option, value, prop, default):
        if not option:
            return default

        if prop == "slug":  # pragma: no cover
            return option.slug
        elif prop == "label":
            return option.label.get(get_language())

        return {"slug": value, "label": option.label.get(get_language())}

    def option_parser(
        self, value, default, answer=None, prop=None, field=None, **kwargs
    ):
        if isinstance(value, list):
            return [
                self.option_parser(v, default, answer=answer, prop=prop, **kwargs)
                for v in value
            ]

        option = next(
            filter(
                lambda option: option.pk == value,
                self._field_or_question_options(answer=answer, field=field),
            ),
            None,
        )
        return self._return_option(option, value, prop, default)

    def _field_or_question_options(self, answer, field):
        if field:
            options = field.get_options()
        else:
            options = answer.question.options.all()
        return options

    def dynamic_option_parser(
        self, value, default, answer=None, prop=None, field=None, **kwargs
    ):
        if isinstance(value, list):  # pragma: no cover
            return [
                self.dynamic_option_parser(
                    v, default, answer=answer, prop=prop, field=field, **kwargs
                )
                for v in value
            ]

        dyn_options = (
            field.get_dynamic_options().values()
            if field
            else answer.document.dynamicoption_set.all()
        )

        dynamic_option = next(
            filter(lambda dynamic_option: dynamic_option.slug == value, dyn_options),
            None,
        )
        return self._return_option(dynamic_option, value, prop, default)

    def to_dict(self, fields: Optional[List[str]] = None) -> dict:
        if not fields:
            fields = settings.MASTER_DATA["CONFIG"].keys()

        return {key: getattr(self, key) for key in fields}

    @staticmethod
    def get_question_slug(property_name: str) -> str | List[str] | None:
        config = get_dict_item(
            settings.MASTER_DATA, f"CONFIG.{property_name}", default=None
        )

        if not config:
            return None

        if config[0] not in ["answer", "table", "ng_answer", "ng_table"]:
            return None

        return config[1]

    @staticmethod
    def prefetch_entities_for_queryset(queryset: QuerySet[Case]) -> QuerySet[Case]:
        """Prefetch and select related data used in master data for a case.

        This analyzes the master data config and adds the needed (depending on
        which resolvers are used) `prefetch_related` and `select_related`
        statements to the passed queryset to reduce queries triggered by master
        data.
        """

        prefetch_related = set()
        select_related = set()

        if not settings.MASTER_DATA:
            return queryset

        config = settings.MASTER_DATA["CONFIG"].values()
        all_resolvers = set([prop[0] for prop in config])
        uses_work_items = any(
            isinstance(property_config[2], dict)
            and "document_from_work_item" in property_config[2]
            for property_config in config
            if len(property_config) > 2
        )

        if "form_name" in all_resolvers:
            select_related.add("document__form")
        if "table" in all_resolvers or "answer" in all_resolvers:
            # Most of the prefetching is done by the fastloader. However, this
            # is still needed for the `get_validation_context` method of the
            # `DocumentValidator` in order to not create a query explosion.
            select_related.update(
                [
                    "document",
                    "document__family",
                    "document__form",
                    "document__work_item",
                    "family",
                    "family__document",
                ]
            )
        if "baukontrolle" in all_resolvers:
            prefetch_related.add("work_items")
        if "ng_answer" in all_resolvers or "ng_table" in all_resolvers:
            prefetch_related.add("instance__fields")
        if "php_answer" in all_resolvers:
            prefetch_related.add("instance__answers")
        if (
            "first_workflow_entry" in all_resolvers
            or "last_workflow_entry" in all_resolvers
        ):
            prefetch_related.add("instance__workflowentry_set")
        if "instance_property" in all_resolvers:
            select_related.update(["instance", "instance__form"])
        if uses_work_items:
            if "work_items" in prefetch_related:
                prefetch_related.remove("work_items")

            # Prefetch all work items of the case including data of the related
            # document to reduce queries in the `get_validation_context` method
            # of the `DocumentValidator`
            prefetch_related.add(
                Prefetch(
                    "work_items",
                    queryset=WorkItem.objects.select_related(
                        "document",
                        "document__family",
                        "document__form",
                    ),
                )
            )

        return queryset.select_related(*select_related).prefetch_related(
            *prefetch_related
        )


class MultipleCaseMasterdata:
    def __init__(self, case_queryset):
        self.case_queryset = case_queryset
        documents = Document.objects.filter(case__in=case_queryset)
        self.fastloader = FastLoader.for_queryset(documents)
        self._cases = {str(case.pk): case for case in case_queryset}

    def for_case(self, case_id):
        case = self._cases[str(case_id)]
        return MasterData(case, _fastloader=self.fastloader)
