from alexandria.core import views
from django.core.cache import cache
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework_json_api.django_filters import DjangoFilterBackend

from camac.alexandria.extensions.permissions.extension import (
    CustomPermission as CustomAlexandriaPermission,
)
from camac.caluma.models import Inquiry
from camac.constants.kt_gr import ARE_SERVICE_GROUP
from camac.core.utils import canton_aware
from camac.filters import MultilingualSearchFilter
from camac.instance.models import Instance
from camac.user.models import Service
from camac.user.permissions import DefaultPermission, PublicationPermission


class AlexandriaFileDownloadPermission(BasePermission):
    """Allow anonymous download of files.

    For file downloads we use presigned URLs so anonymous users can download a
    file if they use the correct presigned URL. This permission removes the
    condition of being authenticated and will always return true for the
    download action.
    """

    def has_permission(self, request, view):
        return (
            view.__class__.__name__ == "PatchedFileViewSet"
            and getattr(view, "action", None) == "download"
        )


class PatchedDjangoFilterBackend(DjangoFilterBackend):
    search_param = "filter[search]"


class PatchedSearch(MultilingualSearchFilter):
    search_param = "filter[search]"


class PatchedDocumentViewSet(views.DocumentViewSet):
    permission_classes = [DefaultPermission | PublicationPermission]
    filter_backends = [
        PatchedSearch,
        OrderingFilter,
        PatchedDjangoFilterBackend,
    ]


class PatchedFileViewSet(views.FileViewSet):
    permission_classes = [
        DefaultPermission | PublicationPermission | AlexandriaFileDownloadPermission
    ]


class PatchedTagViewSet(views.TagViewSet):
    filter_backends = [
        PatchedSearch,
        OrderingFilter,
        PatchedDjangoFilterBackend,
    ]


class PatchedCategoryViewSet(views.CategoryViewSet):
    permission_classes = [DefaultPermission | PublicationPermission]

    @canton_aware
    def get_queryset(self):
        return super().get_queryset()

    def get_queryset_gr(self):
        """
        Filter categories for an instance-specific request..

        If the request is for a specific instance, we add category filtering for
        categories that need to be hidden for inquired services that are not
        inquired by ARE.
        """
        params = self.request.query_params
        queryset = super().get_queryset()

        # If no group or service is set, ignore the filter.
        if not self.request.group or not self.request.group.service:  # pragma: no cover
            return queryset

        service_group = self.request.group.service.service_group

        # ARE service group does not need filtering.
        if not service_group or service_group.name == ARE_SERVICE_GROUP:
            return queryset

        # If a service is not invited by ARE, exclude alexandria categories
        # with the metainfo key "hideInBab".
        if (
            "camac-instance-id" in params
            and not (
                Inquiry.objects.for_instance(str(params["camac-instance-id"]))
                .addressed_to(self.request.group.service_id)
                .controlled_by(
                    Service.objects.filter(service_group__name=ARE_SERVICE_GROUP)
                    .first()
                    .pk
                )
            ).exists()
        ):
            return queryset.exclude(metainfo__has_key="hideInBab")

        return queryset

    @action(methods=["get"], detail=True)
    def permissions(self, request, pk=None):
        instance_id = request.query_params.get("instance")

        if not instance_id:
            raise ValidationError("'instance' query parameter must be passed")

        cache_key = "-".join(
            [
                "permissions",
                f"category:{pk}",
                f"instance:{instance_id}",
                f"user:{request.user.pk}",
                f"group:{request.group.pk}",
            ]
        )

        permissions = cache.get_or_set(
            cache_key,
            lambda: self._get_permissions_for_category_on_instance(
                self.get_object(),
                request.query_params.get("instance"),
                request,
            ),
            3600,
        )

        return Response(permissions, status=status.HTTP_200_OK)

    def _get_permissions_for_category_on_instance(self, category, instance_id, request):
        return CustomAlexandriaPermission().get_available_permissions(
            request,
            Instance.objects.get(pk=instance_id),
            category,
        )


class PatchedMarkViewSet(views.MarkViewSet):
    permission_classes = [DefaultPermission | PublicationPermission]
