from importlib import import_module

from django.apps import AppConfig


class DefaultConfig(AppConfig):
    name = "camac.instance"

    def ready(self):
        import_module("camac.alexandria.extensions.events")
