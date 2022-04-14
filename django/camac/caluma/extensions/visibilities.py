from caluma.caluma_core.visibilities import filter_queryset_for
from caluma.caluma_form import (
    historical_schema as historical_form_schema,
    schema as form_schema,
)
from caluma.caluma_user.visibilities import Authenticated
from caluma.caluma_workflow import schema as workflow_schema
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db.models import Case, Exists, F, Func, IntegerField, OuterRef, Q, When
from django.db.models.functions import Cast

from camac.caluma.utils import CamacRequest
from camac.constants.kt_bern import DASHBOARD_FORM_SLUG
from camac.instance.filters import CalumaInstanceFilterSet
from camac.instance.mixins import InstanceQuerysetMixin
from camac.user.models import Role, Service
from camac.utils import filters, order


class CustomVisibility(Authenticated, InstanceQuerysetMixin):
    """Custom visibility for Kanton Bern.

    To avoid multiple db lookups, the result is cached in the
    request object, and reused if the need arises. Caching beyond a request is
    not done but might become a future optimisation.
    """

    instance_field = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group = None
        self.user = None
        self.request = None

    @filter_queryset_for(form_schema.Question)
    @filter_queryset_for(form_schema.Form)
    @filter_queryset_for(form_schema.Option)
    @filter_queryset_for(form_schema.DynamicOption)
    def filter_queryset_public(self, node, queryset, info):
        # this is blueprint data which is uncritical and can be exposed publicly
        return queryset

    @filter_queryset_for(form_schema.Document)
    @filter_queryset_for(historical_form_schema.HistoricalDocument)
    def filter_queryset_for_document(self, node, queryset, info):
        instance_ids = self._all_visible_instances(info)

        return queryset.filter(
            # document is accessible through CAMAC ACLs
            Q(family__case__family__instance__pk__in=instance_ids)
            | Q(family__work_item__case__family__instance__pk__in=instance_ids)
            # OR dashboard documents
            | Q(form_id=DASHBOARD_FORM_SLUG)
            # OR unlinked table documents created by the requesting user
            | Q(
                family__case__instance__isnull=True,
                family=F("pk"),
                created_by_user=info.context.user.username,
            )
        )

    @filter_queryset_for(form_schema.Answer)
    @filter_queryset_for(historical_form_schema.HistoricalAnswer)
    def filter_queryset_for_answer(self, node, queryset, info):
        # return all answers, since answers can only be accessed via documents
        # which are already properly protected
        return queryset

    @filter_queryset_for(workflow_schema.Case)
    def filter_queryset_for_case(self, node, queryset, info):
        # Child cases are used for instances in circulation but
        # shouldn't be returned for cases list (marked by the
        # exclude_child_cases)
        exclude_child_cases = filters(CamacRequest(info).request).get(
            "exclude_child_cases"
        )
        order_by = order(CamacRequest(info).request)

        filter = Q(family__instance__pk__in=self._all_visible_instances(info))
        if exclude_child_cases == "true":
            filter = filter & Q(parent_work_item__isnull=True)

        return (
            queryset.filter(filter).order_by(*order_by)
            if order_by
            else queryset.filter(filter)
        )

    @filter_queryset_for(workflow_schema.WorkItem)
    def filter_queryset_for_work_items(self, node, queryset, info):
        return queryset.filter(
            case__family__instance__pk__in=self._all_visible_instances(info)
        )

    def _all_visible_instances(self, info):
        """Fetch visible camac instances and cache the result.

        Take user's group from a custom HTTP header named `X-CAMAC-GROUP` or use
        default group  to retrieve all Camac instance IDs that are accessible.

        Return a list of instance identifiers.
        """
        result = getattr(info.context, "_visibility_instances_cache", None)
        if result is not None:  # pragma: no cover
            return result

        self.request = CamacRequest(info).request

        filtered = CalumaInstanceFilterSet(
            data=filters(self.request),
            queryset=self.get_queryset(),
            request=self.request,
        )

        instance_ids = filtered.qs.values_list("pk", flat=True)

        setattr(info.context, "_visibility_instances_cache", instance_ids)
        return instance_ids


