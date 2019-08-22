from django.db.models import Q
from django.db.models.constants import LOOKUP_SEP
from django_filters.constants import EMPTY_VALUES
from django_filters.rest_framework import BaseInFilter, CharFilter, NumberFilter


class BaseMultiValueFilter(BaseInFilter):
    """
    Filter for multiple values whereas values as separated with commas.

    Per default lookup_expr 'in' is used, but maybe written and query
    will be handled with `OR` statements.

    This filter also supports the lookup mode "all", which is only
    useful in 1:n relations: It will filter the same field to multiple
    values.
    """

    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs

        lookup = self.lookup_expr
        if lookup == "in":
            return super().filter(qs, value)

        elif lookup == "all":
            for val in value:
                # need to match all values (useful only on 1:n rels)
                qs = qs.filter(Q(**{self.field_name: val}))
            return qs

        q = Q()
        for val in value:
            q = q | Q(**{self.field_name + LOOKUP_SEP + lookup: val})

        return qs.filter(q)


class NumberMultiValueFilter(BaseMultiValueFilter, NumberFilter):
    pass


class CharMultiValueFilter(BaseMultiValueFilter, CharFilter):
    pass


class JSONFieldMultiValueFilter(BaseMultiValueFilter, CharFilter):
    """
    Filter a JSON field by multiple values.

    Depending on the field's structure, you can use value_transform to
    translate the search value into a lookup that accesses the right field
    within JSON.
    """

    def __init__(self, value_transform=lambda x: x, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value_transform = value_transform

    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs

        value_new = self.value_transform(value)
        return super().filter(qs, value_new)
