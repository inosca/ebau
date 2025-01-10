from alexandria.core.models import BaseModel, Category, Document, File, Mark, Tag
from django.conf import settings
from django.db.models import CharField, Q
from django.db.models.functions import Cast
from generic_permissions.visibilities import filter_queryset_for

from camac.instance.filters import CalumaInstanceFilterSet
from camac.instance.mixins import InstanceQuerysetMixin
from camac.user.models import Service
from camac.utils import filters

from .common import get_role, get_service_parent_and_children


def get_category_access_rule(prefix, value, role=None):
    return Q(
        Q(**{f"{prefix}category__metainfo__access__has_key": role})
        & Q(**{f"{prefix}category__metainfo__access__{role}__visibility": value})
    ) | Q(
        Q(**{f"{prefix}category__parent__metainfo__access__has_key": role})
        & Q(
            **{f"{prefix}category__parent__metainfo__access__{role}__visibility": value}
        )
    )


class CustomVisibility(InstanceQuerysetMixin):
    instance_field = None

    def _all_visible_instances(self, request):
        """Fetch visible camac instances and cache the result.

        Take user's group from a custom HTTP header named `X-CAMAC-GROUP` or use
        default group  to retrieve all Camac instance IDs that are accessible.

        Return a list of instance identifiers.
        """
        result = getattr(request, "_visibility_instances_cache", None)
        if result is not None:  # pragma: no cover
            return result

        self.request = request
        filtered = CalumaInstanceFilterSet(
            data=filters(request),
            queryset=self.get_queryset(),
            request=request,
        )

        instance_ids = list(filtered.qs.values_list("pk", flat=True))

        setattr(request, "_visibility_instances_cache", instance_ids)
        return instance_ids

    @filter_queryset_for(BaseModel)
    def filter_queryset_for_all(self, queryset, request):  # pragma: no cover
        if get_role(request.group) != "public":
            return queryset

        return queryset.none()

    def document_and_file_filter(self, request, prefix=""):
        role = get_role(request.group)

        visible_instances_filter = Q(
            **{
                f"{prefix}instance_document__instance__in": self._all_visible_instances(
                    request
                )
            }
        )

        if role == "public":
            return visible_instances_filter & Q(
                **{
                    f"{prefix}marks__pk__in": settings.ALEXANDRIA[
                        "MARK_VISIBILITY"
                    ].get("PUBLIC", [])
                }
            )

        aggregated_filter = Q()
        # directly readable categories
        aggregated_filter |= get_category_access_rule(prefix, "all", role)
        # categories where only documents from my own service are readable
        aggregated_filter |= Q(
            get_category_access_rule(prefix, "service", role)
            & Q(**{f"{prefix}modified_by_group": str(request.group.service_id)})
        )
        # categories where only documents from my own service, it's parent and
        # their subservices are readable
        aggregated_filter |= Q(
            get_category_access_rule(prefix, "service-and-subservice", role)
            & Q(
                **{
                    f"{prefix}modified_by_group__in": get_service_parent_and_children(
                        request.group.service_id
                    )
                }
            )
        )

        if role == "applicant":
            # decision document available for applicants
            aggregated_filter |= Q(
                **{
                    f"{prefix}marks__pk__in": settings.ALEXANDRIA[
                        "MARK_VISIBILITY"
                    ].get("APPLICANT", [])
                }
            )

        return visible_instances_filter & aggregated_filter

    @filter_queryset_for(Document)
    def filter_queryset_for_document(self, queryset, request):
        return queryset.filter(self.document_and_file_filter(request)).distinct()

    @filter_queryset_for(File)
    def filter_queryset_for_file(self, queryset, request):
        # Limitations for `Document` should also be enforced on `File`.
        return queryset.filter(
            self.document_and_file_filter(request, "document__")
        ).distinct()

    @filter_queryset_for(Category)
    def filter_queryset_for_category(self, queryset, request):
        if "swagger" in request.path:  # pragma: no cover
            return queryset.none()

        role = get_role(request.group)
        # TODO: need to evaluate some permissions to avoid displaying categories at useless times
        return queryset.filter(
            Q(metainfo__access__has_key=role)
            | Q(parent__metainfo__access__has_key=role)
        ).order_by("metainfo__sort")

    @filter_queryset_for(Tag)
    def filter_queryset_for_tag(self, queryset, request):
        if get_role(request.group) == "support":
            return queryset

        if get_role(request.group) in ["public", "applicant"]:
            return queryset.none()

        if settings.ALEXANDRIA["TAG_VISIBILITY"] == "all":
            return queryset
        elif settings.ALEXANDRIA["TAG_VISIBILITY"] == "service-subservice":
            return queryset.filter(
                Q(
                    created_by_group__in=get_service_parent_and_children(
                        request.group.service_id
                    )
                )
                | Q(
                    created_by_group__in=Service.objects.filter(
                        service_group__name="municipality"
                    )
                    .annotate(id_string=Cast("pk", CharField()))
                    .values_list("id_string", flat=True)
                )
            )
        else:  # pragma: no cover
            raise ValueError("Unknown tag visibility setting")

    @filter_queryset_for(Mark)
    def filter_queryset_for_mark(self, queryset, request):
        if get_role(request.group) == "public":
            return queryset.filter(pk__in=settings.ALEXANDRIA["PUBLIC_MARKS"])

        return queryset.order_by("metainfo__sort")
