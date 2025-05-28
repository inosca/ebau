from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.generics import CreateAPIView

from camac.gever.constants import ALL_AGR_SERVICE_SLUGS

from ..instance.models import Instance
from .api import GeverAPI


class GeverSyncView(CreateAPIView):
    def create(self, request, **kwargs):
        if request.group.service.slug not in ALL_AGR_SERVICE_SLUGS:
            return HttpResponse(status=status.HTTP_403_FORBIDDEN)

        # TODO: this should go throught the visibility layer instead
        instance = Instance.objects.filter(
            instance_id=kwargs.get("instance_id")
        ).first()

        if not instance:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        # TODO: This could take a while and should therefore be scheduled as
        # a background task.
        api = GeverAPI(instance)
        result = api.sync_full()
        return JsonResponse(result)
