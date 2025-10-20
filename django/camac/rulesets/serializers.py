from datetime import date

from caluma.caluma_form.models import Form
from django.conf import settings
from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError
from rest_framework_json_api import serializers

from camac.rulesets.models import DistributionDeadlineRule, ResponsibleUserRule
from camac.user.models import Service, User


class ApplicationTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Form
        fields = ["name"]
        resource_name = "application-types"


class ResponsibleUserRuleSerializer(serializers.ModelSerializer):
    application_types = serializers.ResourceRelatedField(
        required=False,
        many=True,
        queryset=Form.objects.filter(is_published=True, **{"meta__is-main-form": True}),
    )
    municipalities = serializers.ResourceRelatedField(
        required=False,
        many=True,
        queryset=Service.objects.municipalities_for_rulesets(),
    )

    def validate(self, data: dict) -> dict:
        validated_data = super().validate(data)

        municipalities = validated_data.get(
            "municipalities",
            self.instance.municipalities.all() if self.instance else [],
        )
        application_types = validated_data.get(
            "application_types",
            self.instance.application_types.all() if self.instance else [],
        )

        if not municipalities and not application_types:
            raise ValidationError(
                _("Municipalities and application types can't both be empty")
            )
        elif municipalities and application_types:
            raise ValidationError(
                _("Municipalities and application types can't both be set")
            )

        return validated_data

    def validate_responsible_user(self, user: User) -> User:
        if not user.groups.filter(
            service=self.context["request"].group.service
        ).exists():
            raise ValidationError(_("User is not a member of this service"))

        return user

    def create(self, validated_data: dict) -> ResponsibleUserRule:
        validated_data["service"] = self.context["request"].group.service

        last_sort = (
            ResponsibleUserRule.objects.filter(service=validated_data["service"])
            .order_by("-sort")
            .values_list("sort", flat=True)
            .first()
        )

        validated_data["sort"] = last_sort + 1 if last_sort is not None else 0

        return super().create(validated_data)

    included_serializers = {
        "application_types": "camac.rulesets.serializers.ApplicationTypeSerializer",
        "municipalities": "camac.user.serializers.PublicServiceSerializer",
        "responsible_user": "camac.user.serializers.UserSerializer",
    }

    class Meta:
        model = ResponsibleUserRule
        exclude = ["service"]
        read_only_fields = ["sort"]


class ResponsibleUserRuleReorderSerializer(serializers.Serializer):
    order = serializers.ListField(child=serializers.IntegerField(min_value=0))

    class Meta:
        resource_name = "responsible-user-rule-reorders"


class DistributionDeadlineRuleSerializer(serializers.ModelSerializer):
    exclude_holidays = serializers.SerializerMethodField()
    deadline = serializers.SerializerMethodField()
    target_service = serializers.ResourceRelatedField(queryset=Service.objects)

    def get_exclude_holidays(self, rule: DistributionDeadlineRule) -> bool:
        return rule.should_exclude_holidays()

    def get_deadline(self, rule: DistributionDeadlineRule) -> date:
        return rule.get_deadline()

    def validate_target_service(self, service):
        if (
            service.service_group.name
            in settings.DISTRIBUTION.get(
                "DEADLINE_LEAD_TIME_FOR_ADDRESSED_SERVICE_GROUPS", {}
            ).keys()
            or service.slug
            in settings.DISTRIBUTION.get(
                "DEADLINE_LEAD_TIME_FOR_ADDRESSED_SERVICES", {}
            ).keys()
        ):
            raise ValidationError(
                _("Defining a deadline rule for this service is not allowed")
            )

        existing = DistributionDeadlineRule.objects.filter(
            target_service=service,
        )

        if self.instance:
            existing = existing.filter(
                source_service=self.instance.source_service
            ).exclude(pk=self.instance.pk)
        else:
            existing = existing.filter(
                source_service=self.context["request"].group.service,
            )

        if existing.exists():
            raise ValidationError(
                _("There is already a deadline rule defined for this service")
            )

        return service

    def create(self, validated_data: dict) -> DistributionDeadlineRule:
        validated_data["source_service"] = self.context["request"].group.service

        return super().create(validated_data)

    included_serializers = {
        "target_service": "camac.user.serializers.PublicServiceSerializer",
    }

    class Meta:
        model = DistributionDeadlineRule
        exclude = ["source_service"]
        read_only_fields = ["deadline"]
