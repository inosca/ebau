from dataclasses import dataclass

from caluma.caluma_form import models as form_models
from django.conf import settings
from django.utils.translation import get_language


@dataclass
class MasterData(object):
    case: object

    def __getattr__(self, lookup_key):
        config = settings.APPLICATION["MASTER_DATA"].get(lookup_key)

        if not config:
            raise AttributeError(
                f"Key '{lookup_key}' is not configured in master data config"
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

    def _get_cell_value(self, row, lookup_config):
        options = {}

        if isinstance(lookup_config, tuple):
            lookup, options = lookup_config
        else:
            lookup = lookup_config

        value = self.answer_resolver(lookup, document=row)

        if options.get("value_mapping"):
            return options.get("value_mapping").get(value)

        return value

    def answer_resolver(
        self, lookup, value_key="value", document=None, default=None, value_mapping={}
    ):
        """Resolve data from caluma answers.

        Example configuration for a "normal" value:

        MASTER_DATA = {
            "some_string": (
                "answer",
                # This could also be multiple, the first with an answer will be returned
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
                    "value_mapping": {
                        "my-choice-yes": True,
                        "my-choice-no": False,
                    }
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
        return getattr(answer, value_key, default) if answer else default

    def case_meta_resolver(self, lookup, default=None):
        """Resolve data from the case meta.

        Example configuration:

        MASTER_DATA = {
            "identifier": {
                "case_meta",
                "ebau-number"
            }
        }
        """
        return self.case.meta.get(lookup, default)

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
                                "value_mapping": {
                                    "is-juristic-person-yes": True,
                                    "is-juristic-person-no": False,
                                }
                            }
                        ),
                    }
                }
            }
        }
        """
        rows = self.answer_resolver(
            lookup, "documents", default=form_models.Document.objects.none()
        )

        return [
            {
                key: self._get_cell_value(row, lookup_config)
                for key, lookup_config in column_mapping.items()
            }
            for row in rows.all()
        ]

    def dynamic_option_resolver(self, lookup, default=None):
        """Resolve data from dynamic options.

        Example configuration:

        MASTER_DATA = {
            "municipality": {
                "dynamic_option",
                "municipality"
            }
        }
        """
        dynamic_option = next(
            filter(
                lambda dynamic_option: dynamic_option.question_id == lookup,
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
