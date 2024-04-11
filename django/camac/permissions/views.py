from logging import getLogger

from django.conf import settings
from django.db.models import Exists, OuterRef, Q
from rest_framework import response, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework_json_api.views import ModelViewSet, ReadOnlyModelViewSet

from camac.core import models as core_models
from camac.instance import filters as instance_filters, models as instance_models
from camac.instance.mixins import InstanceQuerysetMixin
from camac.permissions.switcher import permission_switching_method
from camac.user.permissions import get_group, get_role_name, permission_aware
from camac.utils import get_dict_item

from . import api, filters, mixins, models, permissions, serializers

log = getLogger(__name__)


class InstanceACLViewset(InstanceQuerysetMixin, ModelViewSet):
    serializer_class = serializers.InstanceACLSerializer
    filterset_class = filters.InstanceACLFilterSet
    queryset = models.InstanceACL.objects

    instance_field = "instance"
    ordering_fields = ["start_time"]
    ordering = ["-start_time"]

    @permission_switching_method
    def get_queryset(self):
        qs = self.get_base_queryset()
        # Instance ACLs are never shown outside of a single instance. Therefore
        # we find the instance query param here (even though the filtering is done in
        # the filterset) and limit the ACL visibility to the ones where
        # the user has `permissions-read-$ACCESSLEVEL`.

        instance_id = self.request.query_params.get("instance")
        if not instance_id:
            if "pk" in self.kwargs:
                # Detail view (or revoke). This is a bit ugly, bu twe use
                # the (single) ACL to get the instance, and from there see
                # if the user is actually allowed to see the ACL.
                # I wish we could get around the double-query here, but
                # can't see how
                instance_id = qs.model.objects.get(pk=self.kwargs["pk"]).instance_id
            else:
                # User MUST pass instance filter for the list view
                log.warning(
                    "Permissions view: No instance filter given, and "
                    "not in detail view. Not returning anything!"
                )
                return qs.none()

        manager = api.PermissionManager.from_request(self.request)
        have_permissions = manager.get_permissions(instance_id)

        read_prefix = permissions.READ_SPECIFIC("")

        # If we have a "permissions-read-foo" on this instance, we're allowed
        # to see all ACLs that refer to the access level "foo".
        visible_access_levels = [
            perm.replace(read_prefix, "")
            for perm in have_permissions
            if perm.startswith(read_prefix)
        ]
        if "any" in visible_access_levels:
            # The exception is "any", which allows us to see all ACLs
            log.debug("User has permission to see *any* access level")
            return qs

        log.debug(f"User has permission to see access levels {visible_access_levels}")
        return qs.filter(access_level__slug__in=visible_access_levels)

    @get_queryset.register_old
    def get_queryset_rbac(self):
        # TODO: This uses the old permissions / visibility system for now.
        #       Migrate once we're fully using the permissions system
        #       (automatic creation / revocation etc)

        # The InstanceQuerysetMixin grants too much access, as an
        # instance is visible to a wider audience than the ACLs should be.
        # Therefore we need to do the role switching manually and just call
        # `get_queryset_for_municipality()` in the right circumstances
        group = get_group(self)
        role_name = get_role_name(group)
        if role_name == "municipality":
            qs = self.get_queryset_for_municipality()
            # Filter it down some more: Only if user is actually part of a
            # responsible service for the instances, can they be seen
            return qs.filter(
                Exists(
                    core_models.InstanceService.objects.filter(
                        instance=OuterRef("instance"), service=group.service
                    )
                )
                | Q(instance__group__service=group.service)
            )
        elif role_name == "applicant":
            qs = super().get_queryset(self)

            return qs.filter(access_level_id="municipality-before-submission")

        return models.InstanceACL.objects.none()

    @action(methods=["post"], detail=True)
    def revoke(self, request, pk):
        return self._revoke(request, pk)

    @permission_switching_method
    def _revoke(self, request, pk):
        acl: models.InstanceACL = self.get_object()
        api.PermissionManager.from_request(request).require_any(
            acl.instance,
            [permissions.REVOKE_ANY, permissions.REVOKE_SPECIFIC(acl.access_level_id)],
        )

        return self._do_revoke(request, acl)

    @_revoke.register_old
    def _revoke_rbac(self, request, pk):
        acl: models.InstanceACL = self.get_object()
        self.enforce_change_permission(acl.instance)
        return self._do_revoke(request, acl)

    def _do_revoke(self, request, acl):
        api.PermissionManager.from_request(request).revoke(
            acl,
            event_name="manual-revocation",
        )
        serializer = self.get_serializer(acl)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def enforce_change_permission(self, instance: instance_models.Instance):
        """Enforce change permission for ACLs on this instance.

        Checks whether the user is allowed, and raises an exception
        if not.

        NOTE: This is currently only looking at the instance's responsible
        services and matches them against the user's group's service (de facto
        only allowing "Leitbehörde" and other responsible services to grant/
        revoke permissions).

        This will need to be changed when other user groups
        start granting permissions, and needs to be fully rewritten once the
        permissions module becomes the sole "source-of-truth" for access rights
        """
        # Currently, create/revoke have the same permissions
        request_service_id = self.request.group.service.pk

        if settings.APPLICATION.get("USE_INSTANCE_SERVICE"):
            active_service_filters = get_dict_item(
                settings.APPLICATION, "ACTIVE_SERVICES.MUNICIPALITY.FILTERS"
            )
            has_permission = instance.instance_services.filter(
                **active_service_filters, service_id=request_service_id
            ).exists()
        else:
            has_permission = request_service_id == instance.group.service_id

        if not has_permission:
            # This is primarily already handled via visibility, but this will
            # change and then we'll need this check here as well
            raise ValidationError(
                "Only responsible service may manage ACLs on this instance"
            )

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
    filterset_class = filters.AccessLevelFilterset

    @permission_aware
    def get_queryset(self):
        # TODO is this still correct? We're post-Geometer permissions
        # now, so non-municpality users should likely sse the access levels
        # as well...
        return super().get_queryset().none()

    def get_queryset_for_municipality(self):
        return super().get_queryset()
