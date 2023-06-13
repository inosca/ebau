from django_filters.rest_framework import BooleanFilter, FilterSet, NumberFilter

from camac.filters import CharMultiValueFilter

from . import models


class TopicFilterSet(FilterSet):
    has_unread = BooleanFilter()

    class Meta:
        model = models.CommunicationsTopic
        fields = ("subject", "has_unread", "instance")


class IsReadFilter(BooleanFilter):
    def filter(self, queryset, value):
        if value is None:
            # Not filtering if filter value is not given
            return queryset
        if value:
            return queryset.filter(read_at__isnull=False)
        else:
            return queryset.filter(read_at__isnull=True)


class IsDraftFilter(BooleanFilter):
    def filter(self, queryset, value):
        if value is None:
            return queryset

        # A draft is a message without sent_at.
        return queryset.filter(sent_at__isnull=value)


class MessageFilterSet(FilterSet):
    is_read = IsReadFilter()
    is_draft = IsDraftFilter()
    instance = NumberFilter(field_name="topic__instance_id")

    class Meta:
        model = models.CommunicationsMessage
        fields = ["topic", "is_read", "is_draft", "instance"]


class AttachmentFilterSet(FilterSet):
    name = CharMultiValueFilter()

    class Meta:
        model = models.CommunicationsAttachment
        fields = ("name",)
