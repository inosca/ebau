from django.apps import AppConfig


class RulesetsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "camac.rulesets"

    def ready(self):
        import camac.rulesets.signals  # noqa: F401
