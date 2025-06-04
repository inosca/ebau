from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.generics import CreateAPIView

from camac.gever import events as gever_events
from camac.gever.utils import get_all_agr_service_slugs

from ..instance.models import Instance


class GeverSyncView(CreateAPIView):
    def create(self, request, **kwargs):
        if request.group.service.slug not in get_all_agr_service_slugs():
            return HttpResponse(status=status.HTTP_403_FORBIDDEN)

        # TODO: this should go throught the visibility layer instead
        instance = Instance.objects.filter(
            instance_id=kwargs.get("instance_id")
        ).first()

        if not instance:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        # TODO: We should probably just use a custom model to store all
        # sync operations on a dossier, for future retrieval
        task_id = gever_events.sync_button_pressed(instance)

        return JsonResponse({"scheduled": True, "task_id": task_id})
