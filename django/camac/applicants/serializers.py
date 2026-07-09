from caluma.caluma_form.models import Document
from django.db.models import Q
from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError
from rest_framework_json_api import relations, serializers

from camac.instance.mixins import InstanceEditableMixin
from camac.instance.models import Instance
from camac.permissions.events.core import Trigger
from camac.user.models import User
from camac.user.relations import CurrentUserResourceRelatedField
from camac.user.serializers import UserSerializer

from . import models


class ApplicantSerializer(serializers.ModelSerializer, InstanceEditableMixin):
    user = CurrentUserResourceRelatedField()
    instance = relations.ResourceRelatedField(queryset=Instance.objects.all())
    invitee = relations.ResourceRelatedField(read_only=True)
    email = serializers.EmailField(required=True)

    included_serializers = {"invitee": UserSerializer, "user": UserSerializer}

    def create(self, validated_data):
        new = super().create(validated_data)
        Trigger.applicant_added(self.context["request"], new.instance, new)
        return new

    def validate(self, data):
        if data.get("role") == models.ROLE_CHOICES.PROJECT_OWNER.value:
            raise ValidationError(
                "Role Project owner can only be granted by the system."
            )

        data["email"] = data["email"].lower()

        portal_user = (
            User.objects.only_active().portal_users().get_by_email(data["email"])
        )

        data["invitee"] = portal_user

        unique_filter = (
            Q(email=data["email"])
            if data["invitee"] is None
            else Q(invitee=data["invitee"])
        )

        if data["instance"].involved_applicants.filter(unique_filter).exists():
            raise ValidationError(
                _("Email '%(email)s' has already access to instance %(instance)s")
                % {"email": data["email"], "instance": data["instance"].pk}
            )

        return data

    class Meta:
        model = models.Applicant
        fields = ("user", "instance", "invitee", "created", "email", "role", "username")
        read_only_fields = ("user", "invitee", "created", "username")


class ApplicantConfirmationSerializer(serializers.ModelSerializer):
    user = relations.SerializerMethodResourceRelatedField(
        model=User,
        read_only=True,
    )
    roles = serializers.SerializerMethodField()
    display_name = serializers.SerializerMethodField()

    def get_user(self, confirmation):
        return confirmation.user

    def get_roles(self, confirmation):
        return confirmation.roles

    def get_display_name(self, confirmation):
        return confirmation.display_name

    included_serializers = {
        "round": "camac.applicants.serializers.ApplicantConfirmationRoundSerializer",
    }

    class Meta:
        model = models.ApplicantConfirmation
        fields = (
            "applicant",
            "user",
            "round",
            "status",
            "roles",
            "display_name",
            "created_at",
            "closed_at",
        )
        read_only_fields = (
            "applicant",
            "user",
            "round",
            "status",
            "roles",
            "display_name",
            "created_at",
            "closed_at",
        )


class ApplicantConfirmationRoundSerializer(serializers.ModelSerializer):
    document = relations.ResourceRelatedField(
        required=True,
        write_only=True,
        queryset=Document.objects,
    )

    def create(self, validated_data):
        return models.ApplicantConfirmationRound.objects.start_for_document(
            validated_data["document"],
            self.context["request"],
        )

    included_serializers = {
        "confirmations": "camac.applicants.serializers.ApplicantConfirmationSerializer",
    }

    class Meta:
        model = models.ApplicantConfirmationRound
        fields = (
            "document",
            "instance",
            "confirmations",
            "step",
            "status",
            "created_at",
            "closed_at",
        )
        read_only_fields = (
            "instance",
            "confirmations",
            "step",
            "status",
            "created_at",
            "closed_at",
        )
