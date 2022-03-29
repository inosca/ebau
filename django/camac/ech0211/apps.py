from django.apps import AppConfig


class Ech0211Config(AppConfig):
    name = "camac.ech0211"

    def ready(self):
        import camac.ech0211.event_handlers  # noqa
