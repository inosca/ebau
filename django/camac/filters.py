from django.db.models import Q
from django.db.models.constants import LOOKUP_SEP
from django_filters.rest_framework import (BaseInFilter, CharFilter,
                                           NumberFilter)


class BaseMultiValueFilter(BaseInFilter):
    """
    Filter for multiple values whereas values as separated with commas.

    Per default lookup_expr 'in' is used, but maybe written and query
    will be handled with `OR` statements.
    """

    def filter(self, qs, value):
        lookup = self.lookup_expr
        if lookup == 'in':
            return super().filter(qs, value)

        q = Q()
        for val in value:
            q = q | Q(**{self.field_name + LOOKUP_SEP + lookup: val})

        return qs.filter(q)


class NumberMultiValueFilter(BaseMultiValueFilter, NumberFilter):
    pass


class CharMultiValueFilter(BaseMultiValueFilter, CharFilter):
    pass