class CustomVisibilitySZ(CustomVisibility):
    """Custom visibility for Kanton Schwyz.

    Form visibility rules are defined in the form meta.
    Possible configurations are shown below.
    Note: If no visibility is configured for a form,
    the form is by default NOT returned.

    Visible for internal roles:
    "meta": {
        "visibility": {
            "type": "internal"
        }
    },

    Publicly visible:
    "meta": {
        "visibility": {
            "type": "public"
        }
    },

    Visible for certain roles and services:
    * Request user needs to belong to one of the
    specified roles OR services:
    "meta": {
        "visibility": {
            "type": "specific",
            "visibleFor": {
                "roles": [3],
                "services": [6]
            }
        }
    },

    * Request user needs to belong to one of the specified
    roles, service is not relevant:
    "meta": {
        "visibility": {
            "type": "specific",
            "visibleFor": {
                "roles": [3, 4]
            }
        }
    },

    * Request user needs to belong to one of the specified
    services, role is not relevant:
    "meta": {
        "visibility": {
            "type": "specific",
            "visibleFor": {
                "services": [6, 7]
            }
        }
    },

    TODO: More generic future design
    To make the configurable visibility / permission feature
    usable for the other cantons, a few things need to be adapted:

    * Use "permissions" instead of "visibility" on form meta:

        "meta": {
            "createPermission": {
                "type": "public"
            }
        },

    * Read from and check permission config in instance serializer
        (create method), throw exception if permission is missing

    * Filter forms based on create permission in frontend
    """

    @filter_queryset_for(form_schema.Form)
    def filter_queryset_for_form(self, node, queryset, info):

        camac_request = CamacRequest(info).request
        camac_role = camac_request.group.role.role_id
        camac_service = camac_request.group.service_id

        # public filter: visible to all
        public_filter = Q(meta__visibility__type="public")

        # internal filter: excludes configured public roles
        public_roles = [
            role.role_id
            for role in Role.objects.filter(
                name__in=settings.APPLICATION.get("PUBLIC_ROLES", [])
            )
        ]
        internal_forms = (
            [form.slug for form in queryset.filter(meta__visibility__type="internal")]
            if camac_role not in public_roles
            else []
        )
        internal_filter = Q(slug__in=internal_forms)

        # specific filter: visible to specific roles or services
        specific_filter = Q(
            meta__visibility__type="specific",
            meta__visibility__visibleFor__roles__contains=[camac_role],
        ) | Q(
            meta__visibility__type="specific",
            meta__visibility__visibleFor__services__contains=[camac_service],
        )

        return queryset.filter(public_filter | internal_filter | specific_filter)

    @filter_queryset_for(form_schema.Question)
    @filter_queryset_for(form_schema.Option)
    @filter_queryset_for(form_schema.DynamicOption)
    def filter_queryset_public(self, node, queryset, info):
        # this is blueprint data which is uncritical and can be exposed publicly
        return queryset

    @filter_queryset_for(workflow_schema.WorkItem)
    def filter_queryset_for_work_items(self, node, queryset, info):
        visibility_config = settings.APPLICATION.get("INTER_SERVICE_GROUP_VISIBILITIES")

        service = CamacRequest(info).request.group.service

        # If the work-item task is "inquiry", check if the current service
        # is either in the controlling_groups or addressed_groups. If not, then
        # check if the current service is permitted to see the work-item
        # according to its service_group
        return queryset.filter(
            Case(
                When(
                    Q(task_id=settings.DISTRIBUTION["INQUIRY_TASK"])
                    & ~Q(addressed_groups__contains=[service.pk])
                    & ~Q(controlling_groups__contains=[service.pk]),
                    then=Exists(
                        Service.objects.filter(
                            # Use element = ANY(array) operator to check if
                            # element is present in ArrayField, which requires
                            # lhs and rhs of expression to be of same type
                            pk=Func(
                                Cast(
                                    OuterRef("addressed_groups"),
                                    output_field=ArrayField(IntegerField()),
                                ),
                                function="ANY",
                            ),
                            service_group__pk__in=visibility_config.get(
                                service.service_group_id, []
                            ),
                        )
                    ),
                ),
                default=True,
            ),
            case__family__instance__pk__in=self._all_visible_instances(info),
        )
