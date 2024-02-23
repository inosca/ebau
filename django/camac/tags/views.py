from rest_framework_json_api.views import ModelViewSet, ReadOnlyModelViewSet

from camac.instance.mixins import InstanceQuerysetMixin
from camac.user.permissions import permission_aware

from . import filters, models, serializers


class TagView(ReadOnlyModelViewSet):
    serializer_class = serializers.TagSerializer
    filterset_class = filters.TagFilterSet
    search_fields = ("name",)
    ordering = ("name",)
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


class KeywordView(ModelViewSet, InstanceQuerysetMixin):
    serializer_class = serializers.KeywordSerializer
    filterset_class = filters.KeywordFilterSet
    search_fields = ("name",)
    ordering = ("name",)
    queryset = models.Keyword.objects.all()

    @permission_aware
    def get_queryset(self):
        return super().get_queryset().none()

    def get_queryset_for_municipality(self):
        return super().get_queryset().filter(service=self.request.group.service)

    def get_queryset_for_service(self):
        return super().get_queryset().filter(service=self.request.group.service)

    def get_queryset_for_support(self):
        return super().get_queryset()
