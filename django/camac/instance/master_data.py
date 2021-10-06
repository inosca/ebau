from dataclasses import dataclass

from caluma.caluma_form import models as form_models
from dateutil.parser import ParserError, parse as dateutil_parse
from django.conf import settings
from django.utils.translation import get_language


@dataclass
class MasterData(object):
    case: object

    def __getattr__(self, lookup_key):
        config = settings.APPLICATION["MASTER_DATA"].get(lookup_key)

        if not config:
            raise AttributeError(
                f"Key '{lookup_key}' is not configured in master data config. Available keys are: {', '.join(settings.APPLICATION['MASTER_DATA'].keys())}"
            )

        resolver, *args = config
        fn = getattr(self, f"{resolver}_resolver", None)

        if not fn:
            raise AttributeError(
                f"Resolver '{resolver}' used in key '{lookup_key}' is not defined in master data class"
            )

        lookup = args[0]
        kwargs = args[1] if len(args) > 1 else {}

        return fn(lookup, **kwargs)

    def _parse_value(self, value, default=None, value_parser=None, answer=None):
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
            value,
            default=default,
            answer=answer,
            **options,
        )

    def _get_cell_value(self, row, lookup_config):
        options = {}

        if isinstance(lookup_config, tuple):
            lookup, options = lookup_config
        else:
            lookup = lookup_config

        return self.answer_resolver(lookup, document=row, **options)

    def answer_resolver(self, lookup, value_key="value", document=None, **kwargs):
        """Resolve data from caluma answers.

        Example configuration for a "normal" value:

        MASTER_DATA = {
            "some_string": (
                "answer",
                # question slug of the answer, can also be multiple
                "my-string"
            )
        }

        Example configuration for a date value:

        MASTER_DATA = {
            "some_date": (
                "answer",
                "my-date",
                {
                    "value_key": "date",
                    "default": datetime.date(2021, 8, 13)
                }
            )
        }

        Example configuration for a choice question:

        MASTER_DATA = {
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
        """
        if not isinstance(lookup, list):
            lookup = [lookup]

        answer = next(
            filter(
                lambda answer: answer.question_id in lookup,
                document.answers.all()
                if document
                else self.case.document.answers.all(),
            ),
            None,
        )

        return self._parse_value(
            getattr(answer, value_key, None) if answer else None,
            answer=answer,
            **kwargs,
        )

    def case_meta_resolver(self, lookup, **kwargs):
        """Resolve data from the case meta.

        Example configuration:

        MASTER_DATA = {
            "identifier": {
                "case_meta",
                "some-date",
                {
                    "value_parser": "date"
                }
            }
        }
        """
        return self._parse_value(self.case.meta.get(lookup), **kwargs)

    def table_resolver(self, lookup, column_mapping={}):
        """Resolve data from caluma table answers.

        Example configuration:

        MASTER_DATA = {
            "applicant": {
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
                        ),
                    }
                }
            }
        }
        """
        answer_documents = self.answer_resolver(
            lookup, "answerdocument_set", default=form_models.Document.objects.none()
        )

        return [
            {
                key: self._get_cell_value(answer_document.document, lookup_config)
                for key, lookup_config in column_mapping.items()
            }
            for answer_document in reversed(
                sorted(
                    answer_documents.all(),
                    key=lambda answer_document: answer_document.sort,
                )
            )
        ]

    def workflow_entry_resolver(self, lookup, default=None, **kwargs):
        """Resolve data from the workflow entry.

        Example configuration:

        MASTER_DATA = {
            "submit_date": (
                "workflow_entry",
                # ID of the workflow item, can also be multiple
                10
            )
        }
        """
        if not isinstance(lookup, list):
            lookup = [lookup]

        entry = next(
            filter(
                lambda entry: entry.workflow_item_id in lookup,
                self.case.instance.workflowentry_set.all(),
            ),
            None,
        )

        return entry.workflow_date if entry else default

    def ng_answer_resolver(self, lookup, **kwargs):
        """Resolve data from camac-ng fields.

        Example configuration:

        MASTER_DATA = {
            "some_string": (
                "ng_answer",
                # name of the field
                "my-field"
            )
        }
        """
        field = next(
            filter(
                lambda field: field.name == lookup,
                self.case.instance.fields.all(),
            ),
            None,
        )

        return self._parse_value(field.value if field else None, **kwargs)

    def ng_table_resolver(self, lookup, column_mapping={}, **kwargs):
        """Resolve data from camac-ng table fields.

        Example configuration:

        MASTER_DATA = {
            "applicant": {
                "ng_table",
                "bauherrschaft",
                {
                    "column_mapping": {
                        "last_name": "name",
                        "first_name": "vorname",
                        "street": "strasse",
                        "zip": "plz",
                        "town": "ort",
                    }
                }
            }
        }
        """
        return [
            {
                key: row.get(lookup_config)
                for key, lookup_config in column_mapping.items()
            }
            for row in self.ng_answer_resolver(lookup, default=[])
        ]

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

    def option_label_parser(self, value, default, answer=None, **kwargs):
        if isinstance(value, list):
            return [self.option_label_parser(v, default, answer=answer) for v in value]

        option = next(
            filter(lambda option: option.pk == value, answer.question.options.all()),
            None,
        )

        return option.label.get(get_language()) if option else default

    def dynamic_option_parser(self, value, default, answer=None, **kwargs):
        if isinstance(value, list):  # pragma: no cover
            return [
                self.dynamic_option_parser(v, default, answer=answer) for v in value
            ]

        dynamic_option = next(
            filter(
                lambda dynamic_option: dynamic_option.slug == value,
                self.case.document.dynamicoption_set.all(),
            ),
            None,
        )

        return (
            {
                "slug": dynamic_option.slug,
                "label": dynamic_option.label.get(get_language()),
            }
            if dynamic_option
            else default
        )
