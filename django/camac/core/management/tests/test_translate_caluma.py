import json

from django.core.management import call_command


def test_translate(db):

    with open("camac/core/management/tests/untranslated_config.json", "r") as file:
        data = json.load(file)

        call_command(
            "translate_caluma", "camac/core/management/tests/untranslated_config.json"
        )

        item = next(
            (item for item in data if item["pk"] == "werden-siloanlagen-erstellt")
        )

        assert (
            json.loads(item["fields"]["label"])["de"] == "Werden Siloanlagen erstellt?"
        )
        assert json.loads(item["fields"]["label"])["fr"] == "Des silos sont-ils prévus?"
