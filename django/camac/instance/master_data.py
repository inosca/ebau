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
        fn = getattr(self, resolver, None)

        if not fn:
            raise AttributeError(
                f"Resolver '{resolver}' used in key '{lookup_key}' is not defined in master data class"
            )

        return fn(*args)

    def answer(self, lookup, value_key="value", document=None, default=None):
        answer = next(
            filter(
                lambda answer: answer.question_id == lookup,
                document.answers.all()
                if document
                else self.case.document.answers.all(),
            ),
            None,
        )
        return getattr(answer, value_key, default) if answer else default

    def case_meta(self, lookup):
        return self.case.meta.get(lookup)

    def table(self, lookup, options, value_key="r"):
        rows = self.answer(
            lookup, "documents", default=form_models.Document.objects.none()
        )

        parsed = []
        for row in rows.all():
            obj = {}
            for key, column_lookup in options.items():
                if isinstance(column_lookup, tuple):
                    value = column_lookup[1].get(
                        self.answer(column_lookup[0], document=row)
                    )
                else:
                    value = self.answer(column_lookup, document=row)
                obj[key] = value

            parsed.append(obj)

        return parsed

    def dynamic_option(self, lookup, default=None):
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
