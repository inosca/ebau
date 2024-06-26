import operator
import re
from functools import reduce

from django.conf import settings
from django.db.models import Exists, OuterRef, Q
from django.db.models.constants import LOOKUP_SEP
from django.utils.translation import get_language
from django_filters.constants import EMPTY_VALUES
from django_filters.rest_framework import BaseInFilter, CharFilter, NumberFilter
from rest_framework.filters import SearchFilter


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


class MultilingualSearchFilter(SearchFilter):
    def generate_query(self, orm_lookup, search_term):
        match = re.match(rf".*trans{LOOKUP_SEP}", orm_lookup)
        query = {orm_lookup: search_term}

        if settings.APPLICATION.get("IS_MULTILINGUAL") and match:
            query[f"{match.group()}language"] = get_language()

        return Q(**query)

    def filter_queryset(self, request, queryset, view):
        # WARNING: This whole method is copy pasted from
        # https://github.com/encode/django-rest-framework/blob/3.15.1/rest_framework/filters.py
        # except the line that is marked as changed. If the upstream code
        # changes, we need to update the content of this method as well!
        search_fields = self.get_search_fields(view, request)
        search_terms = self.get_search_terms(request)

        if not search_fields or not search_terms:
            return queryset

        orm_lookups = [
            self.construct_search(str(search_field), queryset)
            for search_field in search_fields
        ]

        base = queryset
        # generator which for each term builds the corresponding search
        conditions = (
            reduce(
                operator.or_,
                # ATTENTION: LINE DIFFERENT TO UPSTREAM
                (self.generate_query(orm_lookup, term) for orm_lookup in orm_lookups),
            )
            for term in search_terms
        )
        queryset = queryset.filter(reduce(operator.and_, conditions))

        # Remove duplicates from results, if necessary
        if self.must_call_distinct(queryset, search_fields):
            # inspired by django.contrib.admin
            # this is more accurate than .distinct form M2M relationship
            # also is cross-database
            queryset = queryset.filter(pk=OuterRef("pk"))
            queryset = base.filter(Exists(queryset))
        return queryset
