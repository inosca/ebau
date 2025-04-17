from django.conf import settings
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.generics import CreateAPIView

from ..instance.models import Instance
from .api import GeverAPI


class GeverSyncView(CreateAPIView):
    def create(self, request, **kwargs):
        if request.group.service_id not in settings.APPLICATION["AGR_GROUPS"]:
            return HttpResponse(status=status.HTTP_403_FROBIDDEN)

        instance = Instance.objects.filter(
            instance_id=kwargs.get("instance_id")
        ).first()

        if not instance:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        api = GeverAPI(instance)
        result = api.sync_full(instance)
        return JsonResponse(result)
