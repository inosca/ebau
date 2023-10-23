from importlib import import_module

from django.apps import AppConfig

from camac.user.permissions import DefaultPermission, PublicationPermission


class AlexandriaConfig(AppConfig):
    name = "camac.alexandria"

    def ready(self):
        import_module("camac.alexandria.extensions.events")
        from alexandria.core import views

        views.DocumentViewSet.permission_classes = [
            DefaultPermission | PublicationPermission
        ]
        views.FileViewSet.permission_classes = [
            DefaultPermission | PublicationPermission
        ]
