from alexandria.core import views
from alexandria.core.models import Category, Mark
from django.conf import settings
from django.core.cache import cache
from django.db.models import CharField, OuterRef, Subquery
from django.db.models.functions import Cast
from django.utils.translation import get_language
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import BasePermission
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_json_api.django_filters import DjangoFilterBackend

from camac.alexandria.extensions.common import has_alexandria_create_permission
from camac.caluma.models import Inquiry
from camac.constants.kt_gr import ARE_SERVICE_GROUP
from camac.core.utils import canton_aware
from camac.filters import MultilingualSearchFilter
from camac.instance.models import Instance
from camac.permissions.conditions import Check
from camac.permissions.models import AccessLevel
from camac.user.models import Role, Service, ServiceT, User
from camac.user.permissions import DefaultPermission, PublicationPermission
from camac.utils import get_dict_item


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
    ordering_fields = [
        "title",
        "modified_at",
        "date",
        "created_at",
        "created_by_username",
        "group_name",
        "category__name",
        "category__sort",
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        # annotate the username/service name because we don't want to sort by a PK
        #
        # The created_by_* fields are string FK's (which we fill with numeric ID's)
        # But theoretically they can also have a string value (e.g. in the test fixtures
        # they are filled as "admin"). That leads to a casting error to an integer field
        # (CAST 'admin' as integer). Therefore we annotate a separate field with the
        # string representation of the FK target and match by that string FK instead.
        queryset = queryset.annotate(
            created_by_username=Subquery(
                User.objects.annotate(pk_str=Cast("pk", output_field=CharField()))
                .filter(pk_str=OuterRef("created_by_user"))
                .values("name")[:1]
            )
        )
        queryset = queryset.annotate(
            group_name=Subquery(
                ServiceT.objects.annotate(
                    service_id_str=Cast("service_id", output_field=CharField())
                )
                .filter(
                    service_id_str=OuterRef("created_by_group"),
                    language=get_language(),
                )
                .values("name")[:1]
            )
        )

        return queryset


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

        # If we are using v1 permissions, we cache the permissions for a category on an instance for 1 hour.
        # For V2 we don't cache, since we're using the permission module already taking care of cache.
        if not settings.ALEXANDRIA["USE_V2_PERMISSIONS"]:
            instance_state_id = Instance.objects.get(pk=instance_id).instance_state_id

            cache_key = "-".join(
                [
                    "permissions",
                    f"category:{pk}",
                    f"instance:{instance_id}",
                    f"instance_state:{instance_state_id}",
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
        else:
            permissions = self._get_permissions_for_category_on_instance(
                self.get_object(),
                request.query_params.get("instance"),
                request,
            )

        return Response(permissions, status=status.HTTP_200_OK)

    def _get_permissions_for_category_on_instance(self, category, instance_id, request):
        instance = Instance.objects.get(pk=instance_id)
        permissions = set()

        if has_alexandria_create_permission(request, instance, category):
            permissions.add("create")

        return permissions


class PatchedMarkViewSet(views.MarkViewSet):
    permission_classes = [DefaultPermission | PublicationPermission]


class AlexandriaPermissionsDebuggerView(APIView):
    authentication_classes = []
    permission_classes = []
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "permissions.html"

    def get_actions(self) -> list[str]:
        return [
            "create",
            "update",
            "tag",
            "move",
            "replace",
            "delete",
            *[f"mark:{mark}" for mark in Mark.objects.values_list("pk", flat="True")],
        ]

    def get_permission_for(self, action: str, permissions: dict[str, Check]) -> dict:
        text = permissions.get(action)

        if not text and "mark" in action:
            text = permissions.get("mark:all")

        if not text:
            text = permissions.get("all", "Never")

        text = str(text)

        if text == "Never":
            color = "red"
        elif text == "Always":
            color = "green"
        else:
            color = "amber"

        return {"text": text, "color": color}

    def get_matrix_for(self, category: Category, access_level: AccessLevel) -> dict:
        all_permissions = settings.PERMISSIONS_ALEXANDRIA.get("ACCESS_LEVELS", {}).get(
            access_level.pk, []
        )

        relevant_permissions = {
            permission.replace(f"{category.pk}:", ""): condition
            for permission, condition in all_permissions
            if permission.startswith(f"{category.pk}:")
        }

        return {
            action: self.get_permission_for(action, relevant_permissions)
            for action in self.get_actions()
        }

    def get(self, request, **kwargs) -> Response:
        if not settings.DEBUG:  # pragma: no cover
            # Make sure to never return anything if we're not in debug mode even
            # if the url should not be registered anyways.
            raise NotFound()

        categories = Category.objects.filter(parent__isnull=True).order_by("sort")
        access_levels = AccessLevel.objects.all().order_by("name")

        matrix = {
            (category.pk, access_level.pk): self.get_matrix_for(category, access_level)
            for category in categories
            for access_level in access_levels
        }

        by = request.query_params.get("by")

        if by == "access_level":
            data = [
                {
                    "name": access_level.name,
                    "slug": access_level.pk,
                    "children": [
                        {
                            "name": category.name,
                            "slug": category.pk,
                            **matrix.get((category.pk, access_level.pk)),
                        }
                        for category in categories
                    ],
                }
                for access_level in access_levels
            ]
        else:
            data = [
                {
                    "name": category.name,
                    "slug": category.pk,
                    "children": [
                        {
                            "name": access_level.name,
                            "slug": access_level.pk,
                            **matrix.get((category.pk, access_level.pk)),
                        }
                        for access_level in access_levels
                    ],
                }
                for category in categories
            ]

        return Response(
            {
                "data": data,
                "actions": self.get_actions(),
                "by": by,
                "switch_to": "access_level" if by is None else None,
            }
        )


class AlexandriaVisibilitiesDebuggerView(APIView):
    authentication_classes = []
    permission_classes = []
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "visibilities.html"

    def get_visibility_for(self, category: Category, role: dict) -> str:
        visibility = get_dict_item(
            category.metainfo,
            f"access.{role.get('slug')}.visibility",
            default="none",
        )

        if visibility == "none":
            color = "red"
        elif visibility == "all":
            color = "green"
        else:
            color = "amber"

        return {"text": visibility, "color": color}

    def get(self, request, **kwargs) -> Response:
        if not settings.DEBUG:  # pragma: no cover
            # Make sure to never return anything if we're not in debug mode even
            # if the url should not be registered anyways.
            raise NotFound()

        # TODO: support USE_ROLE_PERMISSIONS_MAPPING and SERVICE_GROUP_APPEND_ROLE.
        # this version doesn't yet support these settings yet.
        permission_key_settings = settings.ALEXANDRIA["PERMISSION_KEY"]
        categories = Category.objects.filter(parent__isnull=True).order_by("sort")
        roles = [
            {"slug": role.slug, "name": f"{role.name}".lower()}
            for role in Role.objects.all().order_by("name")
        ]
        roles.extend(
            {
                "slug": permission_key_settings["SERVICE_GROUP_MAPPING"][service_group],
                "name": service_group,
            }
            for service_group in permission_key_settings["SERVICE_GROUP_MAPPING"]
        )
        roles = sorted(roles, key=lambda r: r["name"])

        matrix = {
            (category.pk, role.get("slug")): {
                "visibility": self.get_visibility_for(category, role)
            }
            for category in categories
            for role in roles
        }

        by = request.query_params.get("by")

        if by == "role":
            data = [
                {
                    "name": role.get("name"),
                    "slug": role.get("slug"),
                    "children": [
                        {
                            "name": category.name,
                            "slug": category.pk,
                            **matrix.get((category.pk, role.get("slug"))),
                        }
                        for category in categories
                    ],
                }
                for role in roles
            ]
        else:
            data = [
                {
                    "name": category.name,
                    "slug": category.pk,
                    "children": [
                        {
                            "name": role.get("name"),
                            "slug": role.get("slug"),
                            **matrix.get((category.pk, role.get("slug"))),
                        }
                        for role in roles
                    ],
                }
                for category in categories
            ]

        return Response(
            {
                "data": data,
                "by": by,
                "switch_to": "role" if by is None else None,
            }
        )
