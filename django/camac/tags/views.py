from rest_framework_json_api.views import ReadOnlyModelViewSet

from camac.user.permissions import permission_aware

from . import models, serializers


class TagView(ReadOnlyModelViewSet):
    swagger_schema = None
    serializer_class = serializers.TagSerializer
    queryset = models.Tags.objects.all()

    @permission_aware
    def get_queryset(self):
        return super().get_queryset().none()

    def get_queryset_for_municipality(self):
        return super().get_queryset().filter(service=self.request.group.service)

    def get_queryset_for_service(self):
        return super().get_queryset().filter(service=self.request.group.service)

    def get_queryset_for_support(self):
        return super().get_queryset()
