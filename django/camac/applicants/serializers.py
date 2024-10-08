from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError
from rest_framework_json_api import relations, serializers

from camac.instance.mixins import InstanceEditableMixin
from camac.instance.models import Instance
from camac.permissions.events import Trigger
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
        User = get_user_model()
        data["email"] = data["email"].lower()

        email_filter = Q(email=data["email"])

        if settings.ENABLE_TOKEN_EXCHANGE:
            # If token exchange is enabled, we need to make sure that only users
            # using that login method can be invited as applicants.
            email_filter &= Q(
                username__startswith=settings.TOKEN_EXCHANGE_USERNAME_PREFIX
            )

        data["invitee"] = User.objects.filter(email_filter, disabled=False).first()

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
        fields = ("user", "instance", "invitee", "created", "email", "role")
        read_only_fields = ("user", "invitee", "created")
