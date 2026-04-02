import json

from django.core.management import call_command


def test_translate(db, tmp_path):
    ORIG_FILE = "camac/core/tests/untranslated_config.json"

    work_file = tmp_path / "test_config.json"

    with open(ORIG_FILE, "rb") as fh_in, open(work_file, "wb") as fh_out:
        fh_out.write(fh_in.read())

    call_command("translate_caluma", work_file)

    with open(work_file, "r+") as file:
        data = json.load(file)

    item = next((item for item in data if item["pk"] == "werden-siloanlagen-erstellt"))
    untranslated_item = next((item for item in data if item["pk"] == "Test"))

    assert json.loads(item["fields"]["label"])["de"] == "Werden Siloanlagen erstellt?"
    assert json.loads(item["fields"]["label"])["fr"] == "Des silos sont-ils prévus?"
    assert json.loads(untranslated_item["fields"]["label"])["de"] == "Test abc"
