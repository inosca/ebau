import csv
import json
import sys

PATH = "kt_schwyz/form.json"


def _lookup_key(obj, path_segments):
    for segment in path_segments:
        if isinstance(obj, list):
            obj = [x for x in obj if x["name"] == segment][0]
        else:
            obj = [x for x in obj["config"]["columns"] if x["name"] == segment][0]

    return obj


def import_text():
    if len(sys.argv) < 3:
        print("No file given to import!")
        return

    with open(PATH) as f:
        data = json.load(f)

    changed = False

    with open(sys.argv[2], newline="") as content:
        reader = csv.reader(content, delimiter=";")

        for row in reader:
            if len(row) == 4:
                try:
                    slug, column_path, label, hint = row

                    if len(hint) < 2:
                        continue

                    if column_path:
                        column = _lookup_key(
                            data["questions"][slug]["config"]["columns"],
                            column_path.split("||"),
                        )
                        changed = changed or column["hint"] != hint
                        column["hint"] = hint

                    elif data["questions"][slug]["hint"] != hint:
                        data["questions"][slug]["hint"] = hint
                        changed = True
                except KeyError as e:
                    print("Question {0} does not exist, skipping it.".format(e))

        if changed:
            with open(PATH, "w") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)


def _write_recursive_columns(writer, slug, column_path, questions):
    for question in questions:
        try:
            new_column_path = (
                column_path + "||" + question["name"]
                if column_path
                else question["name"]
            )
            writer.writerow(
                [slug, new_column_path, question["label"], question["hint"]]
            )
        except KeyError as e:
            print(
                "Question {0} does not have a {1}, skipping it.".format(
                    question["name"], e
                )
            )

        if "columns" in question["config"]:
            _write_recursive_columns(
                writer, slug, new_column_path, question["config"]["columns"]
            )


def export_form():
    with open(PATH) as f:
        data = json.load(f)
    questions = data["questions"]

    form_export = open("form-export.csv", "w", encoding="utf-8")
    writer = csv.writer(form_export, delimiter=";", quotechar='"')

    for slug, question in questions.items():
        try:
            writer.writerow([slug, "", question["label"], question["hint"]])
        except KeyError as e:
            print("Question {0} does not have a {1}, skipping it.".format(slug, e))

        if "columns" in question["config"]:
            _write_recursive_columns(writer, slug, "", question["config"]["columns"])

    form_export.close()


if sys.argv[1] == "import":
    import_text()
elif sys.argv[1] == "export":
    export_form()
