from rest_framework import viewsets
from rest_framework_json_api import views

from camac.core.models import Circulation
from camac.user.permissions import permission_aware

from . import models, serializers


class FormView(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.FormSerializer

    def get_queryset(self):
        return models.Form.objects.all()


class InstanceView(views.ModelViewSet):
    serializer_class = serializers.InstanceSerializer

    @permission_aware
    def get_queryset(self):
        return models.Instance.objects.none()

    def get_queryset_for_applicant(self):
        return models.Instance.objects.filter(
            user=self.request.user
        )

    def get_queryset_for_municipality(self):
        instances = models.Instance.locations.through.objects.filter(
            location=self.request.group.locations.all()
        ).values('instance')
        # use subquery to avoid duplicates
        return models.Instance.objects.filter(
            pk__in=instances
        )

    def get_queryset_for_service(self):
        instances = Circulation.objects.filter(
            activations__service=self.request.group.service
        ).values('instance')
        # use subquery to avoid duplicates
        return models.Instance.objects.filter(
            pk__in=instances
        )

    def get_queryset_for_canton(self):
        return models.Instance.objects.all()


class FormFieldView(views.ModelViewSet):
    serializer_class = serializers.FormFieldSerializer

    def get_queryset(self):
        # TODO: filter by permission of user
        return models.FormField.objects.all()
