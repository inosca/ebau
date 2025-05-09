from caluma.caluma_form.models import Form
from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError
from rest_framework_json_api import serializers

from camac.rulesets.models import ResponsibleUserRule
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
        queryset=Service.objects.filter(service_group__name="municipality", disabled=0),
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
