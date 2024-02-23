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
from camac.filters import MultilingualSearchFilter
from camac.instance.models import Instance
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
