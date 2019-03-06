import csv
import json
import sys

PATH = "kt_schwyz/form.json"


def importText():
    try:
        with open(PATH) as f:
            data = json.load(f)

        changed = False
        reader = csv.reader(sys.stdin)

        for row in reader:
            if len(row) == 2:
                try:
                    if len(row[1]) > 1 and data["questions"][row[0]]["hint"] != row[1]:
                        data["questions"][row[0]]["hint"] = row[1]
                        changed = True
                except KeyError as e:
                    print("Question {0} does not exist, skipping it.".format(e))

        if changed:
            with open(PATH, "w") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

    except Exception as e:
        sys.exit("Unexpected Error occured: {0}".format(e))


def exportForm():
    try:
        with open(PATH) as f:
            data = json.load(f)
        questions = data["questions"]

        form_export = open("form-export.csv", "w")
        writer = csv.writer(form_export)

        for k, v in questions.items():
            try:
                writer.writerow([k, v["label"], v["hint"]])
            except KeyError as e:
                print("Question {0} does not have a {1}, skipping it.".format(k, e))

        form_export.close()

    except Exception as e:
        sys.exit("Unexpected Error occured: {0}".format(e))


if sys.argv[1] == "import":
    importText()
elif sys.argv[1] == "export":
    exportForm()
