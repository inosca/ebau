from django.core.validators import EMPTY_VALUES
from django_filters.rest_framework import (
    BooleanFilter,
    CharFilter,
    FilterSet,
    NumberFilter,
)

from camac.filters import CharMultiValueFilter

from ..responsible import models as responsible_models
from . import models


class TopicResponsibleServiceUserFilter(CharFilter):
    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs

        # restrict to service from request header
        current_service = self.parent.request.group.service

        if value.lower() == "nobody":
            return qs.exclude(
                # exclude all topics with instances which have responsible services
                instance__pk__in=responsible_models.ResponsibleService.objects.filter(
                    service=current_service
                ).values("instance")
            )

        return qs.filter(
            # restrict to current service
            instance__responsible_services__service=current_service,
            instance__responsible_services__responsible_user=value,
        )


class TopicFilterSet(FilterSet):
    has_unread = BooleanFilter()
    responsible_service_user = TopicResponsibleServiceUserFilter()

    class Meta:
        model = models.CommunicationsTopic
        fields = ("subject", "has_unread", "instance", "responsible_service_user")


class IsReadFilter(BooleanFilter):
    def filter(self, queryset, value):
        if value is None:
            # Not filtering if filter value is not given
            return queryset
        if value:
            return queryset.filter(read_at__isnull=False)
        else:
            return queryset.filter(read_at__isnull=True)


class MessageFilterSet(FilterSet):
    is_read = IsReadFilter()
    instance = NumberFilter(field_name="topic__instance_id")

    class Meta:
        model = models.CommunicationsMessage
        fields = ["topic", "is_read", "instance"]


class AttachmentFilterSet(FilterSet):
    name = CharMultiValueFilter()

    class Meta:
        model = models.CommunicationsAttachment
        fields = ("name",)
