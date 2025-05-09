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

from camac.rulesets.models import ResponsibleUserRule
from camac.rulesets.serializers import (
    ApplicationTypeSerializer,
    ResponsibleUserRuleReorderSerializer,
    ResponsibleUserRuleSerializer,
)
from camac.utils import get_dict_item


class ApplicationTypeViewSet(ReadOnlyModelViewSet):
    serializer_class = ApplicationTypeSerializer
    queryset = Form.objects.filter(is_published=True, **{"meta__is-main-form": True})


class ResponsibleUserRuleViewSet(ModelViewSet):
    serializer_class = ResponsibleUserRuleSerializer
    queryset = ResponsibleUserRule.objects

    def has_base_permission(self) -> bool:
        return (
            self.request.group.role.name
            in get_dict_item(
                settings.RULESETS,
                "RESPONSIBLE_USER_RULE.ALLOWED_ROLES",
                default=[],
            )
            if self.request.group
            else False
        )

    def has_create_permission(self) -> bool:
        return self.has_base_permission()

    def has_reorder_permission(self) -> bool:
        return self.has_base_permission()

    def get_queryset(self) -> QuerySet[ResponsibleUserRule]:
        if not self.has_base_permission():
            return self.queryset.none()

        return self.queryset.filter(service=self.request.group.service_id)

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
