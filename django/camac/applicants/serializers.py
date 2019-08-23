from django.contrib.auth import get_user_model
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from rest_framework_json_api import relations, serializers

from camac.instance.mixins import InstanceEditableMixin
from camac.instance.models import Instance
from camac.user.relations import CurrentUserResourceRelatedField
from camac.user.serializers import UserSerializer

from . import models


class ApplicantSerializer(serializers.ModelSerializer, InstanceEditableMixin):
    user = CurrentUserResourceRelatedField()
    instance = relations.ResourceRelatedField(queryset=Instance.objects.all())
    invitee = relations.ResourceRelatedField(read_only=True)

    email = serializers.EmailField(required=True, write_only=True)

    included_serializers = {"invitee": UserSerializer, "user": UserSerializer}

    def validate(self, data):
        email = data.pop("email")

        try:
            data["invitee"] = get_user_model().objects.get(disabled=False, email=email)
        except ObjectDoesNotExist:
            raise ValidationError(f"User with email '{email}' could not be found")
        except MultipleObjectsReturned:
            raise ValidationError(
                f"There is more than one user with the email '{email}'"
            )

        if (
            data["instance"]
            .involved_applicants.filter(invitee=data["invitee"])
            .exists()
        ):
            raise ValidationError(
                f"User with email '{email}' has already access to instance {data['instance'].pk}"
            )

        return data

    class Meta:
        model = models.Applicant
        fields = ("user", "instance", "invitee", "created", "email")
        read_only_fields = ("user", "invitee", "created")
        write_only_fields = ("email",)
