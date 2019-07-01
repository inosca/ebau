import csv
import sys
from collections import Counter

from django.core.management.base import BaseCommand

from camac.user.models import Group, GroupT, Service, ServiceT

mapping = {
    "Group": {},
    "Service": {
        "phone": "Telefon",
        "zip": "PLZ",
        "address": "Strasse, Nr.",
        "email": "E-Mail",
        "website": "Website",
    },
}

mapping_t = {
    "de": {"name": "Name [DE]", "city": "Ort [DE]"},
    "fr": {"name": "Name [FR]", "city": "Ort [FR]"},
}


class ImportCommand(BaseCommand):
    skip_update = False

    def __init__(self):
        self.created = {"Service": [], "Group": []}
        self.updated = {"Service": [], "Group": []}
        self.skipped = {"Service": [], "Group": []}

    def add_arguments(self, parser):
        parser.add_argument("--path")

    def check_for_duplicates(self, data):
        counter = Counter(x.get("Name [DE]") for x in data)
        duplicates = [name for (name, count) in counter.most_common() if count > 1]

        if len(duplicates):
            print("Found {0} duplicates, aborting.".format(len(duplicates)))
            print(duplicates)
            sys.exit(1)

    def handle(self, *args, **options):
        if options["path"]:
            with open(options["path"], "r") as csvfile:
                reader = csv.DictReader(csvfile)
                data = list(reader)
        else:
            reader = csv.DictReader(sys.stdin)
            data = list(reader)

        self.check_for_duplicates(data)
        print("Duplicate check OK, importing data...")
        self.import_data(data)
        print("Done!")
        for model, entries in self.created.items():
            print(f"Created {len(entries)} {model}s")
        for model, entries in self.updated.items():
            print(f"Updated {len(entries)} {model}s")
        for model, entries in self.skipped.items():
            print(f"Skipped {len(entries)} {model}s")

    def create_or_update_group(self, row, prefix, defaults):
        return self.create_or_update_model(row, Group, GroupT, prefix, defaults)

    def create_or_update_service(self, row, prefix, defaults):
        return self.create_or_update_model(row, Service, ServiceT, prefix, defaults)

    def create_or_update_model(self, row, model, model_t, prefix="", defaults={}):
        name = get_name(prefix, row.get("Name [DE]")).strip()
        model_name = model.__name__

        pk = get_model_id_by_name(name, model_t, model_name)
        if row.get("old_name"):
            pk = get_model_id_by_name(
                get_name(prefix, row.get("old_name")).strip(), model_t, model_name
            )
            if not pk:
                print(
                    "Old name '{0}' specified, but no corresponding entry found".format(
                        row.get("old_name")
                    )
                )
                sys.exit(1)
        if pk:
            obj = model.objects.get(pk=pk)
        else:
            obj = model()

        if self.skip_update and pk:
            print("skip ({0}) {1}".format(model_name, name))
            self.skipped[model_name].append(name)
        else:
            if pk:
                print("~ ({0}) {1}".format(model_name, name))
                self.updated[model_name].append(name)
            else:
                print("+ ({0}) {1}".format(model_name, name))
                self.created[model_name].append(name)

            update_model(obj, row, model_name, defaults)
            create_or_update_model_t(row, obj, prefix, model, model_t)
        return obj


def get_model_id_by_name(name, model_t, model_name):
    filtered = model_t.objects.filter(name=name)
    if len(filtered) > 0:
        return getattr(filtered[0], model_name.lower()).pk
    return None


def create_or_update_model_t(row, obj, prefix, model, model_t):
    for lang in ["de", "fr"]:
        if not row.get(mapping_t[lang]["name"]):
            continue

        name = get_name(prefix, row.get(mapping_t[lang]["name"])).strip()
        find_by_name = name
        if row.get("old_name"):
            find_by_name = get_name(prefix, row.get("old_name")).strip()

        existing = model_t.objects.filter(name=find_by_name, language=lang)
        obj_t = existing[0] if len(existing) > 0 else model_t()

        obj_t.name = name
        obj_t.description = name
        obj_t.city = row.get(mapping_t[lang]["city"])
        setattr(obj_t, model.__name__.lower(), obj)
        obj_t.language = lang
        obj_t.save()


def update_model(obj, row, model_name, defaults):
    data = {name_model: row[key] for name_model, key in mapping[model_name].items()}

    for key, value in {**data, **defaults}.items():
        setattr(obj, key, value)
    obj.sort = 0
    obj.save()


def get_name(prefix, name):
    if prefix:
        return "{0} {1}".format(prefix, name)
    return name
