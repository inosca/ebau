from rest_framework import response, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework_json_api.views import ModelViewSet, ReadOnlyModelViewSet

from camac.instance import filters as instance_filters, models as instance_models
from camac.instance.mixins import InstanceQuerysetMixin
from camac.user.permissions import get_group, get_role_name, permission_aware

from . import api, filters, mixins, models, serializers


class InstanceACLViewset(InstanceQuerysetMixin, ModelViewSet):
    serializer_class = serializers.InstanceACLSerializer
    filterset_class = filters.InstanceACLFilterSet
    queryset = models.InstanceACL.objects

    instance_field = "instance"

    def get_queryset(self):
        # TODO: This uses the old permissions / visibility system for now.
        #       Migrate once we're fully using the permissions system
        #       (automatic creation / revocation etc)

        # The InstanceQuerysetMixin grants too much access, as an
        # instance is visible to a wider audience than the ACLs should be.
        # Therefore we need to do the role switching manually and just call
        # `get_queryset_for_municipality()` in the right circumstances
        role_name = get_role_name(get_group(self))
        if role_name == "municipality":
            return self.get_queryset_for_municipality()
        return models.InstanceACL.objects.none()

    @action(
        methods=["post"],
        detail=True,
        serializer_class=serializers.InstanceACLSerializer,
    )
    @permission_aware
    def revoke(self, request, pk):
        raise ValidationError("You do not have permission to revoke ACLs here")

    def revoke_for_municipality(self, request, pk):
        acl = self.get_object()

        serializer = self.get_serializer(acl, data=request.data)
        serializer.is_valid(raise_exception=True)

        # We really only look ad the end_time field, everything else
        # gets ignored (ACLs' attributes cannot be modified after all)
        end_time = serializer.validated_data.get("end_time")

        # We don't allow past revocations. Immediate revocations can be done
        # by setting no end time. The revoke() method will then set it to
        # the current datetime before saving the ACL
        api.PermissionManager.from_request(request).revoke(
            acl,
            ends_at=end_time,
            event_name="manual-revocation",
        )
        # Reload the serializer, so updated data is rendered
        serializer = self.get_serializer(acl)

        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, *_args, **_kwargs):
        raise ValidationError(
            "You cannot delete InstanceACLs. Use the revoke endpoint instead"
        )

    def update(self, *_args, **_kwargs):
        raise ValidationError(
            "You cannot modify InstanceACLs. Use the revoke endpoint for revocations, "
            "other changes are not permitted"
        )


class InstancePermissionsViewset(
    mixins.PermissionVisibilityMixin, ReadOnlyModelViewSet
):
    filterset_class = instance_filters.InstanceFilterSet
    serializer_class = serializers.InstancePermissionSerializer
    queryset = instance_models.Instance.objects

    instance_prefix = ""


class AccessLevelViewset(ReadOnlyModelViewSet):
    serializer_class = serializers.AccessLevelSerializer
    queryset = models.AccessLevel.objects.all()

    @permission_aware
    def get_queryset(self):
        return super().get_queryset().none()

    def get_queryset_for_municipality(self):
        return super().get_queryset()
