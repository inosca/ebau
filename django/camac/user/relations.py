from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework_json_api.relations import ResourceRelatedField
from rest_framework_json_api.serializers import CurrentUserDefault

from camac.relations import FormDataResourceRelatedField
from camac.user.models import Group, Service


class CurrentUserResourceRelatedField(ResourceRelatedField):
    """User resource related field restricting user to current user."""

    def __init__(self, *args, **kwargs):
        kwargs["default"] = CurrentUserDefault()
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        request = self.context["request"]
        return get_user_model().objects.filter(pk=request.user.pk)


class CurrentUserFormDataResourceRelatedField(
    FormDataResourceRelatedField, CurrentUserResourceRelatedField
):
    pass


class GroupResourceRelatedField(ResourceRelatedField):
    """Group resource related field restricting groups to user groups."""

    def get_queryset(self):
        request = self.context["request"]

        return Group.objects.filter(
            Q(pk__in=request.user.groups.values("group_id")) | Q(pk=request.group.pk)
        )


class ServiceResourceReleatedField(GroupResourceRelatedField):
    """Service resource related field restricting services to user services."""

    def get_queryset(self):
        services = super().get_queryset().values("service_id")
        return Service.objects.filter(pk__in=services)


class ServiceFormDataResourceRelatedField(
    FormDataResourceRelatedField, GroupResourceRelatedField
):
    pass


class GroupFormDataResourceRelatedField(
    FormDataResourceRelatedField, GroupResourceRelatedField
):
    pass
