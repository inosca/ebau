from django.db.models import Q
from django.db.models.constants import LOOKUP_SEP
from django_filters.constants import EMPTY_VALUES
from django_filters.rest_framework import BaseInFilter, CharFilter, NumberFilter


class BaseMultiValueFilter(BaseInFilter):
    """
    Filter for multiple values whereas values as separated with commas.

    Per default lookup_expr 'in' is used, but maybe written and query
    will be handled with `OR` statements.
    """

    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs

        lookup = self.lookup_expr
        if lookup == "in":
            return super().filter(qs, value)

        q = Q()
        for val in value:
            q = q | Q(**{self.field_name + LOOKUP_SEP + lookup: val})

        return qs.filter(q)


class NumberMultiValueFilter(BaseMultiValueFilter, NumberFilter):
    pass


class CharMultiValueFilter(BaseMultiValueFilter, CharFilter):
    pass


class JSONFieldMultiValueFilter(BaseMultiValueFilter, CharFilter):
    def __init__(self, json_field="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.json_field = json_field

    def filter(self, qs, value):
        if value in EMPTY_VALUES or self.json_field == "":
            return qs

        # JSONField is a list, so value must look like this:
        # [{'field_name': 'field_value'}]
        # TODO is it always a list?!
        value_new = [[{self.json_field: val}] for val in value]
        return super().filter(qs, value_new)
