import csv
import json

from django.core.management.base import BaseCommand

sources = [
    "camac/core/translation_files/question_t.csv",
    "camac/core/translation_files/chapter_t.csv",
    "camac/core/translation_files/file_content_t.csv",
    "camac/core/translation_files/form_t.csv",
    "camac/core/translation_files/answer_list_t.csv",
    "camac/core/translation_files/instance_resource_t.csv",
    "camac/core/translation_files/resource_t.csv",
    "camac/core/translation_files/file_complement_state_t.csv",
    "camac/core/translation_files/circulation_answer_t.csv",
    "camac/core/translation_files/button_t.csv",
    "camac/core/translation_files/action_t.csv",
    "camac/core/translation_files/file_content_category_t.csv",
    "camac/core/translation_files/instance_state_t.csv",
    "camac/core/translation_files/journal_action_config_t.csv",
    "camac/core/translation_files/notice_type_t.csv",
    "camac/core/translation_files/notification_template_t.csv",
    "camac/core/translation_files/page_form_group_t.csv",
    "camac/core/translation_files/page_t.csv",
    "camac/core/translation_files/role_t.csv",
    "camac/core/translation_files/missing_translations.csv",
]
properties = [("question", "label"), ("form", "name"), ("option", "label")]


def _load_csv(translation_file):
    """Load a csv file and return a list with translations."""
    with open(translation_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        data = []
        for item in csv_reader:
            if line_count == 0:
                pass
            else:
                row = item
                data.append(row)
            line_count += 1
        return data


def _open_config_file(config_file):
    with open(config_file, "r") as file:
        return json.loads(file.read())


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "config_file", nargs="?", default="../caluma/fixtures/config.json", type=str
        )

    def handle(self, *args, **options):
        translations = []
        for file in sources:
            translations = translations + _load_csv(file)

        self._write_translations(options["config_file"], translations)

    def _write_translations(self, config_file, translations):
        """Write the translations into the config.json file."""
        data = _open_config_file(config_file)
        misses = []

        for form_model, key in properties:
            counter = 0
            form_models = (
                item for item in data if item["model"] == "form.{0}".format(form_model)
            )
            for model_entry in form_models:
                try:
                    prop = json.loads(model_entry["fields"][key], strict=False)
                    prop_de = (
                        prop["de"]
                        .replace("\\u00e4", "ä")
                        .replace("\\u00fc", "ü")
                        .replace("\\u00f6", "ö")
                    )

                    match = next((t for t in translations if t[0] == prop_de))
                    prop["fr"] = match[1]
                    model_entry["fields"][key] = json.dumps(prop)
                    counter += 1

                except StopIteration:
                    misses.append(prop_de)

            self.stdout.write(f"{counter} {form_model} were translated")

            with open(config_file, "w") as file:
                json.dump(data, file, ensure_ascii=False)

        self.stdout.write(f"Missing {len(set(misses))} translations: {set(misses)}")
