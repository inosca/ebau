from caluma.caluma_core.visibilities import filter_queryset_for
from caluma.caluma_form import (
    historical_schema as historical_form_schema,
    schema as form_schema,
)
from caluma.caluma_user.visibilities import Authenticated
from caluma.caluma_workflow import models as workflow_models, schema as workflow_schema
from django.conf import settings
from django.db.models import F, Q

from camac.caluma.utils import CamacRequest, visible_inquiries_expression
from camac.constants.kt_bern import DASHBOARD_FORM_SLUG
from camac.instance.filters import CalumaInstanceFilterSet
from camac.instance.mixins import InstanceQuerysetMixin
from camac.user.models import Role
from camac.user.permissions import permission_aware
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

    def filter_queryset(self, node, queryset, info):
        if not getattr(info.context, "camac_request", None):
            info.context.camac_request = CamacRequest(info).request

        self.request = info.context.camac_request

        return super().filter_queryset(node, queryset, info)

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

    @permission_aware
    @filter_queryset_for(form_schema.Answer)
    @filter_queryset_for(historical_form_schema.HistoricalAnswer)
    def filter_queryset_for_answer(self, node, queryset, info):
        # return all answers, since answers can only be accessed via documents
        # which are already properly protected
        return queryset

    def filter_queryset_for_answer_for_public(self, node, queryset, info):
        # Scrub sensitive data from answer queryset for public users
        return queryset.exclude(
            question_id__in=settings.PUBLICATION.get("SCRUBBED_ANSWERS", [])
        )

    @filter_queryset_for(workflow_schema.Case)
    def filter_queryset_for_case(self, node, queryset, info):
        order_by = order(self.request)

        queryset = queryset.filter(
            family__instance__pk__in=self._all_visible_instances(info)
        )

        return queryset.order_by(*order_by) if order_by else queryset

    @filter_queryset_for(workflow_schema.WorkItem)
    def filter_queryset_for_work_items(self, node, queryset, info):
        filters = Q(case__family__instance__pk__in=self._all_visible_instances(info))
        if settings.DISTRIBUTION:
            # Provide additional filtering for inquiry work-items
            filters &= ~Q(task_id=settings.DISTRIBUTION["INQUIRY_TASK"]) | (
                Q(task_id=settings.DISTRIBUTION["INQUIRY_TASK"])
                & visible_inquiries_expression(self.request.group)
            )

        if settings.ADDITIONAL_DEMAND:
            filters &= self.visible_additional_demands_expression(self.request.group)

        return queryset.filter(filters).distinct()

    def _all_visible_instances(self, info):
        """Fetch visible camac instances and cache the result.

        Take user's group from a custom HTTP header named `X-CAMAC-GROUP` or use
        default group  to retrieve all Camac instance IDs that are accessible.

        Return a list of instance identifiers.
        """
        result = getattr(info.context, "_visibility_instances_cache", None)
        if result is not None:  # pragma: no cover
            return result

        filtered = CalumaInstanceFilterSet(
            data=filters(self.request),
            queryset=self.get_queryset(),
            request=self.request,
        )

        instance_ids = list(filtered.qs.values_list("pk", flat=True))

        setattr(info.context, "_visibility_instances_cache", instance_ids)
        return instance_ids

    def visible_additional_demands_expression(self, group):
        if settings.APPLICATION.get("PORTAL_GROUP") == self.request.group.pk:
            return (
                ~Q(task_id=settings.ADDITIONAL_DEMAND["TASK"])
                | Q(
                    task_id=settings.ADDITIONAL_DEMAND["TASK"],
                    child_case__work_items__task_id=settings.ADDITIONAL_DEMAND[
                        "FILL_TASK"
                    ],
                )
            ) & (
                ~Q(
                    task_id__in=[
                        settings.ADDITIONAL_DEMAND["CHECK_TASK"],
                        settings.ADDITIONAL_DEMAND["SEND_TASK"],
                    ]
                )
                | Q(
                    task_id__in=[
                        settings.ADDITIONAL_DEMAND["CHECK_TASK"],
                        settings.ADDITIONAL_DEMAND["SEND_TASK"],
                    ],
                    status=workflow_models.WorkItem.STATUS_COMPLETED,
                )
            )
        else:
            return ~Q(task_id=settings.ADDITIONAL_DEMAND["FILL_TASK"]) | Q(
                task_id=settings.ADDITIONAL_DEMAND["FILL_TASK"],
                status=workflow_models.WorkItem.STATUS_COMPLETED,
            )


class CustomVisibilitySZ(CustomVisibility):
    """Custom visibility for Kanton Schwyz.

    Form visibility rules are defined in the form meta.
    Possible configurations are shown below.
    Note: If no visibility is configured for a form,
    the form is visible by default.

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
        camac_role = self.request.group.role.role_id
        camac_service = self.request.group.service_id

        default_filter = Q(meta__visibility__isnull=True)

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

        return queryset.filter(
            default_filter | public_filter | internal_filter | specific_filter
        )

    @filter_queryset_for(form_schema.Question)
    @filter_queryset_for(form_schema.Option)
    @filter_queryset_for(form_schema.DynamicOption)
    def filter_queryset_public(self, node, queryset, info):
        # this is blueprint data which is uncritical and can be exposed publicly
        return queryset


class CustomVisibilityBE(CustomVisibility):
    pass
