from django.db.models import Q
from rest_framework_json_api.relations import ResourceRelatedField

from camac.relations import FormDataResourceRelatedField
from camac.user.models import Group, Service


class GroupResourceRelatedField(ResourceRelatedField):
    """Group resource related field restricting groups to user groups."""

    def get_queryset(self):
        request = self.context['request']

        return Group.objects.filter(
            Q(pk__in=request.user.groups.values('group_id')) |
            Q(pk=request.group.pk))


class ServiceResourceReleatedField(GroupResourceRelatedField):
    """Service resource related field restricting services to user services."""

    def get_queryset(self):
        services = super().get_queryset().values('service_id')
        return Service.objects.filter(pk__in=services)


class GroupFormDataResourceRelatedField(FormDataResourceRelatedField,
                                        GroupResourceRelatedField):
    pass
