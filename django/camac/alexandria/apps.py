from importlib import import_module

from django.apps import AppConfig


class AlexandriaConfig(AppConfig):
    name = "camac.alexandria"

    def ready(self):
        # load signals
        import_module("camac.alexandria.extensions.events")
