from django.conf import settings
from rest_framework_json_api.views import ModelViewSet

from camac.instance.mixins import InstanceQuerysetMixin
from camac.notification.utils import send_mail
from camac.user.permissions import permission_aware

from . import filters, models, serializers


class ApplicantsView(InstanceQuerysetMixin, ModelViewSet):
    swagger_schema = None
    filterset_class = filters.ApplicantFilterSet
    serializer_class = serializers.ApplicantSerializer
    queryset = models.Applicant.objects.all().select_related(
        "invitee", "instance", "instance__instance_state"
    )
    prefetch_for_includes = {"invitee": ["service"], "user": ["service"]}

    def create(self, request):
        created = super().create(request)

        # send notification email when configured
        notification_template = settings.APPLICATION["NOTIFICATIONS"]["APPLICANT"][
            "EXISTING" if created.data["invitee"] else "NEW"
        ]
        if notification_template:
            send_mail(
                notification_template,
                self.get_serializer_context(),
                recipient_types=["email_list"],
                email_list=created.data["email"],
                instance={"id": created.data["instance"]["id"], "type": "instances"},
            )

        return created

    @permission_aware
    def has_create_permission(self):
        return True

    def has_create_permission_for_municipality(self):
        return False

    def has_create_permission_for_service(self):
        return False

    def has_create_permission_for_canton(self):
        return False

    def has_update_permission(self):
        return False

    @permission_aware
    def has_object_destroy_permission(self, obj):
        # it should not be possible to delete the last involved applicant to
        # prevent having an instance without a user having access to it
        return obj.instance.involved_applicants.count() > 1

    def has_object_destroy_permission_for_municipality(self, obj):
        return False

    def has_object_destroy_permission_for_service(self, obj):
        return False

    def has_object_destroy_permission_for_canton(self, obj):
        return False

    def has_object_destroy_permission_for_support(self, obj):
        return True
