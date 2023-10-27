from alexandria.core.models import BaseModel, Category, Document, File, Tag
from alexandria.core.visibilities import BaseVisibility, filter_queryset_for
from django.db.models import Q

from camac.instance.filters import CalumaInstanceFilterSet
from camac.instance.mixins import InstanceQuerysetMixin
from camac.settings import ALEXANDRIA
from camac.utils import filters

from .common import get_role


def get_category_access_rule(prefix, value, role=None, lookup=None):
    query = (
        f"metainfo__access__{role}__{lookup}" if role else "metainfo__access__has_key"
    )

    return Q(
        Q(**{f"{prefix}category__{query}": value})
        | Q(**{f"{prefix}category__parent__{query}": value})
    )


class CustomVisibility(BaseVisibility, InstanceQuerysetMixin):
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
        if get_role(request.caluma_info.context.user) != "public":
            return queryset

        return queryset.none()

    def document_and_file_filter(self, request, prefix=""):
        user = request.caluma_info.context.user
        role = get_role(user)

        visible_instances_filter = Q(
            **{
                f"{prefix}instance_document__instance__in": self._all_visible_instances(
                    request
                )
            }
        )

        if role == "public":
            return visible_instances_filter & Q(
                **{f"{prefix}tags__pk": ALEXANDRIA["MARKS"]["PUBLICATION"]}
            )

        aggregated_filter = Q()
        normal_permissions = ["Admin", "Read", "Write"]
        for permission in normal_permissions:
            # directly readable categories
            aggregated_filter |= get_category_access_rule(
                prefix, permission, role, "istartswith"
            )

        if role == "applicant":
            # decision document available for applicants
            aggregated_filter |= Q(
                **{f"{prefix}tags__pk": ALEXANDRIA["MARKS"]["DECISION"]}
            )

        return visible_instances_filter & (
            aggregated_filter
            | Q(
                # categories where only documents from my own service are readable
                get_category_access_rule(prefix, "Internal", role, "icontains")
                & Q(**{f"{prefix}created_by_group": user.group})
            )
        )

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

        role = get_role(request.caluma_info.context.user)
        # TODO: need to evaluate some permissions to avoid displaying categories at useless times
        return queryset.filter(
            Q(metainfo__access__has_key=role)
            | Q(parent__metainfo__access__has_key=role)
        ).order_by("metainfo__sort")

    @filter_queryset_for(Tag)
    def filter_queryset_for_tag(self, queryset, request):
        if get_role(request.caluma_info.context.user) == "support":
            return queryset

        if get_role(request.caluma_info.context.user) in ["public", "applicant"]:
            return queryset.none()

        return queryset.filter(
            Q(created_by_group=request.caluma_info.context.user.group)
            | Q(pk__in=ALEXANDRIA["MARKS"]["ALL"])
        )
