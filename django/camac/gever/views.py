from django.conf import settings
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.generics import CreateAPIView

from ..instance.models import Instance
from .api import GeverAPI


class GeverSyncView(CreateAPIView):
    def create(self, request, **kwargs):  # pragma: no cover
        all_agr_groups = (
            settings.GEVER["AGR_GROUPS"] + settings.GEVER["AGR_SHOOTING_GROUPS"]
        )
        if request.group.pk not in all_agr_groups:
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
