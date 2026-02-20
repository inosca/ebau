from django.apps import AppConfig


class AlexandriaConfig(AppConfig):
    name = "camac.alexandria"

    def ready(self):
        import camac.alexandria.extensions.events  # noqa: F401 imported for signales
