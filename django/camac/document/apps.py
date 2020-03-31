from django.apps import AppConfig


class DefaultConfig(AppConfig):
    name = "camac.document"

    def ready(self):
        import camac.document.signals  # noqa
