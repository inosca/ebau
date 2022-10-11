from django.conf import settings
from django.forms import BooleanField, ChoiceField


class CamacLanguageField(ChoiceField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = settings.LANGUAGES


class CamacBooleanField(BooleanField):
    def prepare_value(self, value):
        return value == 1

    def clean(self, value):
        return 1 if super.clean(value) else 0
