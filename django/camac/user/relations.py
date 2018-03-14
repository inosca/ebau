from django.db.models import Q
from rest_framework_json_api.relations import ResourceRelatedField

from camac.relations import FormDataResourceRelatedField
from camac.user.models import Group


class GroupResourceRelatedField(ResourceRelatedField):
    """Group resource related field restricting groups to user groups."""

    def get_queryset(self):
        request = self.context['request']

        return Group.objects.filter(
            Q(pk__in=request.user.groups.values('group_id')) |
            Q(pk=request.group.pk))


class GroupFormDataResourceRelatedField(FormDataResourceRelatedField,
                                        GroupResourceRelatedField):
    pass
