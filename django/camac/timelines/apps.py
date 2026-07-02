from django.apps import AppConfig


class TimelinesConfig(AppConfig):
    name = "camac.timelines"

    def ready(self):
        import camac.timelines.events  # noqa: F401
