import json

from django.core.management import call_command


def test_translate(db):
    with open("camac/core/tests/untranslated_config.json", "r+") as file:
        original_data = json.load(file)

        call_command("translate_caluma", "camac/core/tests/untranslated_config.json")

    with open("camac/core/tests/untranslated_config.json", "r+") as file:
        data = json.load(file)

        item = next(
            (item for item in data if item["pk"] == "werden-siloanlagen-erstellt")
        )
        untranslated_item = next((item for item in data if item["pk"] == "Test"))

        # reset file content
        file.seek(0)
        json.dump(original_data, file, ensure_ascii=False, indent=2)

        assert (
            json.loads(item["fields"]["label"])["de"] == "Werden Siloanlagen erstellt?"
        )
        assert json.loads(item["fields"]["label"])["fr"] == "Des silos sont-ils prévus?"
        assert json.loads(untranslated_item["fields"]["label"])["de"] == "Test abc"
