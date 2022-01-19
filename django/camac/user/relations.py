from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework_json_api.relations import ResourceRelatedField
from rest_framework_json_api.serializers import CurrentUserDefault

from camac.relations import FormDataResourceRelatedField
from camac.user.models import Group, Service
from camac.user.permissions import permission_aware


class CurrentUserDefault(CurrentUserDefault):
    def __call__(self, serializer_field=None):
        if serializer_field and "request" in serializer_field.context:
            return serializer_field.context["request"].user

    def set_context(self, serializer_field):
        # When generating the schema with our custom FileUploadSwaggerAutoSchema
        # we don't have access to the request object
        self.user = None
        if "request" in serializer_field.context:
            self.user = serializer_field.context["request"].user


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

    @permission_aware
    def get_queryset(self):
        request = self.context.get("request")
        return Group.objects.filter(
            Q(pk__in=request.user.groups.values("pk")) | Q(pk=request.group.pk)
        )

    def get_queryset_for_public(self):
        return Group.objects.none()

    def get_queryset_for_support(self):
        return Group.objects.all()


class ServiceResourceRelatedField(GroupResourceRelatedField):
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
    def to_representation(self, value):
        if hasattr(value, "pk"):
            return super().to_representation(value)
