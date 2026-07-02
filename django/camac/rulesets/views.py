from typing import TYPE_CHECKING

from caluma.caluma_form.models import Form
from django.conf import settings
from django.db import transaction
from django.db.models import QuerySet
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_json_api.views import ModelViewSet, ReadOnlyModelViewSet

from camac.rulesets.filters import DistributionDeadlineRuleFilterSet
from camac.rulesets.models import DistributionDeadlineRule, ResponsibleUserRule
from camac.rulesets.serializers import (
    ApplicationTypeSerializer,
    DistributionDeadlineRuleSerializer,
    ResponsibleUserRuleReorderSerializer,
    ResponsibleUserRuleSerializer,
)
from camac.user.permissions import permission_aware

if TYPE_CHECKING:
    from camac.settings.modules.rulesets_schema import (
        DistributionDeadlineRuleConfig,
        ResponsibleUserRuleConfig,
    )


class ApplicationTypeViewSet(ReadOnlyModelViewSet):
    serializer_class = ApplicationTypeSerializer
    queryset = Form.objects.filter(is_published=True, **{"meta__is-main-form": True})


class ResponsibleUserRuleViewSet(ModelViewSet):
    serializer_class = ResponsibleUserRuleSerializer
    queryset = ResponsibleUserRule.objects

    prefetch_for_includes = {
        "municipalities": ["municipalities__trans"],
    }

    def has_base_permission(self) -> bool:
        module_settings: ResponsibleUserRuleConfig = (
            settings.RULESETS.responsible_user_rule
        )

        return (
            self.request.group.role.name in module_settings.allowed_roles
            if self.request.group
            else False
        )

    def has_create_permission(self) -> bool:
        return self.has_base_permission()

    def has_reorder_permission(self) -> bool:
        return self.has_base_permission()

    def get_queryset(self) -> QuerySet[ResponsibleUserRule]:
        queryset = super().get_queryset()

        if not self.has_base_permission():
            return queryset.none()

        return queryset.filter(service=self.request.group.service_id)

    def perform_destroy(self, instance: ResponsibleUserRule) -> None:
        super().perform_destroy(instance)

        # Update the sort property of all remaining entries for this service so
        # we don't have any gaps in the ordering
        for i, entry in enumerate(
            ResponsibleUserRule.objects.filter(service=instance.service)
        ):
            entry.sort = i
            entry.save(update_fields=["sort"])

    @action(
        methods=["POST"],
        detail=False,
        serializer_class=ResponsibleUserRuleReorderSerializer,
    )
    @transaction.atomic()
    def reorder(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_order = serializer.data["order"]
        queryset = self.get_queryset()

        ids = set(queryset.values_list("pk", flat=True))

        if ids - set(new_order):
            raise ValidationError(_("`order` must include all IDs"))
        elif set(new_order) - ids:
            raise ValidationError(_("`order` contains inexistent IDs"))

        all_rules = sorted(
            queryset.iterator(),
            key=lambda rule: new_order.index(rule.pk),
        )

        # Since the unique toghether constraint will prevent us from updating
        # the sort property directly, we need to temporarily assign a large
        # offset that will not collide with current sort properties. After that,
        # we can normally assign our new order.
        tmp_offset = 99999
        for i, rule in enumerate(all_rules):
            rule.sort = tmp_offset - i
        ResponsibleUserRule.objects.bulk_update(all_rules, fields=["sort"])

        for i, rule in enumerate(all_rules):
            rule.sort = i
        ResponsibleUserRule.objects.bulk_update(all_rules, fields=["sort"])

        return Response(status=status.HTTP_204_NO_CONTENT)


class DistributionDeadlineRuleViewSet(ModelViewSet):
    serializer_class = DistributionDeadlineRuleSerializer
    filterset_class = DistributionDeadlineRuleFilterSet
    queryset = DistributionDeadlineRule.objects
    ordering = ["pk"]

    select_for_includes = {
        "__all__": ["target_service", "target_service__service_group"],
    }
    prefetch_for_includes = {
        "target_service": ["target_service__trans"],
    }

    @permission_aware
    def get_queryset(self) -> QuerySet[DistributionDeadlineRule]:
        return (
            super().get_queryset().filter(source_service=self.request.group.service_id)
        )

    def get_queryset_for_applicant(self) -> QuerySet[DistributionDeadlineRule]:
        return super().get_queryset().none()

    def has_base_permission(self) -> bool:
        module_settings: DistributionDeadlineRuleConfig = (
            settings.RULESETS.distribution_deadline_rule
        )

        return (
            self.request.group.role.name in module_settings.allowed_roles
            if self.request.group
            else False
        )

    def has_create_permission(self) -> bool:
        return self.has_base_permission()

    def has_object_update_permission(self, obj: DistributionDeadlineRule) -> bool:
        return self.has_base_permission()

    def has_object_destroy_permission(self, obj: DistributionDeadlineRule) -> bool:
        return self.has_base_permission()
