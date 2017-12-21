from rest_framework import viewsets
from rest_framework_json_api import views

from . import models, serializers


class FormView(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.FormSerializer

    def get_queryset(self):
        # TODO: filter by permission of user
        return models.Form.objects.all()


class InstanceView(views.ModelViewSet):
    serializer_class = serializers.InstanceSerializer

    def get_queryset(self):
        # TODO: filter by permission of user
        return models.Instance.objects.all()


class FormFieldView(views.ModelViewSet):
    serializer_class = serializers.FormFieldSerializer

    def get_queryset(self):
        # TODO: filter by permission of user
        return models.FormField.objects.all()
