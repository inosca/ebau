from django.apps import AppConfig


class EchbernConfig(AppConfig):
    name = "camac.echbern"

    def ready(self):
        import camac.echbern.event_handlers  # noqa
